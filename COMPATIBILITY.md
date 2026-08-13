# Agent Skills 兼容性实测

> 最近实测：**2026-08-13** · 原始记录：[data/compatibility.json](data/compatibility.json) · 汇总校验：[scripts/check_compatibility.py](scripts/check_compatibility.py) · 单次报告规范：[JSON Schema](schemas/compatibility-result.schema.json)

本页只记录实际拿到的证据。**能被 CLI 发现、文件安装成功、AI 自动触发、最终任务完成，是四件不同的事。** 没运行过的客户端明确标为“待测”，不把格式兼容写成实测通过。

## 当前结论

| 检查项 | 结果 | 证据边界 |
|---|---|---|
| `skills` CLI 发现本站原创 Skill | ✅ 13 / 13 | `npx skills@1.5.22 add . --list` 找到 13 个 Skill |
| Codex 隔离项目安装内容 | ✅ 13 / 13 | `skills@1.5.22 --copy` 安装至临时 Git 项目的 `.agents/skills/`，与当前仓库逐字节一致；[查看复测记录](cases/skills-cli-isolated-install-2026-08-13.md) |
| 项目级旧副本更新 | ✅ 13 / 13 | 受控历史夹具中的 13 个完整 Skill 文件夹经 `skills@1.5.22 update -p -y` 更新后均与当前仓库一致；全局文件未改变 |
| 既有全局安装副本 | ⚠️ 0 / 13 当前一致 | 8 月 8 日安装后，仓库又新增元数据并修订内容；安装不是持续同步，不能把旧副本当成当前版本 |
| Codex 自动触发 | ⚠️ 13 / 13 | 10 项当次任务完成；1 项按流程等待必要输入；2 项大任务失败后通过缩小复测 |
| Claude Code | ⏳ 待测 | 当前没有运行 Claude Code，不能声称通过 |
| Cursor | ⏳ 待测 | 当前没有运行 Cursor，不能声称通过 |

当前任务级案例记录的客户端为 Codex CLI `0.147.0-alpha.6.5`；这仍不代表其他 Codex 版本或任务措辞会得到相同结果。安装复测与任务级自动触发是两轮不同证据，不能互相替代。

另有 6 条运行前公开任务与成功门槛的前瞻复测：`book-digest-cn` 与 `chinese-design-md` 已分别在隔离单 Skill 临时项目中执行并通过 4 / 4 门槛；[拆书记录](cases/book-digest-cn-prospective-retest-2026-08-13.md)和[设计选型记录](cases/chinese-design-md-prospective-retest-2026-08-13.md)保留命令、文件哈希与边界。其余 4 条仍为 `planned`，不计为通过。这组结果不改写上表的首次自动触发 10 / 1 / 2 统计。

## 13 个本站原创 Skill

| Skill | CLI 发现 | 隔离安装内容 | Codex 触发 | Claude Code | Cursor |
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

### 安装不是自动更新

2026-08-13 复查时，未固定版本的 `npx skills --version` 命中了本机旧缓存 `1.5.18`，而 npm `latest` 与本轮固定复测版本均为 `1.5.22`。随后在临时 Git 项目运行固定版本安装，13 项均与当前仓库一致，且全局 Skill 文件前后哈希未变。

与此同时，8 月 8 日留下的 13 个全局副本与当前仓库均已出现差异，主要是后来补充的作者、分类和标签元数据，另有 3 项内容修订。它不代表 CLI 安装错误，只证明**安装后的文件不会随上游仓库持续同步**。排错或复现时应先记录 `npx skills --version`，必要时固定已知版本，并在确认来源后使用 CLI 的更新或重新安装流程；不要直接假定旧副本仍等于当前仓库。

同日在受控临时项目中，先保留公开仓库安装生成的 `skills-lock.json`，再把 13 个项目副本替换为历史提交 `5906879` 的完整文件夹。更新前 13 / 13 与当前仓库不同；运行 `npx --yes skills@1.5.22 update -p -y` 后，13 / 13 完整文件夹与当前仓库一致，全局文件哈希未变。这个结果只验证**有锁文件的项目级复制安装**，不证明全局 `update -g` 或无锁文件场景。

## 状态定义

- ✅ **已验证**：执行过对应检查，并保留了命令、日期和结果。
- ⚠️ **部分通过**：只有一部分行为得到验证，限制会写在表中。
- ❌ **失败**：已经复现不兼容或错误。
- ⏳ **待测**：没有足够证据。它不代表不兼容，也不代表通过。

## 下一轮测试

13 个原创 Skill 已各完成一次自动触发测试：10 项当次任务完成，1 项按流程等待必要输入，两个失败项完成缩小复测。下一步补 Claude Code / Cursor 的真实环境证据，并为大任务建立明确输出预算。

如果你能提供 Claude Code 或 Cursor 的实际结果，请用[结构化兼容性表单](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml)提交。表单会分别记录模型是否开始执行、是否点名 Skill、是否触发与任务是否完成；成功和失败都欢迎，但请先删除 Token、邮箱和私人路径。

希望用 PR 提交机器可读结果时，复制[真实示例报告](examples/compatibility-result.example.json)，按 [JSON Schema](schemas/compatibility-result.schema.json)填写，再运行：

```bash
python3 scripts/check_compatibility_report.py compatibility-reports/<id>.json
```

仓库校验器不依赖第三方 Python 包，并额外检查本仓库 Skill 名称、环境阻断与完成状态的一致性，以及常见敏感信息。它不是通用 JSON Schema 实现，也不能替代人工脱敏。
