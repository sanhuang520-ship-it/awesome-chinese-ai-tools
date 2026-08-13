# 贡献指南

参与 Issue、PR 与 Discussion 前，请遵守[社区行为规范](CODE_OF_CONDUCT.md)。我们欢迎成功、失败和不同意见，但不接受伪造实测、刷星、推广链接或人身攻击。

先说三条最容易白费功夫的：

| ⚠️ | 说明 |
|----|------|
| **收录内容改 `data/`** | `SKILLS.md` 由脚本重建；README 只自动同步数量、复检日期等公开统计。新增收录请改 `data/tools.json` 或 `data/skills.json` |
| **链接不能带推广参数** | `?from=` `?ref=` `utm_*` `aff` 之类一律不收。想被收录就给干净的官网链接 |
| **自己的产品要说明** | 提交自己做的东西完全可以，但请在 PR 里写一句「这是我做的」。不写而被发现，直接关闭 |

---

## 不会写代码，也可以贡献

如果不想先研究仓库结构，可以从[三个 10—20 分钟的真实维护任务](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/contribute/)里选一个。每项都给出操作范围、提交入口和完成标准。

不需要 Fork 仓库或编辑 JSON，选一个表单填写即可：

- [推荐一个 Skill 或 AI 工具](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=add-entry.yml)
- [报告失效链接或事实错误](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=report-problem.yml)
- [改进一个本站原创 Skill](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=improve-skill.yml)
- [提交一次成功、失败或未触发的兼容性实测](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml)
- [提交一次 Windows、WSL、Linux 或 macOS 安装环境复测](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=install-environment-result.yml)
- [提议一个现有四组未覆盖的中文 Skill 组合](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=request-bundle.yml)

不知道的字段可以如实写“不确定”或“暂无”。维护者会复核，不要求提交者先得出完整结论；请不要为了填满表单而猜测。

安装环境结果也可以通过 PR 留下机器可读记录：复制 [`examples/install-environment-result.example.json`](examples/install-environment-result.example.json)，按 [`schemas/install-environment-result.schema.json`](schemas/install-environment-result.schema.json) 填写，并运行：

```bash
python3 scripts/check_install_environment_report.py <report>.json
```

该记录只描述一次 CLI 安装尝试、版本、落盘路径与文件类型；自动触发和任务完成仍须用兼容性实测表单或报告单独记录。

如何选择：推荐新项目用“推荐”；链接、名称、数字或说明错误用“事实错误”；本站原创 Skill 已经触发但方法、边界、示例或交付需要改进，用“原创 Skill 改进”；是否被客户端自动读取或最终是否完成，用“兼容性实测”；有真实中文任务但现有四组开箱方案都不合适，用“组合需求”。

---

## 分享一次真实使用结果（不需要提 PR）

如果你已经使用过某个 Skill，优先用[兼容性实测表单](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml)提交。它会分别记录客户端版本、原始任务、是否点名 Skill、是否触发、任务是否完成、实际结果和证据边界；成功、失败和没有自动触发都欢迎。也可以在[置顶 Discussion](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/discussions/4)按下面的格式回复：

```markdown
### 使用的 Skill

### 环境与版本
<!-- Codex / Claude Code / Cursor；操作系统；能确认的版本 -->

### 我交给 AI 的任务

### 是否在任务里点名 Skill

### 实际结果

### 是否触发 / 是否完成

### 有效的地方 / 需要改进的地方
```

提交前请删除 Token、邮箱、私人路径和未公开业务数据。维护者如需把案例整理进 README 或文档，会保留原讨论链接，并区分“用户反馈”与“已复核事实”。

### 用 JSON 提交可自动检查的结果

准备提 PR 时，可以复制 [`examples/compatibility-result.example.json`](examples/compatibility-result.example.json)，按公开的 [`schemas/compatibility-result.schema.json`](schemas/compatibility-result.schema.json)填写，并保存为 `compatibility-reports/<id>.json`。示例取自仓库已经公开的真实复测，不是虚构的“理想输出”。

```bash
python3 scripts/check_compatibility_report.py compatibility-reports/<id>.json
```

JSON Schema 是跨工具的数据契约；上面的无第三方依赖校验器还会检查：Skill 是否属于本仓库维护范围、环境阻断是否被误写成任务完成，以及公开文本中常见的 Token、邮箱和私人路径。自动扫描不能代替人工脱敏，提交前仍需逐项阅读。

提交前也可运行 `python3 scripts/check_compatibility_reports.py`，一次检查目录中的全部 JSON，并在报错时标出文件名。通过只代表机器可检查的结构与一致性成立；维护者仍会人工核对来源、证据边界和脱敏情况。

## 更新社交分享图

`og.svg` 由已提交的目录与兼容性证据生成，不手工填写数量。统计变化后运行：

```bash
python3 scripts/generate_social_preview.py --write --png
python3 scripts/generate_social_preview.py --check
```

生成 PNG 需要本机安装 `rsvg-convert`；完整本地检查也会验证 SVG 是否与当前数据一致，以及 PNG 是否为 1200 × 630。

原创 Skill 说明页的 Open Graph、Twitter Card 和 JSON-LD 图片字段由脚本统一维护。新增或修改说明页标题、摘要、图片后运行：

```bash
python3 scripts/sync_social_cards.py --write
python3 scripts/sync_social_cards.py
```

---

## 提交前本地验证

仓库内的结构化数据、公开页面、站内链接、RSS、Sitemap 和证据边界可以用一条命令检查，不需要网络：

```bash
python3 scripts/verify.py
```

如果脚本报告公开元数据不同步，先运行 `python3 scripts/sync_public_metadata.py . --write`，检查变更后再重新验证。

维护者发布稳定版本后，可用 `python3 scripts/check_github_release.py` 只读核对：对应 tag 是否存在公开且非 prerelease 的 GitHub Release、标题与证据边界是否完整、tag 是否仍为 annotated tag。该检查不创建、修改或删除 Release。

复测 GitHub 仓库搜索发现性时，使用固定查询脚本，不要手工改变排序后与旧基线比较：

```bash
python3 scripts/capture_github_search.py --output metrics/YYYY-MM-DD-github-search.json
```

该脚本只读取公开仓库搜索和公开 Stars/Forks。排名会受索引、活跃度、Stars 与未知因素影响，不能把变化归因于一处 README 修改，也不能承诺涨星。

核对 GitHub 仓库 description、homepage 和 topics 是否与已提交定位一致：

```bash
python3 scripts/check_repository_profile.py
```

检查器只读取公开 API，不会修改仓库设置；期望值保存在 `data/repository-profile.json`。

---

## 加一个 Skill

下面是适合直接提 PR 的方式；如果不想改代码，使用上面的推荐表单即可。

编辑 **`data/skills.json`**，在 `skills` 数组里加一条：

```json
{
  "name": "skill-的目录名",
  "cat": "cn",
  "official": false,
  "desc": "一句话说明它做什么（中文）",
  "descEn": "原作者写的 description，从对方 SKILL.md 的 frontmatter 里取",
  "url": "https://github.com/owner/repo"
}
```

`cat` 可选：`cn` 中文条目（不代表原创归属） · `doc` 文档办公 · `dev` 开发工程 · `design` 创意设计 ·
`biz` 办公协作 · `data` 数据研究 · `sec` 安全取证 · `3d` 3D 与图形 · `game` 游戏开发

**收录标准：**

- 仓库里**必须有 `SKILL.md`**——只是个不错的项目但没有 SKILL.md 的，不算 skill
- 仓库真实存在且可访问（我们每天会自动复检，失效会标记）
- `desc` 要么译自原作者的 description，要么明确是你的理解。**不要看名字猜功能**
- `desc` / `descEn` 不写动态 Star 排名、借用上游 Star 数、Star 与安装量对比，或未经本站复现的百分比效果；提交前运行 `python3 scripts/check_catalog_claims.py`
- 名称、URL、描述会用于网站渲染：不要在名称或 URL 中加入引号、反引号或 HTML；描述中不要写 HTML 标签

## 加一个 AI 工具

编辑 **`data/tools.json`**。收录标准：

- 真实可用，非 Demo、非停更
- 核心功能基于 AI
- 有免费额度优先（纯付费需注明）
- 界面或内容支持中文（国际工具标 🌐）

## 报告失效链接

直接提 Issue，或者提 PR 改 `data/` 里对应条目。**发现事实错误请一定告诉我们**——
这个项目全部的价值就在"可信"两个字上。

---

## 不会收录的

- 已停服、停更的产品
- **带推广/追踪参数的链接**
- 仅有企业版、个人完全用不了的
- 纯英文且无中文支持计划的（除非是 Skills 生态里绕不开的）
- 没有 `SKILL.md` 却想进 skills 列表的

## 关于新闻

**本项目不转述任何 AI 新闻**，也不接受新闻类投稿。原因见 [CONTENT_POLICY.md](CONTENT_POLICY.md)。
