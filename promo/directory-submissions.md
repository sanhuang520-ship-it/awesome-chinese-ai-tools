# Agent Skills 发现渠道账本

> 更新：2026-08-13。原则：先查重、再核对规则、逐个提交；不群发、不互 Star、不把目录收录称作质量认证。外部表单、Fork 和 PR 都需要发布时确认，本文件只记录证据与可用草稿。

## 已完成并验证

### 1. Agent-Skills.md

- 状态：**已提交、已收录、已验证**。
- 作者页：https://agent-skills.md/authors/sanhuang520-ship-it
- 2026-08-13 验证：页面能找到 `sanhuang520-ship-it`，并展示 `chinese-typography`、`github-readme-cn` 等全部 13 个本站原创 Skill。
- 边界：自动解析成功不代表目录方完成内容审核、安全认证或跨客户端兼容测试。
- 下一步：不重复提交；只有 Skill 增删或页面缺失时再处理。

### 2. skills.sh

- 状态：**已索引、README 已公开说明**。
- 仓库页：https://skills.sh/sanhuang520-ship-it/awesome-chinese-ai-tools
- 边界：平台展示的聚合安装次数可能包含维护者安装核验，不等于独立用户、实际效果或质量认证。
- 下一步：不重复提交；只在索引缺失或名称错误时报告。

## 可考虑，但发布前仍需确认

### 3. kodustech/awesome-agent-skills

- 仓库：https://github.com/kodustech/awesome-agent-skills
- 2026-08-13 只读核验：95 Stars、74 Forks、未归档；最近一次检索到的合并发生在 2026-06-28；候选名称没有重复，但当前约有 39 个开放 PR。
- 当前 README 的 Frontend Development 已收录通用 `web-typography-skill`，因此 `chinese-typography` 存在主题重叠，不能用“又一个排版 Skill”作为理由。
- 决策：**暂不提交**。只有在 PR 能用 CJK 特有问题证明明显差异（CJK 断行、全角标点、中英混排、中文字体栈），且用户确认愿意创建 Fork/PR 时再行动。

若决定提交，严格只投一个 Skill：

```markdown
| [chinese-typography](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-typography) | Audit CJK-specific typography: line breaking, full-width punctuation, Chinese font stacks, mixed Chinese-English spacing, and accessible emphasis. |
```

建议 PR 标题：

```text
Add CJK-specific typography audit skill
```

建议 PR 正文：

```markdown
## What changed

Adds `chinese-typography` to Frontend Development.

## Why it is distinct

The list already includes a general web typography skill. This contribution is limited to CJK-specific behavior: Chinese line breaking, full-width punctuation, Chinese font stacks, mixed Chinese-English spacing, and emphasis conventions.

## Validation and boundaries

- The link points directly to a public folder containing `SKILL.md` with `name` and `description` frontmatter.
- The repository records one natural-language Codex activation task and publishes the task-level evidence.
- That observation is not presented as universal compatibility or a quality certification.
- License: MIT.
```

## 暂缓或不投入

### VoltAgent/awesome-agent-skills — 暂缓

- 2026-08-13 只读核验：约 3 万 Stars，仓库活跃，未检索到 `chinese-typography` 同名项。
- 官方贡献要求写明：Skill 必须已有“real community usage”，且新 Skill 应先成熟再提交。
- 当前证据只有仓库自测、聚合 Traffic/Clone 与 7 Stars；Clone 不能叫用户，也不能证明社区采用。
- 解锁条件：至少出现可公开、可复核的独立用户使用报告，再重新评估；不为了进高星目录夸大采用情况。

### SkillMD.ai — 暂缓

- 提交表单要求邮箱并宣称未来创作者奖励；当前没有足够理由发送维护者个人信息。
- 解锁条件：先确认隐私政策、审核机制与实际目录流量，再由用户决定是否提交邮箱。

### OmniSkill / 新建小目录 — 不投入

- 2026-08-13 搜索结果中的 OmniSkill 页面显示 0 个 Skill；`appssemble/awesome-skill-md` 当日公开数据仅 2 Stars。
- 决策：发现价值尚未建立，不花时间批量提交。

### LINUX DO — 不由 AI 代发

社区规则明确禁止发布 AI 生成或润色的推广正文，并要求开源推广使用指定标签、原则上每周不超过一帖。因此只保留用户本人基于实际维护经历自行撰写的选项，不提供可直接粘贴的 AI 推广稿，也不自动发布。

## 每次外部发布后的记录

记录平台、URL、时间、标题版本，以及发布后 24 小时和 72 小时的滚动 Traffic、热门来源与 Stars。只能写“发布后观察到”，不能直接归因；不同快照窗口可能重叠，也不能把 Clone 换算为用户或 Star 转化率。
