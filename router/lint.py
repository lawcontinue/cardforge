#!/usr/bin/env python3
"""cardforge lint runner — deterministic T1 rules for agent claims.

Rules (each maps to a seed card's lint_rules field):
  absolute-claims  — "唯一/首个/最大/唯一/first/only/largest" without >=3 sources flagged (card: decision-3q ecosystem)
  number-sanity    — "一个数量级/N倍/10x" claims recomputed; flags order-of-magnitude exaggeration
  decision-gates   — decision docs missing verifiable baseline (Q1) or opposition (Q3)
  paraphrase-diff  — strawman detection: paraphrase vs source negation/entity mismatch

Exit code: number of findings (0 = clean). CI-friendly.

Usage:
  python3 router/lint.py scan docs/decisions/decision.md
  python3 router/lint.py diff --source original.txt --paraphrase attack.txt
  python3 router/lint.py scan README.md ROADMAP.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict

ABSOLUTE_PAT = re.compile(
    r"(唯一|首个|第一个|最大|最全|完全|彻底|绝对的|the only|first ever|largest|completely|absolutely)",
    re.IGNORECASE,
)
SOURCE_HINT_PAT = re.compile(r"(来源|source|依据|according to|参考|\[\d+\]|\(20\d\d\))", re.IGNORECASE)
MAGNITUDE_PAT = re.compile(r"一个数量级|指数级|an order of magnitude|exponential", re.IGNORECASE)
MULTIPLE_PAT = re.compile(r"(\d+(?:\.\d+)?)\s*(?:倍|x|X|×|times|fold)")
NUMBER_PAT = re.compile(r"\d+(?:\.\d+)?")
MAJOR_PAT = re.compile(r"(重大|P0|architecture|架构决策|major decision|不可逆)", re.IGNORECASE)
BASELINE_PAT = re.compile(r"(\d+(?:\.\d+)?\s*[%‰]?|benchmark|基线|baseline|实测|measured|数据集|dataset)", re.IGNORECASE)
OPPOSITION_PAT = re.compile(r"(反对|谁会反对|objector|反方|risk|风险|最坏|worst[- ]case|谁会反对)", re.IGNORECASE)

SENT_SPLIT = re.compile(r"[。；;.!?！？\n]")
NEGATIONS = {"不", "没", "无", "非", "not", "no", "never", "cannot", "can't", "without"}


@dataclass
class Finding:
    rule: str
    severity: str  # warn
    line: int
    excerpt: str
    note: str


def _lines_with_match(text: str, pat: re.Pattern):
    for i, line in enumerate(text.splitlines(), 1):
        m = pat.search(line)
        if m:
            yield i, line.strip(), m


def rule_absolute_claims(text: str) -> list[Finding]:
    out = []
    for i, line, m in _lines_with_match(text, ABSOLUTE_PAT):
        ctx = text[max(0, text.find(line) - 200): text.find(line) + len(line) + 200]
        source_count = len(SOURCE_HINT_PAT.findall(ctx))
        if source_count < 3:
            out.append(
                Finding("absolute-claims", "warn", i, line[:100],
                        f"absolute claim '{m.group(0)}' with <3 source hints ({source_count}) in context")
            )
    return out


def rule_number_sanity(text: str) -> list[Finding]:
    out = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if MAGNITUDE_PAT.search(line):
            nums = [float(n) for n in NUMBER_PAT.findall(line)]
            if len(nums) >= 2:
                a, b = max(nums), min(nums)
                ratio = a / b if b else float("inf")
                if ratio < 10:
                    out.append(
                        Finding("number-sanity", "warn", i + 1, line[:100],
                                f"claimed 'order of magnitude' but numbers give {ratio:.1f}x (<10x)")
                    )
        for m in MULTIPLE_PAT.finditer(line):
            claimed = float(m.group(1))
            others = [float(n) for n in NUMBER_PAT.findall(line) if abs(float(n) - claimed) > 1e-9]
            # heuristic: if two anchor numbers present, recompute
            if len(others) >= 2:
                ratio = max(others) / min(others) if min(others) else float("inf")
                if ratio > 0 and abs(ratio - claimed) / max(claimed, 1e-9) > 0.5:
                    out.append(
                        Finding("number-sanity", "warn", i + 1, line[:100],
                                f"claimed {claimed}x but anchors compute {ratio:.1f}x")
                    )
    return out


def rule_decision_gates(text: str) -> list[Finding]:
    out = []
    is_major = bool(MAJOR_PAT.search(text))
    if not BASELINE_PAT.search(text):
        out.append(Finding("decision-gates", "warn", 1, "<document>",
                           "no-baseline: no verifiable number/benchmark found (Q1 missing)"))
    if is_major and not OPPOSITION_PAT.search(text):
        out.append(Finding("decision-gates", "warn", 1, "<document>",
                           "missing-opposition: major-flagged decision lacks Q3 opposition/worst-case section"))
    return out


def _entities(text: str) -> set[str]:
    words = set(re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}|[\u4e00-\u9fff]{2,4}", text.lower()))
    return words


def rule_paraphrase_diff(source: str, paraphrase: str) -> list[Finding]:
    out = []
    for i, pline in enumerate(paraphrase.splitlines(), 1):
        pline = pline.strip()
        if not pline:
            continue
        p_ents = _entities(pline)
        p_neg = bool(re.search(r"\b(not|no|never|cannot)\b|不|没|无|非", pline.lower()))
        best, best_overlap = None, 0.0
        for sline in source.splitlines():
            s_ents = _entities(sline)
            if not p_ents or not s_ents:
                continue
            overlap = len(p_ents & s_ents) / len(p_ents)
            if overlap > best_overlap:
                best, best_overlap = sline, overlap
        if best is None:
            continue
        s_neg = bool(re.search(r"\b(not|no|never|cannot)\b|不|没|无|非", best.lower()))
        if best_overlap >= 0.3 and p_neg != s_neg:
            out.append(
                Finding("paraphrase-diff", "warn", i, pline[:100],
                        f"negation mismatch vs closest source line ({best_overlap:.0%} overlap): '{best.strip()[:80]}'")
            )
    return out


def scan(paths: list[str], as_json: bool = False) -> int:
    findings: list[Finding] = []
    for p in paths:
        text = open(p, encoding="utf-8").read()
        findings += rule_absolute_claims(text)
        findings += rule_number_sanity(text)
        findings += rule_decision_gates(text)
    if as_json:
        print(json.dumps([asdict(f) for f in findings], ensure_ascii=False, indent=2))
    else:
        for f in findings:
            print(f"[{f.rule}] L{f.line}: {f.note}\n    > {f.excerpt}")
        print(f"\n{len(findings)} finding(s) in {len(paths)} file(s)")
    return len(findings)


def main() -> None:
    ap = argparse.ArgumentParser(description="cardforge T1 lint runner")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan")
    s.add_argument("paths", nargs="+")
    s.add_argument("--json", action="store_true")
    d = sub.add_parser("diff")
    d.add_argument("--source", required=True)
    d.add_argument("--paraphrase", required=True)
    args = ap.parse_args()

    if args.cmd == "scan":
        sys.exit(min(scan(args.paths, args.json), 1))
    elif args.cmd == "diff":
        src = open(args.source, encoding="utf-8").read()
        par = open(args.paraphrase, encoding="utf-8").read()
        findings = rule_paraphrase_diff(src, par)
        for f in findings:
            print(f"[{f.rule}] L{f.line}: {f.note}")
        sys.exit(min(len(findings), 1))


if __name__ == "__main__":
    main()
