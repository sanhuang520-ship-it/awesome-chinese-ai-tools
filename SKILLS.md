# 🧩 AI Agent Skills 中文指南

> 给中文用户讲清楚：Skills 是什么、怎么装、哪些值得用
> 本页所有仓库链接均经过实际验证（GitHub API 实测存在），星数为查询时数据

---

## 目录

- [什么是 Skills](#什么是-skills)
- [Skills / MCP / 插件 有什么区别](#skills--mcp--插件-有什么区别)
- [怎么安装（实测有效）](#怎么安装实测有效)
- [官方 Skills（Anthropic 出品）](#官方-skillsanthropic-出品)
- [社区精选 Skills](#社区精选-skills)
- [Skills 资源大全](#skills-资源大全)
- [怎么自己写一个 Skill](#怎么自己写一个-skill)

---

## 什么是 Skills

**一句话：Skills 是给 AI 助手加的「专业技能包」。**

打个比方——AI 本身像个聪明的通才，但你让它做 PPT，它可能每次风格都不一样、也不知道你公司的规范。给它装一个 `pptx` skill，它就掌握了处理 PPT 的标准流程。

技术上，一个 Skill 就是**一个文件夹**，里面有个 `SKILL.md` 说明书，告诉 AI：
- 什么时候该用这个技能
- 用的时候按什么步骤做
- 有哪些参考资料和脚本可以调用

AI 会**自动判断**什么时候该激活哪个 skill，不需要你手动切换。

---

## Skills / MCP / 插件 有什么区别

| | 是什么 | 解决什么 | 举例 |
|---|--------|---------|------|
| **Skills** | 一份「工作说明书」（Markdown + 可选脚本） | 教 AI **怎么做**某类任务 | 做 PPT 的规范流程、写周报的模板 |
| **MCP** | 一个后台服务（Model Context Protocol） | 让 AI **连上**外部系统 | 读取数据库、操作浏览器、调用 API |
| **插件 / Plugin** | 打包分发的组合 | 把 skills + MCP 打包好一键装 | 某个产品的完整集成包 |

**简单记**：Skills 教「怎么做」，MCP 给「能做什么」的能力，插件是打包好的礼盒。

---

## 怎么安装（实测有效）

### Claude Code（命令行）

Skills 放在这个目录：

```bash
~/.claude/skills/
```

> ⚠️ **注意**：有些英文教程写的是 `~/.config/claude-code/skills/`，经实测在 macOS 上**实际生效的是 `~/.claude/skills/`**。以你机器上实际存在的目录为准。

安装步骤：

```bash
# 1. 确保目录存在
mkdir -p ~/.claude/skills/

# 2. 把 skill 文件夹放进去（以 git clone 为例）
cd ~/.claude/skills/
git clone https://github.com/anthropics/skills.git temp-skills
cp -r temp-skills/skills/pdf ./pdf
rm -rf temp-skills

# 3. 确认结构正确（必须有 SKILL.md）
ls ~/.claude/skills/pdf/
# 应该看到：SKILL.md  以及可能的 references/ scripts/ 等

# 4. 重启 Claude Code
claude
```

装好后**不用手动调用**——描述你的任务，AI 会自动判断该用哪个 skill。

### Claude.ai（网页版）

1. 在对话界面点击 🧩 技能图标
2. 从市场添加，或上传自定义 skill
3. AI 会根据任务自动激活

### 验证是否装好

```bash
# 看看装了哪些
ls ~/.claude/skills/

# 检查某个 skill 的说明是否正常
head ~/.claude/skills/pdf/SKILL.md
```

---

## 官方 Skills（Anthropic 出品）

来源：[anthropics/skills](https://github.com/anthropics/skills) ⭐166,200 —— 官方仓库，共 17 个

### 📄 文档办公

| Skill | 用途 |
|-------|------|
| [docx](https://github.com/anthropics/skills/tree/main/skills/docx) | Word 文档：创建、编辑、修订标记、批注、排版 |
| [pdf](https://github.com/anthropics/skills/tree/main/skills/pdf) | PDF：提取文字/表格/元数据、合并、批注 |
| [pptx](https://github.com/anthropics/skills/tree/main/skills/pptx) | PPT：读取、生成、调整版式和模板 |
| [xlsx](https://github.com/anthropics/skills/tree/main/skills/xlsx) | Excel：公式、图表、数据转换 |
| [doc-coauthoring](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring) | 文档协作撰写 |

### 💻 开发设计

| Skill | 用途 |
|-------|------|
| [web-artifacts-builder](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) | 构建复杂网页组件（React / Tailwind / shadcn-ui） |
| [frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | 前端设计规范 |
| [webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) | Web 应用测试 |
| [mcp-builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) | 构建 MCP 服务 |
| [claude-api](https://github.com/anthropics/skills/tree/main/skills/claude-api) | Claude API 使用参考 |
| [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | **写 skill 的 skill**（新手从这个开始） |

### 🎨 创意视觉

| Skill | 用途 |
|-------|------|
| [canvas-design](https://github.com/anthropics/skills/tree/main/skills/canvas-design) | 画布设计 |
| [algorithmic-art](https://github.com/anthropics/skills/tree/main/skills/algorithmic-art) | 算法生成艺术 |
| [theme-factory](https://github.com/anthropics/skills/tree/main/skills/theme-factory) | 主题配色生成 |
| [brand-guidelines](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines) | 品牌规范应用 |
| [slack-gif-creator](https://github.com/anthropics/skills/tree/main/skills/slack-gif-creator) | Slack GIF 制作 |

### 💼 办公协作

| Skill | 用途 |
|-------|------|
| [internal-comms](https://github.com/anthropics/skills/tree/main/skills/internal-comms) | 内部沟通文案 |

---

## 社区精选 Skills

> 以下描述取自各仓库自己的介绍，未做主观加工。

| Skill | 说明 |
|-------|------|
| [claude-epub-skill](https://github.com/smerchek/claude-epub-skill) | 把 Markdown 文档和对话总结转成专业 EPUB 电子书 |
| [aws-skills](https://github.com/zxkane/aws-skills) | AWS 开发：CDK 最佳实践、成本优化、Serverless 架构模式 |
| [master-claude-for-legal](https://github.com/sboghossian/master-claude-for-legal) | 法务团队技能包：NDA 审阅、多方版本对比、引用核验等 |

---

## Skills 资源大全

想找更多？这几个仓库是目前最全的（星数为实测数据）：

| 仓库 | ⭐ | 说明 |
|------|-----|------|
| [anthropics/skills](https://github.com/anthropics/skills) | 166,200 | **官方仓库**，质量最有保证 |
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | 91,811 | MCP 服务大全（连接外部系统） |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 81,564 | 生产级工程类 skills |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 71,763 | 社区精选列表，分类齐全 |

---

## 怎么自己写一个 Skill

**最简单的 Skill 就是一个文件夹 + 一份 SKILL.md：**

```
my-skill/
└── SKILL.md          # 必需
    references/       # 可选：参考资料
    scripts/          # 可选：脚本
```

`SKILL.md` 的基本结构：

```markdown
---
name: my-skill
description: 一句话说明什么时候该用这个技能（AI 靠这句判断是否激活）
---

# 我的技能

## 什么时候用
描述适用场景

## 怎么做
1. 第一步
2. 第二步
3. 第三步

## 注意事项
需要避免的坑
```

**关键点**：`description` 写得越准确，AI 越能在正确的时机激活它。

推荐用官方的 [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 来生成——它就是专门帮你写 skill 的 skill。

---

## ⚠️ 安全提醒

Skills 可以包含**可执行脚本**。安装第三方 skill 前：

1. **看一眼 SKILL.md 内容**，确认它做的事符合预期
2. **检查是否有 scripts/ 目录**，里面的脚本会被执行
3. 优先选择**官方仓库**或**星数高、有活跃维护**的来源
4. 不要安装来源不明的 skill

---

*本页由 [AI 工具导航](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/) 维护 · 信息有误欢迎 [提 Issue](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues)*
