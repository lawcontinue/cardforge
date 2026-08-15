# cardforge

> **角色已死，方法论当立。** / The Persona is dead. Long live the Method.
>
> Method cards for agents, forged in real debates — a capture → store → route → invoke system, not another prompt library.

方法论卡片的**沉淀 → 存储 → 路由 → 调用**完整系统。不是又一个 prompt 库——每张卡都是经过真实多角色辩论淬炼、可审计、可路由、可组合的**决策程序**。

---

## 为什么

生态里有上万张角色卡（"你是资深架构师…"），可审计的决策程序在我们审计过的生态样本中罕见¹。角色扮演不可测量、不可组合、不可复利；方法论全部可以：

| | 角色卡 | 方法论卡 |
|---|--------|---------|
| 可测量 | ✗ 扮演质量无断言 | ✓ 路由命中率 / OOD 实测² |
| 可组合 | ✗ 人格不可拼接 | ✓ triggers + steps + failure_conditions 结构化 |
| 复利 | ✗ 角色越多维护越重 | ✓ 148 场辩论 → 每场残值沉淀为资产 |

¹ 基于对 agent 生态插件目录的人工审计（2026-08），非穷举统计。
² 内部路由器项目实测：工程类问题卡路由覆盖率 22%→68%，OOD 命中率 85.5%（110 题开发期测试集，样本量低于验收线 200 条，数据集与测试脚本随 P1 路由引擎开源）。

**死的是角色的 runtime 实体性**——作为能力容器、作为依赖、作为归责对象。角色转世三去向：构建期做出处（署名/provenance），关系层做温度（可埋怨/可信任），接口层做盲区声明。

**一问切分法**：CI 会不会因为这个角色挂掉？会 → 移出依赖图；不会 → 合法保留在元数据层。

## 判别工具（T1 规则规格已定，runner 实现在 P1）

```text
# T1 纯规则层（确定性代码，无需 LLM）——规格见对应卡 lint_rules 字段
strawman-detection   # 转述-原文 diff 对照
number-sanity        # "一个数量级/N倍" 声明反算
absolute-claims-lint # "唯一/首个/最大" 无来源即警告
decision-gates       # no-baseline / missing-opposition 门控
```

## 使用

```bash
# 路由：问题 → 方法卡（零依赖，Python 3.9+）
python3 router/cardforge_router.py "before committing to the architecture decision, go or no-go"
# [t1]   4.9261  decision-three-questions  — Progressive Decision Three-Questions

# Lint：确定性声明质检（T1 规则，CI 友好）
python3 router/lint.py scan docs/decision.md          # 扫描绝对性声明/伪数量级/决策门控
python3 router/lint.py diff --source src.txt --paraphrase attack.txt  # 稼草人检测

# 测试（含双卡绑定校验）
python3 -m pytest tests/ -q
```

**已知误报模式**（诚实披露）：确定性规则有盲区——规则自身文档含触发词（自指误报）、多义词（“张力未完全消解”的“完全”非绝对性声明）。因此 lint 输出是 **warn 不是 error**，CI 不阻塞；人来裁决。

## 架构

```
L1 Spec     卡片格式规范（YAML 机器卡 + MD 人读卡，双卡绑定）
L2 Capture  沉淀管线（辩论 → 贡献评级 → 格式化 → 去重 → 注册）
L3 Route    路由引擎（关键词 → TF-IDF → 规则 → embedding，四层降级可插拔）
L4 Invoke   调用运行时（agent 插件 / claim-lint）
L5 Cards    种子卡库（本仓库 cards/）
```

**双格式是设计，不是债**：`card.yaml` 给路由器和 agent 消费，`card.md` 给人读。一张方法论卡 = 机器可路由的决策程序 + 人类可读的淬炼叙事。

## 种子卡（第一批，6 张）

| 卡 | 类型 | 工具化层级 |
|----|------|-----------|
| `strawman-detection` 诡辩识别三层定位 | review | T1（diff 子集可代码化） |
| `decision-three-questions` 决策前三问 | decision | T1（门控规则） |
| `blind-spot-field` 盲区自省字段 | design | T3 |
| `position-revision-incentive` 立场修正激励 | debate | T3 |
| `three-stage-reincarnation` 三段转世模型 | design | T3 |
| `runtime-buildtime-separation` Runtime/Build-time 角色分离 | architecture | T3 |

每张卡都在真实多角色辩论系统中淬炼（出处见卡片 `source` 字段）——角色在这里只做**出处见证**（build-time provenance），不做运行时依赖。

## FAQ

**Q：你们自己不就是一套多角色系统吗？**
A：角色是卡片的人格化索引——UI，不是内核。角色 = commit message 里的淬炼署名，不是 author 字段（author 必须人类身份，见 CONTRIBUTING）。系统的产出物是卡片，不是人格。

**Q：AI companion 产品里角色是产品本体，也死了吗？**
A：本叙事仅限**能力架构域**。companion 产品中角色是内容本体（用户买的就是角色体验），不在宣战范围。

**Q：方法论能提供情感锚点和责任归属吗？**
A：这是本系统最诚实的未解张力。我们的回应：情感锚点保留在关系层（转世），责任归属走**双链分离**——归责链上零角色（commit author 必须人类身份，法律责任落法人），信任链上显式角色（出处签名）。张力未完全消解，欢迎来辩。

## 路线图

- **P0** ✅ schema + 骨架 + README + 6 张种子卡
- **P1** 路由引擎开源（四层分类器 + 测试套件 + 实测数据）
- **P2** 沉淀管线（capture）+ 种子库扩充
- **P3** agent 插件接口（claim-lint / card-invoke）

## License

MIT

## 反对意见（诚实记录）

persona 派最强反方：*角色提供用户情感锚点和责任归属接口，方法论不提供。人买的是"谁在帮我"，不是"哪条程序在跑"。* 本系统以"角色转世 + 双链分离"回应，不假装此立场不存在。
