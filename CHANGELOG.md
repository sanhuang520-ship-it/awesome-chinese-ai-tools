# 变更日志

本项目只记录用户能复核的功能、数据与证据变化。自动更新星数、复检日期等日常提交不逐条列入。

## [v1.1.0] - 2026-08-12

### 新增

- 13 个本站原创 Skill 的 Codex 自动触发矩阵与逐项案例。
- 独立的[兼容性实测页](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/compatibility/)，区分 CLI 发现、文件安装、自动触发和任务完成。
- 独立的[安装与排错页](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/install/)，记录 `skills` CLI 1.5.22 的本机路径结果。
- 原创 Skill 的静态质量与安全标签，包括脚本、凭据、写文件与运行时网络能力。
- 结构化兼容性 Issue 表单，接收 Codex、Claude Code、Cursor 的成功、失败或未触发结果。
- `llms.txt`、可验证更新 RSS、站内链接检查、公开数据一致性和证据边界测试。

### 修正

- 移除旧自动“今日工具推荐”及 RSS 中未经持续复核的 AI 日报。
- 移除“最好用”“国内最强”“完全免费无限次”等无测量依据或易过期表述。
- 不再把 Vercel Labs 的 `skills` CLI 称作官方 CLI。
- 不再根据 `~/.claude/skills/` 符号链接推断 Claude Code 已自动触发。
- 修复兼容性页面的案例索引断链，并将断链检查加入每日维护。

### 当前证据边界

- Codex：13/13 在单任务中发生自动触发；11 项首次完成，2 项大任务失败后缩小复测通过。
- Claude Code：待任务级实测。
- Cursor：待任务级实测。
- 本版本不声明准确率、正式安全认证或跨客户端全面兼容。

[v1.1.0]: https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/releases/tag/v1.1.0
