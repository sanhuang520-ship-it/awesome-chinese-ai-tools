# 贡献指南

先说三条最容易白费功夫的：

| ⚠️ | 说明 |
|----|------|
| **别改 README.md 和 SKILLS.md** | 这两个文件**每天由脚本从 `data/` 重新生成**，直接改会被覆盖。改 `data/tools.json` 或 `data/skills.json` |
| **链接不能带推广参数** | `?from=` `?ref=` `utm_*` `aff` 之类一律不收。想被收录就给干净的官网链接 |
| **自己的产品要说明** | 提交自己做的东西完全可以，但请在 PR 里写一句「这是我做的」。不写而被发现，直接关闭 |

---

## 加一个 Skill

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

`cat` 可选：`cn` 中文原创 · `doc` 文档办公 · `dev` 开发工程 · `design` 创意设计 ·
`biz` 办公协作 · `data` 数据研究 · `sec` 安全取证 · `3d` 3D 与图形 · `game` 游戏开发

**收录标准：**

- 仓库里**必须有 `SKILL.md`**——只是个不错的项目但没有 SKILL.md 的，不算 skill
- 仓库真实存在且可访问（我们每天会自动复检，失效会标记）
- `desc` 要么译自原作者的 description，要么明确是你的理解。**不要看名字猜功能**

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
