# ROADMAP

## P0 ✅ (2026-08-16)
- schema v1.0（双卡绑定：yaml 机器卡 + md 人读卡，语义 slug 防 ID 冲突）
- 仓库骨架（cards/router/capture/docs/schema）
- README（叙事 v2 + FAQ 三条 + 反对意见段）
- CONTRIBUTING（双链分离原则）
- 6 张种子卡

## P1 路由引擎（+1 周，8-15h）
- [ ] 四层分类器开源（关键词 → TF-IDF → 规则 → embedding，可插拔后端）
- [ ] 测试套件（r1/r2/OOD/regression）+ 数据集开源（README 脚注 ² 的兑现）
- [ ] **lint runner：T1 卡 lint_rules 可执行化**（strawman paraphrase-diff / decision gates / number-sanity / absolute-claims-lint）——落地时对 P0 两张 T1 卡执行验证，未过自动降级 T3
- [ ] **CI：双链分离强制**（GitHub Actions 校验 commit author 非角色名 + 卡片双卡绑定/frontmatter id 一致性/schema 机器可读版 JSON Schema）——Shield P0，发布前阻塞项
- [ ] README.en.md 完整英文版（首屏双语已修，完整版 P1）

## P2 沉淀管线 + 卡库扩充（+2 周，10-20h）
- [ ] capture：贡献评级模板 + 去重检查 + 注册工具
- [ ] 种子库扩充至 30 张（含精选方法论迁移）
- [ ] 中文先发（dsh 生态中文主场），双语化等国际信号

## P3 agent 插件（触发式：等 dsh API stable v1）
- [ ] claim-lint 插件（T1 规则打包）
- [ ] card-invoke 接口（agent 运行时按 triggers 路由调用）
- [ ] 生态发布观察 7 天 star/issue → 决定追加投入（负需求验证）

## 战略约束
- 时间盒封顶：每周 ≤10h，主现金流项目优先
- 定位：生态卡位 + 获客漏斗，非第四主线
- 全量投入等两个信号：① dsh API stable ② 生态出现第一个非能力型插件
