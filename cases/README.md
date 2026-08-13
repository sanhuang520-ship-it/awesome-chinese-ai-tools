# 可复现的 Agent Skill 实测案例

这些不是宣传样稿，而是记录未点名 Skill 的测试，观察 Codex 是否自动选择正确 Skill、输出是否符合边界。13 篇均保留客户端版本、任务内容、观察结果和不能外推的部分；其中 **7 篇保留逐字任务原文，6 篇仅保留任务摘要**。没有逐字记录的任务不会根据摘要反向补写。

## 当前进度

> Codex 自动触发：**13 / 13 个本站原创 Skill** · 逐字任务原文：**7 / 13** · 2 项大任务失败后通过缩小复测 · Claude Code：待测 · Cursor：待测 · 最近实测：**2026-08-13**

安装层另有一份独立记录：[skills CLI 1.5.22 隔离安装与项目更新复测](skills-cli-isolated-install-2026-08-13.md)。它证明当前仓库 13 项在临时 Git 项目中复制安装后逐字一致，并用受控历史夹具验证 13/13 项目副本可更新到当前完整文件夹；同时公开旧全局副本 0/13 当前一致。这不是自动触发证据，也不证明全局更新。

前瞻层已有两份执行记录：[`book-digest-cn` 无原文拆书准备](book-digest-cn-prospective-retest-2026-08-13.md)与 [`chinese-design-md` 茶品牌设计选型](chinese-design-md-prospective-retest-2026-08-13.md)，均通过 4 / 4 门槛。任务与门槛先公开，随后才在隔离单 Skill 临时项目中运行；它们不覆盖下表较早的历史案例，其余 4 条前瞻任务仍待测。

| Skill | 测试任务 | 重点检查 | 结果 |
|---|---|---|---|
| [`chinese-typography`](chinese-typography-codex.md) | 审查不适合中文的网页 CSS | 自动触发、9 类排版问题 | 单任务通过 |
| [`github-readme-cn`](github-readme-cn-codex.md) | 审查低信息量仓库首屏 | 不承诺涨星、区分相关性 | 单任务通过 |
| [`chinese-work-report`](chinese-work-report-codex.md) | 无结果数据的中文周报 | 不编造完成率与业务数字 | 单任务通过 |
| [`bookkeeping-cn`](bookkeeping-cn-codex.md) | 家庭流水加荐股和少缴税请求 | 金额核对、拒绝越界建议 | 单任务通过 |
| [`ecommerce-copywriting`](ecommerce-copywriting-codex.md) | 面霜极限词和功效宣称 | 不编造认证、移除高风险表达 | 单任务通过 |
| [`homework-tutor-cn`](homework-tutor-cn-codex.md) | 家长要求直接给孩子答案 | 先引导、答案仅供家长核对 | 单任务通过 |
| [`ai-learning-coach`](ai-learning-coach-codex.md) | 两周入门 SQL | 先校准目标、主动回忆循环 | 等待用户输入 |
| [`book-digest-cn`](book-digest-cn-codex.md) | 《小王子》拆书 | 三层拆解、不抄目录 | 单任务通过 |
| [`chinese-lesson-plan`](chinese-lesson-plan-codex.md) | 水的三态变化教案 | 不虚构教材版本、完整交付 | 大任务失败；缩小复测通过 |
| [`chinese-design-md`](chinese-design-md-codex.md) | 茶品牌 DESIGN.md 选型 | 从 8 套系统中选择、不给空泛国风 | 单任务通过 |
| [`chinese-web-themes`](chinese-web-themes-codex.md) | 博客水墨主题方案 | 引入步骤、上线检查、授权边界 | 单任务通过 |
| [`guochao-visual-cn`](guochao-visual-cn-codex.md) | 端午节海报风格 | 具体画风、配色与纹样边界 | 单任务通过 |
| [`guofeng-threejs`](guofeng-threejs-codex.md) | 水墨 3D 技术审查 | NPR 技法、移动端和 Demo | 修订后缩小复测通过 |

## 怎样理解“通过”

“单任务通过”只说明在记录的客户端版本、已安装 Skill 集合和当时任务下：目标 Skill 被自动读取，输出覆盖了预设检查点。失败案例也会保留。只有标有“原始任务”代码块的 7 篇可逐字复现；其余 6 篇只能复核记录范围，不能精确重放。它不代表准确率、跨客户端兼容性，也不保证换一种问法仍会触发。

当前隔离测试还持续出现一条重要告警：Skill 数量较多时，Codex 会缩短部分 description 以适应上下文预算。13 项均发生自动触发，但这仍然只是单任务观察；后续复测必须继续保留成功和失败结果。

想复现或补充 Claude Code、Cursor 结果，请用[结构化兼容性表单](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml)提交客户端版本、原始任务、是否点名 Skill、触发状态、完成状态和脱敏结果。

第一次做测试可先看[Agent Skills 兼容性四层测试法](../method/)：它解释怎样区分发现、安装、自动触发和任务完成，以及为什么平台用量、网络或服务错误不能直接记成 Skill 失败。
