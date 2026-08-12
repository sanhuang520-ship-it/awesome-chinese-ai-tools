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

不需要 Fork 仓库或编辑 JSON，选一个表单填写即可：

- [推荐一个 Skill 或 AI 工具](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=add-entry.yml)
- [报告失效链接或事实错误](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=report-problem.yml)
- [提交一次成功、失败或未触发的兼容性实测](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml)

不知道的字段可以如实写“不确定”或“暂无”。维护者会复核，不要求提交者先得出完整结论；请不要为了填满表单而猜测。

---

## 分享一次真实使用结果（不需要提 PR）

如果你已经使用过某个 Skill，优先用[兼容性实测表单](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml)提交。它会要求客户端版本、原始任务、实际结果和证据边界；成功、失败和没有自动触发都欢迎。也可以在[置顶 Discussion](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/discussions/4)按下面的格式回复：

```markdown
### 使用的 Skill

### 环境与版本
<!-- Codex / Claude Code / Cursor；操作系统；能确认的版本 -->

### 我交给 AI 的任务

### 实际结果

### 有效的地方 / 需要改进的地方
```

提交前请删除 Token、邮箱、私人路径和未公开业务数据。维护者如需把案例整理进 README 或文档，会保留原讨论链接，并区分“用户反馈”与“已复核事实”。

---

## 提交前本地验证

仓库内的结构化数据、公开页面、站内链接、RSS、Sitemap 和证据边界可以用一条命令检查，不需要网络：

```bash
python3 scripts/verify.py
```

如果脚本报告公开元数据不同步，先运行 `python3 scripts/sync_public_metadata.py . --write`，检查变更后再重新验证。

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
