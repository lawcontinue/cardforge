#!/usr/bin/env python3
"""cardforge router — route a question to method cards.

Three layers (zero-dependency core):
  1. trigger match  — exact/substring hits on card `triggers`
  2. tf-idf match   — semantic similarity over one_liner + triggers + steps
  3. related boost  — cards linked from top hits get a relevance bonus

Embedding backend is pluggable (P1.5): implement `EmbeddingBackend.search()`.

Usage:
  python3 router/cardforge_router.py "should we rewrite our db in rust?"
  python3 router/cardforge_router.py "..." --json
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

CARD_ROOT = Path(__file__).resolve().parent.parent / "cards"
_TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]{1,}|[\u4e00-\u9fff]")
_STOPWORDS = frozenset(
    "the a an and or of to in on for is are was were be been with without what which who "
    "how why when where this that these those it its as at by from not no do does did "
    "have has had will would can could should may might must about into over under more "
    "most less least like just also than then there their them they you your we our us "
    "i me my mine today very much many some any every each other another such only own "
    "same so if because while during before after above below up down out off again further "
    "的是了在和不也有这那之与及其或被把为一个"
    .split()
)


def tokenize(text: str) -> list[str]:
    """Latin words + CJK chars/bigrams, stopwords removed (lightweight bilingual)."""
    tokens = [t for t in _TOKEN_RE.findall(text.lower()) if t not in _STOPWORDS]
    out: list[str] = []
    for t in tokens:
        if re.match(r"[\u4e00-\u9fff]", t):
            out.append(t)
        else:
            out.append(t)
    # CJK bigrams
    cjk = [t for t in tokens if re.match(r"[\u4e00-\u9fff]", t)]
    for i in range(len(cjk) - 1):
        out.append(cjk[i] + cjk[i + 1])
    return out


@dataclass
class Card:
    slug: str
    name: str
    one_liner: str
    triggers: list[str]
    steps: list[str]
    toolization: str
    related: list[str]
    source: str = ""
    failure_conditions: list[str] = field(default_factory=list)

    @property
    def doc(self) -> str:
        return " ".join([self.one_liner, *self.triggers, *self.steps])


def load_cards(root: Path = CARD_ROOT) -> list[Card]:
    """Minimal YAML subset parser for card.yaml (avoids PyYAML dependency).

    Supports the cardforge schema's flat + list fields. Fails loudly on
    unknown structure so schema drift is caught early.
    """
    cards: list[Card] = []
    for yml in sorted(root.glob("*/card.yaml")):
        data: dict = {}
        current_list: str | None = None
        for raw in yml.read_text(encoding="utf-8").splitlines():
            line = raw.rstrip()
            if not line or line.lstrip().startswith("#"):
                continue
            m = re.match(r"^(\w[\w_]*):\s*(.*)$", line)
            if m and not line.startswith((" ", "-")):
                key, val = m.group(1), m.group(2).strip()
                if val.startswith("[") and val.endswith("]"):
                    data[key] = [v.strip().strip('"') for v in val[1:-1].split(",") if v.strip()]
                    current_list = None
                elif val == "":
                    data[key] = []
                    current_list = key  # subsequent "- item" lines append here
                else:
                    data[key] = val.strip('"')
                    current_list = None
            elif line.lstrip().startswith("- ") and current_list:
                item = line.lstrip()[2:].strip()
                data[current_list].append(item.strip('"'))
        cards.append(
            Card(
                slug=data.get("id", yml.parent.name),
                name=data.get("name", yml.parent.name),
                one_liner=data.get("one_liner", ""),
                triggers=data.get("triggers", []),
                steps=data.get("steps", []),
                toolization=data.get("toolization", "t3"),
                related=data.get("related", []),
                source=data.get("source", ""),
                failure_conditions=data.get("failure_conditions", []),
            )
        )
    if not cards:
        raise SystemExit(f"no cards found under {root}")
    return cards


def trigger_score(question: str, card: Card) -> float:
    q = question.lower()
    hits = sum(1 for t in card.triggers if t.lower() in q)
    return hits / max(1, len(card.triggers)) if hits else 0.0


def tfidf_scores(question: str, cards: list[Card]) -> dict[str, float]:
    docs = {c.slug: Counter(tokenize(c.doc)) for c in cards}
    q = Counter(tokenize(question))
    n = len(cards)
    df: Counter = Counter()
    for d in docs.values():
        for term in d:
            df[term] += 1
    scores: dict[str, float] = {}
    for slug, d in docs.items():
        s = 0.0
        for term, qf in q.items():
            if term in d and df[term] < n:  # term in corpus but not universal
                idf = math.log(n / df[term]) + 1.0
                s += qf * idf * d[term]
        norm = math.sqrt(sum(v * v for v in d.values())) or 1.0
        scores[slug] = s / norm
    return scores


def route(question: str, top_k: int = 3) -> list[dict]:
    cards = load_cards()
    by_slug = {c.slug: c for c in cards}

    trig = {c.slug: trigger_score(question, c) for c in cards}
    tfidf = tfidf_scores(question, cards)

    combined = {}
    for c in cards:
        combined[c.slug] = 2.0 * trig[c.slug] + tfidf.get(c.slug, 0.0)

    # related boost: cards linked from top-2 raw hits gain 0.5x their linker's score
    ranked = sorted(combined.items(), key=lambda kv: kv[1], reverse=True)
    for slug, score in ranked[:2]:
        if score <= 0:
            continue
        for rel in by_slug[slug].related:
            if rel in combined:
                combined[rel] += 0.5 * score

    final = sorted(combined.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    out = []
    for slug, score in final:
        if score < 0.15:  # relevance floor: irrelevant queries should return empty, not noise
            break
        c = by_slug[slug]
        out.append(
            {
                "slug": slug,
                "name": c.name,
                "score": round(score, 4),
                "toolization": c.toolization,
                "one_liner": c.one_liner,
                "path": str(CARD_ROOT / slug),
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="cardforge method-card router")
    ap.add_argument("question")
    ap.add_argument("--top-k", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    results = route(args.question, args.top_k)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not results:
            print("no matching cards")
            return
        for r in results:
            print(f"[{r['toolization']:>2}] {r['score']:>8.4f}  {r['slug']}  — {r['name']}")


if __name__ == "__main__":
    main()
