# Agent Skills 兼容性实测

> 最近实测：**2026-08-12** · 原始记录：[data/compatibility.json](data/compatibility.json) · 校验脚本：[scripts/check_compatibility.py](scripts/check_compatibility.py)

本页只记录实际拿到的证据。**能被 CLI 发现、文件安装成功、AI 自动触发、最终任务完成，是四件不同的事。** 没运行过的客户端明确标为“待测”，不把格式兼容写成实测通过。

## 当前结论

| 检查项 | 结果 | 证据边界 |
|---|---|---|
| `skills` CLI 发现本站原创 Skill | ✅ 13 / 13 | `npx skills@1.5.22 add . --list` 找到 13 个 Skill |
| Codex 共享目录安装内容 | ✅ 13 / 13 | 仓库与 `~/.agents/skills/<name>/SKILL.md` 逐字节一致 |
| Codex 自动触发 | ⚠️ 13 / 13 | 均发生自动触发；2 项大任务失败后通过缩小复测 |
| Claude Code | ⏳ 待测 | 当前没有运行 Claude Code，不能声称通过 |
| Cursor | ⏳ 待测 | 当前没有运行 Cursor，不能声称通过 |

当前任务级案例记录的客户端为 Codex CLI `0.147.0-alpha.6.5`；这仍不代表其他 Codex 版本或任务措辞会得到相同结果。

## 13 个本站原创 Skill

| Skill | CLI 发现 | Codex 安装内容 | Codex 触发 | Claude Code | Cursor |
|---|---:|---:|---:|---:|---:|
| [`ai-learning-coach`](cases/ai-learning-coach-codex.md) | ✅ | ✅ | ⚠️¹ | ⏳ | ⏳ |
| [`book-digest-cn`](cases/book-digest-cn-codex.md) | ✅ | ✅ | ✅¹ | ⏳ | ⏳ |
| [`bookkeeping-cn`](cases/bookkeeping-cn-codex.md) | ✅ | ✅ | ✅¹ | ⏳ | ⏳ |
| [`chinese-design-md`](cases/chinese-design-md-codex.md) | ✅ | ✅ | ✅¹ | ⏳ | ⏳ |
| [`chinese-lesson-plan`](cases/chinese-lesson-plan-codex.md) | ✅ | ✅ | ⚠️¹ | ⏳ | ⏳ |
| [`chinese-typography`](cases/chinese-typography-codex.md) | ✅ | ✅ | ✅¹ | ⏳ | ⏳ |
| [`chinese-web-themes`](cases/chinese-web-themes-codex.md) | ✅ | ✅ | ✅¹ | ⏳ | ⏳ |
| [`chinese-work-report`](cases/chinese-work-report-codex.md) | ✅ | ✅ | ✅¹ | ⏳ | ⏳ |
| [`ecommerce-copywriting`](cases/ecommerce-copywriting-codex.md) | ✅ | ✅ | ✅¹ | ⏳ | ⏳ |
| [`github-readme-cn`](cases/github-readme-cn-codex.md) | ✅ | ✅ | ✅¹ | ⏳ | ⏳ |
| [`guochao-visual-cn`](cases/guochao-visual-cn-codex.md) | ✅ | ✅ | ✅¹ | ⏳ | ⏳ |
| [`guofeng-threejs`](cases/guofeng-threejs-codex.md) | ✅ | ✅ | ⚠️¹ | ⏳ | ⏳ |
| [`homework-tutor-cn`](cases/homework-tutor-cn-codex.md) | ✅ | ✅ | ✅¹ | ⏳ | ⏳ |

¹ 仅代表链接案例中的单任务、单客户端版本结果；⚠️ 包括等待用户补充，或大任务失败后仅通过缩小复测。

### 本轮发现的客户端限制

Codex 在隔离实测中报告：已安装 Skill 较多时，会为适应 skills 上下文预算而缩短部分 description。`chinese-typography` 本次仍然正确触发，但这条告警可能影响其他 Skill 的发现，因此后续测试会同时记录触发成功与未触发结果。

## 状态定义

- ✅ **已验证**：执行过对应检查，并保留了命令、日期和结果。
- ⚠️ **部分通过**：只有一部分行为得到验证，限制会写在表中。
- ❌ **失败**：已经复现不兼容或错误。
- ⏳ **待测**：没有足够证据。它不代表不兼容，也不代表通过。

## 下一轮测试

13 个原创 Skill 已各完成一次自动触发测试，两个失败项也完成缩小复测。下一步补 Claude Code / Cursor 的真实环境证据，并为大任务建立明确输出预算。

如果你能提供 Claude Code 或 Cursor 的实际结果，请用[结构化兼容性表单](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml)提交。表单会分别记录是否点名 Skill、是否触发与任务是否完成；成功和失败都欢迎，但请先删除 Token、邮箱和私人路径。
