# Agent Skills 兼容性实测

> 最近实测：**2026-08-28**（skills CLI 全局更新）· 2026-08-26（Claude Code）· 2026-08-13（Codex） · 原始记录：[data/compatibility.json](data/compatibility.json) · 汇总校验：[scripts/check_compatibility.py](scripts/check_compatibility.py) · 单次报告规范：[JSON Schema](schemas/compatibility-result.schema.json)

本页只记录实际拿到的证据。**能被 CLI 发现、文件安装成功、AI 自动触发、最终任务完成，是四件不同的事。** 没运行过的客户端明确标为“待测”，不把格式兼容写成实测通过。

## 当前结论

| 检查项 | 结果 | 证据边界 |
|---|---|---|
| `skills` CLI 发现本站原创 Skill | ✅ 13 / 13 | `npx skills@1.5.22 add . --list` 找到 13 个 Skill |
| Codex 隔离项目安装内容 | ✅ 13 / 13 | `skills@1.5.22 --copy` 安装至临时 Git 项目的 `.agents/skills/`，与当前仓库逐字节一致；[查看复测记录](cases/skills-cli-isolated-install-2026-08-13.md) |
| 项目级旧副本更新 | ✅ 13 / 13 | 受控历史夹具中的 13 个完整 Skill 文件夹经 `skills@1.5.22 update -p -y` 更新后均与当前仓库一致；全局文件未改变 |
| 既有全局安装副本 | ⚠️ 曾 0 / 13，08-28 重装后 13 / 13 | 8 月 8 日安装后仓库又有修订，且 `update -g` 看不见无锁条目的副本；重新安装才追平。安装不是持续同步，不能把旧副本当成当前版本 |
| Codex 自动触发 | ⚠️ 13 / 13 | 10 项当次任务完成；1 项按流程等待必要输入；2 项大任务失败后通过缩小复测 |
| Claude Code 发现本站原创 Skill | ✅ 13 / 13 | 13 个全部出现在会话可用 Skill 列表中；[查看记录](cases/claude-code-13-skills-2026-08-26.md) |
| Claude Code 加载与路径解析 | ✅ 13 / 13 | 13 个全部加载成功，`base directory` 正确解析到 `~/.claude/skills/<name>` |
| Claude Code 任务覆盖 | ✅ 13 / 13 | 用自然措辞、不点名 Skill 撰写任务，按输出内容判定。首轮 12/13（`guofeng-threejs` 副本过期）；08-28 副本追平后 7 项全部重跑，13 / 13 |
| Claude Code 自动触发 | ⏳ 未记录 | **本轮是自测，不构成独立证据**，详见下方说明 |
| 全局 `update -g`（**有**锁条目） | ✅ 正确拉取上游新版 | 上游改动 `github-readme-cn` 后运行，本机 176 → 181 行、内容与仓库逐字节一致、锁条目 hash 同步更新 |
| 全局 `update -g`（**无**锁条目） | ❌ **静默跳过，不提示** | 同一命令对 7 个无锁条目的 Skill 只字未提、退出码 0；[查看记录](cases/skills-cli-global-update-2026-08-28.md) |
| Cursor | ⏳ 待测 | 当前没有运行 Cursor，不能声称通过 |

当前任务级案例记录的客户端为 Codex CLI `0.147.0-alpha.6.5`；这仍不代表其他 Codex 版本或任务措辞会得到相同结果。安装复测与任务级自动触发是两轮不同证据，不能互相替代。

### 为什么 Claude Code 那轮不记「自动触发」

Codex 那轮的触发证据，是 Codex 在提示词从未出现 Skill 名称的情况下**自己声明**
「我会用『chinese-typography』规范做纯审查」并读取了对应文件——那是可以从外部观察的第三方行为。

Claude Code 通过工具按名称调用 Skill，**选择调用哪个 Skill 的模型，与撰写任务措辞、
判定结果的模型是同一个**。因此本轮虽然 13 个都被正确选中，但这不与 Codex 那轮同级，
本页不把它记为自动触发通过。

能够独立观察、不依赖判断的是另外两件事：Skill 是否出现在客户端会话列表里，
以及能否被加载、路径能否正确解析。这两项按 ✅ 记录。

要取得与 Codex 同级的证据，需要由不知情的执行者做盲测——这是下一轮要补的。

另有 6 条运行前公开任务与成功门槛的前瞻复测，现已全部执行：初次 4 条通过 4 / 4；`chinese-web-themes` 因遗漏授权检查、`guofeng-threejs` 因超过 300 字限制，各记为 3 / 4 失败。随后只针对失败原因修改 Skill 指令，并以完全相同的原始任务复测，两项均通过 4 / 4（Three.js 响应实测 294 字符）。[主题修复记录](cases/chinese-web-themes-remediation-retest-2026-08-13.md)与 [Three.js 修复记录](cases/guofeng-threejs-remediation-retest-2026-08-13.md)不会覆盖首次失败。这组结果不改写上表的首次自动触发 10 / 1 / 2 统计。

## 13 个本站原创 Skill

| Skill | CLI 发现 | 隔离安装内容 | Codex 触发 | Claude Code | Cursor |
|---|---:|---:|---:|---:|---:|
| [`ai-learning-coach`](cases/ai-learning-coach-codex.md) | ✅ | ✅ | ⚠️¹ | ✅² | ⏳ |
| [`book-digest-cn`](cases/book-digest-cn-codex.md) | ✅ | ✅ | ✅¹ | ✅² | ⏳ |
| [`bookkeeping-cn`](cases/bookkeeping-cn-codex.md) | ✅ | ✅ | ✅¹ | ✅² | ⏳ |
| [`chinese-design-md`](cases/chinese-design-md-codex.md) | ✅ | ✅ | ✅¹ | ✅² | ⏳ |
| [`chinese-lesson-plan`](cases/chinese-lesson-plan-codex.md) | ✅ | ✅ | ⚠️¹ | ✅² | ⏳ |
| [`chinese-typography`](cases/chinese-typography-codex.md) | ✅ | ✅ | ✅¹ | ✅² | ⏳ |
| [`chinese-web-themes`](cases/chinese-web-themes-codex.md) | ✅ | ✅ | ✅¹ | ✅² | ⏳ |
| [`chinese-work-report`](cases/chinese-work-report-codex.md) | ✅ | ✅ | ✅¹ | ✅² | ⏳ |
| [`ecommerce-copywriting`](cases/ecommerce-copywriting-codex.md) | ✅ | ✅ | ✅¹ | ✅² | ⏳ |
| [`github-readme-cn`](cases/github-readme-cn-codex.md) | ✅ | ✅ | ✅¹ | ✅² | ⏳ |
| [`guochao-visual-cn`](cases/guochao-visual-cn-codex.md) | ✅ | ✅ | ✅¹ | ✅² | ⏳ |
| [`guofeng-threejs`](cases/guofeng-threejs-codex.md) | ✅ | ✅ | ⚠️¹ | ✅² | ⏳ |
| [`homework-tutor-cn`](cases/homework-tutor-cn-codex.md) | ✅ | ✅ | ✅¹ | ✅² | ⏳ |

¹ 仅代表链接案例中的单任务、单客户端版本结果；⚠️ 包括等待用户补充，或大任务失败后仅通过缩小复测。

² Claude Code 一列表示**发现 + 加载 + 任务覆盖**三项，[记录在此](cases/claude-code-13-skills-2026-08-26.md)；**不含自动触发**（原因见上文）。首轮 `guofeng-threejs` 记 ⚠️（本机副本早于一次技法修订）；2026-08-28 副本追平后重跑，改记 ✅。

### 本轮发现的客户端限制

Codex 在隔离实测中报告：已安装 Skill 较多时，会为适应 skills 上下文预算而缩短部分 description。`chinese-typography` 本次仍然正确触发，但这条告警可能影响其他 Skill 的发现，因此后续测试会同时记录触发成功与未触发结果。

### 安装不是自动更新

2026-08-13 复查时，未固定版本的 `npx skills --version` 命中了本机旧缓存 `1.5.18`，而 npm `latest` 与本轮固定复测版本均为 `1.5.22`。随后在临时 Git 项目运行固定版本安装，13 项均与当前仓库一致，且全局 Skill 文件前后哈希未变。

与此同时，8 月 8 日留下的 13 个全局副本与当前仓库均已出现差异，主要是后来补充的作者、分类和标签元数据，另有 3 项内容修订。它不代表 CLI 安装错误，只证明**安装后的文件不会随上游仓库持续同步**。排错或复现时应先记录 `npx skills --version`，必要时固定已知版本，并在确认来源后使用 CLI 的更新或重新安装流程；不要直接假定旧副本仍等于当前仓库。

同日在受控临时项目中，先保留公开仓库安装生成的 `skills-lock.json`，再把 13 个项目副本替换为历史提交 `5906879` 的完整文件夹。更新前 13 / 13 与当前仓库不同；运行 `npx --yes skills@1.5.22 update -p -y` 后，13 / 13 完整文件夹与当前仓库一致，全局文件哈希未变。这个结果只验证**有锁文件的项目级复制安装**，不证明全局 `update -g` 或无锁文件场景。

2026-08-28 补上了全局场景的实测，结论是**否定的**：`skills@1.5.23` 的 `update -g` 只处理
`~/.agents/.skill-lock.json` 里有条目的 Skill。本机 13 个全局副本中有 7 个没有锁条目，
命令输出「✓ Updated 22 skill(s)」、退出码 0，却对这 7 个只字未提，哈希 13/13 全部未变。
它们自 2026-08-08 起静默过期 20 天，期间每次 update 都返回成功。

后果不止于版本不齐：`guofeng-threejs` 的旧副本仍在推荐已被本仓库推翻的 Sobel 描边方案，
**使用者运行 update、看到绿勾、继续拿到错的建议**。改用逐个 `add --skill <name> -g`
重新安装后，7/7 补上锁条目、13/13 内容追平。[完整记录](cases/skills-cli-global-update-2026-08-28.md)

同日稍后补上了这条路径：先改动上游的 `github-readme-cn`（176 → 181 行）并推送，
再运行同一条 `update -g`。判定标准在运行前定死：文件行数、是否含新增段落、
文件 sha、锁条目 hash 四项都要变。结果**四项全变**，内容与仓库逐字节一致。

**所以这个失败是有条件的，不是 `update` 整体坏掉**：有锁条目就能正确拉取，
没有锁条目才会被静默跳过。这个对比也让「补锁条目」成为明确可行的修复手段。

⚠️ 一个未能解释的观察：那次运行还报告更新了 `guofeng-threejs` 与 `homework-tutor-cn`，
但这两个自 08-28 重装以来上游并无改动；而处境完全相同的 `bookkeeping-cn`、
`chinese-design-md`（上游同样停在 08-21、同样 08-28 重装）却未被触及。
内容上无影响（事后 13/13 仍与仓库逐字节一致）。**原因未查明，此处只记录现象，不给解释。**

## 状态定义

- ✅ **已验证**：执行过对应检查，并保留了命令、日期和结果。
- ⚠️ **部分通过**：只有一部分行为得到验证，限制会写在表中。
- ❌ **失败**：已经复现不兼容或错误。
- ⏳ **待测**：没有足够证据。它不代表不兼容，也不代表通过。

## 下一轮测试

13 个原创 Skill 已各完成一次自动触发测试：10 项当次任务完成，1 项按流程等待必要输入，两个失败项完成缩小复测。Claude Code 已于 2026-08-26 补上发现、加载与任务覆盖的证据，但自动触发仍缺同级证据（需盲测）。本机副本已于 2026-08-28 全部追平，7 项也已在当前版本上重跑完毕（13/13）。「有锁条目 + 上游有新提交」这条路径已于同日验证通过。下一步：① 由不知情执行者做盲测，取得与 Codex 同级的触发证据 ② 查明上述「无上游改动却被报告更新」的原因 ③ 补 Cursor。

如果你能提供 Claude Code 或 Cursor 的实际结果，请用[结构化兼容性表单](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml)提交。表单会分别记录模型是否开始执行、是否点名 Skill、是否触发与任务是否完成；成功和失败都欢迎，但请先删除 Token、邮箱和私人路径。

希望用 PR 提交机器可读结果时，复制[真实示例报告](examples/compatibility-result.example.json)，按 [JSON Schema](schemas/compatibility-result.schema.json)填写，再运行：

```bash
python3 scripts/check_compatibility_report.py compatibility-reports/<id>.json
```

仓库校验器不依赖第三方 Python 包，并额外检查本仓库 Skill 名称、环境阻断与完成状态的一致性，以及常见敏感信息。它不是通用 JSON Schema 实现，也不能替代人工脱敏。
