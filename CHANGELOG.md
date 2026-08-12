# 变更日志

本项目只记录用户能复核的功能、数据与证据变化。自动更新星数、复检日期等日常提交不逐条列入。

## [v1.1.1] - 2026-08-12

### 可信度与发现性

- 新增英文项目入口，并由同步器维护 184 个 Skill 条目、141 个来源仓库、13 个本站原创和 46 个工具入口的动态数字。
- 公开口径不再混用 Skill 条目与来源仓库；第三方描述明确不等于逐项功能实测。
- 工具选择器与工作流统一标为不代表质量排名的目录示例，商业条款统一标为历史记录。
- Community Profile 达到 100%；新增社区行为规范、安全政策，并启用 GitHub 私密漏洞报告。

### 自动化与质量

- 修复每日工具检测状态不变时不落盘检测日期的问题；官方 Actions 复检已验证成功。
- Skill 仓库复检按 141 个来源仓库去重请求，避免同仓库多条 Skill 重复访问。
- 元数据命令默认只检查且不改文件，`--write` 才写回，与贡献指南保持一致。
- 13 个原创 Skill 新增目录/frontmatter、本地引用、符号链接与可执行脚本检查。
- 新增目录字段注入门槛、外链 `noopener` 和关键控件无障碍标签回归测试；本版本本地验证共 57 项测试。

### 证据边界

- Codex：仍为 13/13 单任务自动触发；11 项首次完成，2 项缩小复测通过。
- Claude Code 与 Cursor：仍待任务级实测。
- GitHub Stars 在本版本发布前仍为 7；不能将上述改动表述为已经带来增长。

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
[v1.1.1]: https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/releases/tag/v1.1.1
