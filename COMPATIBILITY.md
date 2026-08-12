# Agent Skills 兼容性实测

> 最近实测：**2026-08-12** · 原始记录：[data/compatibility.json](data/compatibility.json) · 校验脚本：[scripts/check_compatibility.py](scripts/check_compatibility.py)

本页只记录实际拿到的证据。**能被 CLI 发现、文件安装成功、AI 自动触发、最终任务完成，是四件不同的事。** 没运行过的客户端明确标为“待测”，不把格式兼容写成实测通过。

## 当前结论

| 检查项 | 结果 | 证据边界 |
|---|---|---|
| `skills` CLI 发现本站原创 Skill | ✅ 13 / 13 | `npx skills@1.5.22 add . --list` 找到 13 个 Skill |
| Codex 共享目录安装内容 | ✅ 13 / 13 | 仓库与 `~/.agents/skills/<name>/SKILL.md` 逐字节一致 |
| Codex 自动触发 | ⏳ 待逐项任务测试 | 安装成功不等于在正确任务里自动触发 |
| Claude Code | ⏳ 待测 | 当前没有运行 Claude Code，不能声称通过 |
| Cursor | ⏳ 待测 | 当前没有运行 Cursor，不能声称通过 |

当前 Codex 客户端为桌面版，但本次没有记录精确构建号，因此不把结论外推到所有版本。

## 13 个本站原创 Skill

| Skill | CLI 发现 | Codex 安装内容 | Codex 触发 | Claude Code | Cursor |
|---|---:|---:|---:|---:|---:|
| `ai-learning-coach` | ✅ | ✅ | ⏳ | ⏳ | ⏳ |
| `book-digest-cn` | ✅ | ✅ | ⏳ | ⏳ | ⏳ |
| `bookkeeping-cn` | ✅ | ✅ | ⏳ | ⏳ | ⏳ |
| `chinese-design-md` | ✅ | ✅ | ⏳ | ⏳ | ⏳ |
| `chinese-lesson-plan` | ✅ | ✅ | ⏳ | ⏳ | ⏳ |
| `chinese-typography` | ✅ | ✅ | ⏳ | ⏳ | ⏳ |
| `chinese-web-themes` | ✅ | ✅ | ⏳ | ⏳ | ⏳ |
| `chinese-work-report` | ✅ | ✅ | ⏳ | ⏳ | ⏳ |
| `ecommerce-copywriting` | ✅ | ✅ | ⏳ | ⏳ | ⏳ |
| `github-readme-cn` | ✅ | ✅ | ⏳ | ⏳ | ⏳ |
| `guochao-visual-cn` | ✅ | ✅ | ⏳ | ⏳ | ⏳ |
| `guofeng-threejs` | ✅ | ✅ | ⏳ | ⏳ | ⏳ |
| `homework-tutor-cn` | ✅ | ✅ | ⏳ | ⏳ | ⏳ |

## 状态定义

- ✅ **已验证**：执行过对应检查，并保留了命令、日期和结果。
- ⚠️ **部分通过**：只有一部分行为得到验证，限制会写在表中。
- ❌ **失败**：已经复现不兼容或错误。
- ⏳ **待测**：没有足够证据。它不代表不兼容，也不代表通过。

## 下一轮测试

按真实任务逐个验证 Codex 自动触发，先从 `chinese-typography`、`github-readme-cn`、`chinese-work-report` 开始。每条记录至少包含任务原文、客户端与版本、是否自动触发、关键输出、人工修改和已知限制。

如果你能提供 Claude Code 或 Cursor 的实际结果，请在[置顶 Discussion](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/discussions/4)按模板回复。成功和失败都欢迎，但请先删除 Token、邮箱和私人路径。
