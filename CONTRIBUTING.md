# CONTRIBUTING

## 双链分离原则（本项目最重要的规矩）

| 链 | 规则 | 落点 |
|----|------|------|
| **归责链** | commit `author` 字段必须人类身份（DCO）；法律责任落法人/自然人 | git metadata |
| **信任链** | 角色名/别名只进 commit message、卡片 `source` 字段——做淬炼见证，不做担保人 | 内容层 |

角色名不得出现在任何**责任语义**位置（"XX 批准过"、"XX 担保"无效）。角色 = 出处，不是担保人。

## 贡献卡片

1. `cards/<semantic-slug>/` 目录，含 `card.yaml` + `card.md` 双卡（见 `schema/card.schema.yaml`）
2. `card.yaml` 必填字段齐全；`steps` 必须可操作（不是抽象原则）
3. `card.md` 必须 ≥1 个真实案例 + ≥1 条诚实风险提示
4. **去重检查**：提交前 grep 卡库确认无重复命题（triggers 重叠 ≥50% 视为候选合并）
5. `source` 字段写清淬炼出处——经受不起"这张卡怎么来的"追问的卡不要提交

## 卡片质量门槛

- 不收 prompt 片段（那是另一个生态的事）
- 不收无 failure_conditions 的万能卡（什么都能用的卡 = 什么都测不出的卡）
- 工具化声明诚实：T1 卡必须附带可执行的 lint 规则，否则降级 T3
  - **过渡条款（至 P1 runner 落地）**：P0 期 T1 卡的 lint_rules 允许为规格描述；runner 落地（ROADMAP P1）时未通过执行验证的 T1 声明自动降级为 T3

## source 字段锚点要求（防编造）

source 不能是裸自由文本，至少包含其一：
1. 可达存档链接（公开辩论记录/issue/commit hash）
2. 显式声明：`private-system` + 系统描述 + 日期（如 `crucible debate #149, 2026-08-15, 8-role private debate system`）——声明私有即承认不可公开审计，读者自行折价采信

## 修正是贡献

修正既有卡片的错误 = 高价值贡献（不是打脸）。修正 PR 请附：原卡错在哪、新证据是什么。
