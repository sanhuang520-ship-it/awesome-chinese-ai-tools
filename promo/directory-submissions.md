# Agent Skills 目录投稿队列

> 更新：2026-08-12。原则：逐个渠道提交，不群发，不要求互 Star；只投目录受众真正相关的 Skill。

## 1. agent-skills.md — 待提交确认

- 提交页：https://agent-skills.md/submit
- 目录说明：粘贴 GitHub 仓库或 `skills/` 目录 URL，站点自动解析有效 Skill。
- 待提交 URL：

```text
https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills
```

- 重复检查：2026-08-12 未检索到 `sanhuang520`、`awesome-chinese-ai-tools`。
- 证据边界：目录自动收录只代表解析成功，不代表目录方认证质量或跨客户端兼容。

## 2. kodustech/awesome-agent-skills — 待 GitHub CLI 认证

- 目标仓库：https://github.com/kodustech/awesome-agent-skills
- 目标分类：`Frontend Development`
- 只提交两个软件工程相关、已有 Codex 自动触发案例的 Skill：

```markdown
| [chinese-typography](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-typography) | Audit and fix CJK web typography, including font stacks, line height, line breaking, punctuation, mixed Chinese-English spacing, and accessible emphasis. |
| [github-readme-cn](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/github-readme-cn) | Audit Chinese GitHub repository presentation, README first-screen structure, real screenshots, topics, evidence claims, and conversion paths without promising Star growth. |
```

建议 PR 标题：

```text
Add two Chinese developer experience skills
```

建议 PR 正文：

```markdown
## What changed

Adds two Chinese-language software engineering skills to Frontend Development:

- `chinese-typography` for CJK web typography audits
- `github-readme-cn` for evidence-aware GitHub README audits

## Why

Both address developer experience gaps for Chinese projects and include explicit boundaries instead of broad compatibility or growth claims.

## Validation

- Each link points directly to a folder containing `SKILL.md` with `name` and `description` frontmatter.
- Both skills were observed auto-activating in one Codex task; those task-level results are documented in the source repository and are not presented as universal compatibility.
```

阻塞：专用 GitHub 发布流程要求 `gh auth status` 成功；当前本机 `gh` 未登录。

## 3. LINUX DO — 不由 AI 代发

社区规则明确禁止发布 AI 生成或润色的推广正文，并要求开源推广使用指定标签、原则上每周不超过一帖。因此只保留用户本人基于实际维护经历自行撰写的选项，不提供可直接粘贴的 AI 推广稿，也不自动发布。
