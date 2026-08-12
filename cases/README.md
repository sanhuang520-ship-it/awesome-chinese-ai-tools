# 可复现的 Agent Skill 实测案例

这些不是宣传样稿，而是使用未点名 Skill 的原始任务，观察 Codex 是否自动选择正确 Skill、输出是否符合边界。每篇均记录客户端版本、任务原文、观察结果和不能外推的部分。

## 当前进度

> Codex 自动触发：**13 / 13 个本站原创 Skill** · 2 项大任务失败后通过缩小复测 · Claude Code：待测 · Cursor：待测 · 最近实测：**2026-08-12**

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

“单任务通过”只说明在记录的客户端版本、已安装 Skill 集合和那条原始任务下：目标 Skill 被自动读取，输出覆盖了预设检查点。失败案例也会保留。它不代表准确率、跨客户端兼容性，也不保证换一种问法仍会触发。

当前隔离测试还持续出现一条重要告警：Skill 数量较多时，Codex 会缩短部分 description 以适应上下文预算。13 项均发生自动触发，但这仍然只是单任务观察；后续复测必须继续保留成功和失败结果。

想复现或补充 Claude Code、Cursor 结果，请在[置顶 Discussion](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/discussions/4)提交客户端版本、原始任务和脱敏结果。
