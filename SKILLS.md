# 🧩 AI Agent Skills 中文合集

> **87 个 Skill，其中 30 个中文原创** —— 每一个都经 GitHub API 验证仓库真实存在
> 在线浏览（可搜索/筛选）：https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/ → 点「🧩 Skills」

---

## 什么是 Skills

**一句话：Skills 是给 AI 助手加的「专业技能包」。**

技术上就是**一个文件夹**，里面有个 `SKILL.md` 说明书，告诉 AI：什么时候该用、按什么步骤做、有哪些参考资料。
AI 会**自动判断**何时激活，不需要手动切换。

| | 是什么 | 解决什么 |
|---|--------|---------|
| **Skills** | 一份工作说明书（Markdown + 可选脚本） | 教 AI **怎么做**某类任务 |
| **MCP** | 一个后台服务 | 让 AI **连上**外部系统（数据库、浏览器） |
| **插件** | 打包分发的组合 | 把 skills + MCP 打包一键装 |

---

## 怎么安装

### 方式一：一键安装（推荐）

```bash
npx skills add <GitHub 仓库地址>
```

### 方式二：手动放置

```bash
mkdir -p ~/.claude/skills/
# 把 skill 文件夹放进去，确认里面有 SKILL.md
ls ~/.claude/skills/<skill-name>/
```

> ⚠️ **实测提醒**：部分英文教程（包括一些高星仓库）写的安装路径是 `~/.config/claude-code/skills/`，
> 经本机实测，macOS 上**实际生效的是 `~/.claude/skills/`**。以你机器上实际存在的目录为准。

装好后重启 Claude Code 即可，**无需手动调用**——描述任务，AI 自动激活。

---

## Skill 清单


### 🇨🇳 中文原创（30 个）

| Skill | 星数 | 说明 |
|-------|------|------|
| [superpowers-zh](https://github.com/jnMetaCode/superpowers-zh) | ⭐7,458 | superpowers 中文版：26万⭐框架完整汉化 + 6 个中国原创 skill |
| [codex-claude-academic-skills](https://github.com/zLanqing/codex-claude-academic-skills) | ⭐2,556 | 学术科研三件套：文献阅读、论文写作、科学计算全流程 |
| [everything-claude-code-zh](https://github.com/xu-xiang/everything-claude-code-zh) | ⭐1,807 | Claude Code 完整配置中文翻译（agents/skills/hooks/commands） |
| [agent-skills-with-anthropic](https://github.com/datawhalechina/agent-skills-with-anthropic) | ⭐1,435 | 吴恩达 DeepLearning.AI 课程的中文翻译与知识整理 |
| [shuorenhua](https://github.com/MrGeDiao/shuorenhua) | ⭐928 | 「说人话」去 AI 味改写：保事实、分场景、改完可直接发 |
| [Awesome-Journal-Skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills) | ⭐909 | 主流期刊投稿技能包（AER、QJE 等经济学顶刊） |
| [speak-human-tw](https://github.com/Raymondhou0917/speak-human-tw) | ⭐744 | 繁体中文去 AI 味：抓 38 种 AI 写作痕迹，校正用语与标点 |
| [claude-code-skills-zh](https://github.com/laolaoshiren/claude-code-skills-zh) | ⭐725 | 面向中文开发者的技能库，按场景分类、复制即装 |
| [higgsfield-seedance2-jineng](https://github.com/beshuaxian/higgsfield-seedance2-jineng) | ⭐722 | AI 视频生成 15 个 prompt skill（Seedance 2.0 × Higgsfield） |
| [xiaohu-wechat-format](https://github.com/xiaohuailabs/xiaohu-wechat-format) | ⭐679 | 公众号一键排版发布：Markdown → 微信 HTML，30 套主题 |
| [Claude_skills_zh-CN](https://github.com/LeastBit/Claude_skills_zh-CN) | ⭐557 | 官方 anthropics/skills 的中文学习版 |
| [cuimao-translator](https://github.com/Cuimao777/cuimao-translator) | ⭐459 | 一键把英文 PDF 翻译成流畅中文 |
| [video-recap-skills](https://github.com/worldwonderer/video-recap-skills) | ⭐438 | 把任意视频剪成解说式短片 |
| [yupi-skill](https://github.com/liyupi/yupi-skill) | ⭐403 | 程序员鱼皮技能包：编程学习、求职面试、技术选型、创业经验 |
| [docx-skill-4-cn-paper](https://github.com/Gostyan/docx-skill-4-cn-paper) | ⭐348 | 中文论文排版规范：课程论文、数模竞赛、毕业论文 |
| [xiaohongshu-skills](https://github.com/vivy-yi/xiaohongshu-skills) | ⭐346 | 139 个小红书运营技能：内容创作、账号运营、电商转化等 9 大类 |
| [opencode-skills](https://github.com/zrt-ai-lab/opencode-skills) | ⭐263 | 技能库：视频生成、图片生成、Agent 互联、智能问数 |
| [universal-examprep-skill](https://github.com/ZeKaiNie/universal-examprep-skill) | ⭐263 | 考前突击教练：把课件资料变成应试重点 |
| [skills_collection](https://github.com/wwwzhouhui/skills_collection) | ⭐257 | 个人实用技能集，覆盖开发效率与内容创作 |
| [humanizer-zh-academic](https://github.com/redbaronyyyyy-eng/humanizer-zh-academic) | ⭐234 | 降低中文学术写作 AIGC 检测率 |
| [awesome-skills-cn](https://github.com/lingxling/awesome-skills-cn) | ⭐224 | 热门 Skills 中文学习版 + 教程，7000+ 收录 |
| [niubiskill](https://github.com/nathanskill/niubiskill) | ⭐208 | 中文变现决策：判断一件事是否接近收入再投入 |
| [Vibe_coding_guide](https://github.com/Lling0000/Vibe_coding_guide) | ⭐205 | 中文优先的 Vibe Coding 工程化流程指南 |
| [technical-writing](https://github.com/luoling8192/technical-writing) | ⭐204 | 中文技术写作：设计文档、评审稿、复盘、分享稿 |
| [SecSkills](https://github.com/Arenbai/SecSkills) | ⭐200 | 渗透测试技能模块，遵循 PTES 标准全阶段覆盖 |
| [makeownsrt](https://github.com/joshhu/makeownsrt) | ⭐175 | 从 MKV 提取英文字幕并翻成繁中双语 SRT |
| [Auto-CV](https://github.com/flamingoTOM/Auto-CV) | ⭐163 | LaTeX 中文简历模板 + 自动提取内容生成 |
| [JobOK](https://github.com/GresonKwan/JobOK) | ⭐115 | 中文求职：优势挖掘、岗位匹配、简历优化、面试训练 |
| [wechat-writing-style](https://github.com/yaoleifly/wechat-writing-style) | ⭐73 | 微信公众号中文写作风格 |
| [refine-legal-chinese](https://github.com/katejianglaw/refine-legal-chinese) | ⭐13 | 法言法语：把口语化表述改写为规范法律中文 |


### 📄 文档办公（9 个）

| Skill | 星数 | 说明 |
|-------|------|------|
| [NotebookLM Integration](https://github.com/PleasePrompto/notebooklm-skill) | ⭐7,566 | 让 Claude Code 直接对话 NotebookLM，做有出处的问答 |
| [article-extractor](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/article-extractor) | ⭐511 | 从网页提取完整文章正文与元数据 |
| [Markdown to EPUB Converter](https://github.com/smerchek/claude-epub-skill) | ⭐147 | 把 Markdown 文档转成专业 EPUB 电子书 |
| [Master Claude for Legal](https://github.com/sboghossian/master-claude-for-legal) | ⭐52 | 法务技能包：NDA 审阅、多方版本对比、引用核验 |
| [doc-coauthoring](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring) | 官方 | 结构化文档协作撰写流程，引导多人共同完成文档 |
| [docx](https://github.com/anthropics/skills/tree/main/skills/docx) | 官方 | Word 文档全流程：创建、读取、编辑、修订标记、批注、排版 |
| [pdf](https://github.com/anthropics/skills/tree/main/skills/pdf) | 官方 | PDF 处理：提取文字/表格/元数据、合并、拆分、批注 |
| [pptx](https://github.com/anthropics/skills/tree/main/skills/pptx) | 官方 | PPT 演示文稿：读取、生成幻灯片、调整版式与模板 |
| [xlsx](https://github.com/anthropics/skills/tree/main/skills/xlsx) | 官方 | Excel 表格：公式计算、图表生成、数据转换 |


### 💻 开发工程（20 个）

| Skill | 星数 | 说明 |
|-------|------|------|
| [finishing-a-development-branch](https://github.com/obra/superpowers/tree/main/skills/finishing-a-development-branch) | ⭐266,215 | 开发分支收尾：合并、清理、发布的标准流程 |
| [test-driven-development](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) | ⭐266,215 | 测试驱动开发全流程指导，写代码前先写测试 |
| [using-git-worktrees](https://github.com/obra/superpowers/blob/main/skills/using-git-worktrees/) | ⭐266,215 | 自动创建隔离的 git worktree，多分支并行开发不打架 |
| [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) | ⭐14,697 | 把任意文档网站自动转成 Claude Skill —— 造 skill 的利器 |
| [reddit-fetch](https://github.com/ykdojo/claude-code-tips/tree/main/skills/reddit-fetch) | ⭐9,539 | 当 WebFetch 被拦时，通过 Gemini CLI 抓取 Reddit 内容 |
| [lean-ctx](https://github.com/yvgude/lean-ctx) | ⭐3,487 | AI 编程代理的上下文运行时，管理会话与上下文 |
| [Playwright Browser Automation](https://github.com/lackeyjb/playwright-skill) | ⭐2,971 | 用 Playwright 做浏览器自动化测试与验证 |
| [prompt-engineering](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/customaize-agent/skills/prompt-engineering) | ⭐1,299 | 系统讲解提示词工程的技巧与模式 |
| [software-architecture](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/ddd/skills/software-architecture) | ⭐1,299 | 实现整洁架构、SOLID 等设计模式 |
| [subagent-driven-development](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/sadd/skills/subagent-driven-development) | ⭐1,299 | 把任务拆给多个子智能体并行处理，加速复杂开发 |
| [iOS Simulator](https://github.com/conorluddy/ios-simulator-skill) | ⭐1,199 | 操作 iOS 模拟器做 App 测试 |
| [aws-skills](https://github.com/zxkane/aws-skills) | ⭐342 | AWS 开发：CDK 最佳实践、成本优化、Serverless 架构 |
| [D3.js Visualization](https://github.com/chrisvoncsefalvay/claude-d3js-skill) | ⭐217 | 用 D3 做交互式数据可视化图表 |
| [great_cto](https://github.com/avelikiy/great_cto) | ⭐73 | 7 个专业子智能体（技术负责人、资深工程师等）组成的技术团队 |
| [claude-api](https://github.com/anthropics/skills/tree/main/skills/claude-api) | 官方 | Claude API 使用参考：模型 ID、定价、参数、流式、工具调用、缓存 |
| [frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | 官方 | 前端视觉设计指导，做出有辨识度、有意图的界面 |
| [mcp-builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) | 官方 | 构建高质量 MCP（Model Context Protocol）服务的完整指南 |
| [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | 官方 | 写 Skill 的 Skill —— 创建、改进、评估技能，新手从这个开始 |
| [web-artifacts-builder](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) | 官方 | 构建复杂多组件网页应用（React / Tailwind / shadcn-ui 技术栈） |
| [webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) | 官方 | 本地 Web 应用的交互测试工具集 |


### 🎨 创意设计（10 个）

| Skill | 星数 | 说明 |
|-------|------|------|
| [youtube-transcript](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/youtube-transcript) | ⭐511 | 抓取 YouTube 视频字幕并整理成摘要 |
| [imagen](https://github.com/sanjay3290/ai-skills/tree/main/skills/imagen) | ⭐364 | 调用 Google Gemini 图像生成 API 出图 |
| [swiftui-design-skill](https://github.com/wholiver/swiftui-design-skill) | ⭐163 | SwiftUI 前端设计（中文）：反 AI 味六条铁律、设计顾问、五维评审 |
| [anydesign](https://github.com/uxKero/anydesign) | ⭐150 | 分析任意图片/网址/Figma 文件，生成结构化设计规范 |
| [pakco-html](https://github.com/pakco77/pakco-html) | ⭐64 | HTML 审美库（中文）：60+ 视觉风格、演示页/长页模板，一键复制 Prompt |
| [algorithmic-art](https://github.com/anthropics/skills/tree/main/skills/algorithmic-art) | 官方 | 用 p5.js 创作算法艺术，支持随机种子与交互 |
| [brand-guidelines](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines) | 官方 | 把品牌配色与字体规范应用到各类产出物 |
| [canvas-design](https://github.com/anthropics/skills/tree/main/skills/canvas-design) | 官方 | 用设计原理创作视觉作品，输出 PNG / PDF |
| [slack-gif-creator](https://github.com/anthropics/skills/tree/main/skills/slack-gif-creator) | 官方 | 制作适配 Slack 的动图 GIF |
| [theme-factory](https://github.com/anthropics/skills/tree/main/skills/theme-factory) | 官方 | 为作品套用主题配色的工具集（幻灯片、网页等） |


### 💼 办公协作（9 个）

| Skill | 星数 | 说明 |
|-------|------|------|
| [brainstorming](https://github.com/obra/superpowers/tree/main/skills/brainstorming) | ⭐266,215 | 把粗略想法通过结构化提问变成完整方案 |
| [kaizen](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/kaizen/skills/kaizen) | ⭐1,299 | 持续改进方法论，多种分析框架 |
| [Brand Build Skills](https://github.com/rampstackco/claude-skills) | ⭐515 | 59 个 skill 的品牌与网站全生命周期库 |
| [ship-learn-next](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/ship-learn-next) | ⭐511 | 基于进展帮你决定下一步该做什么/学什么 |
| [tapestry](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/tapestry) | ⭐511 | 把相关文档互联并总结成知识网络 |
| [n8n-skills](https://github.com/haunchen/n8n-skills) | ⭐381 | 让 AI 直接理解和操作 n8n 工作流 |
| [google-workspace-skills](https://github.com/sanjay3290/ai-skills/tree/main/skills) | ⭐364 | Google 全家桶集成：Gmail、日历、Chat 等 |
| [solo-skills](https://github.com/rockscy/solo-skills) | ⭐6 | 独立开发者双语（中英）技能包：7 个 solo 场景 |
| [internal-comms](https://github.com/anthropics/skills/tree/main/skills/internal-comms) | 官方 | 撰写各类内部沟通文案的资源集 |


### 📊 数据研究（5 个）

| Skill | 星数 | 说明 |
|-------|------|------|
| [root-cause-tracing](https://github.com/obra/superpowers/tree/main/skills/root-cause-tracing) | ⭐266,215 | 错误深藏在执行链路时，追溯根本原因 |
| [CSV Data Summarizer](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill) | ⭐442 | 自动分析 CSV 文件并生成完整数据报告 |
| [deep-research](https://github.com/sanjay3290/ai-skills/tree/main/skills/deep-research) | ⭐364 | 调用 Gemini Deep Research 做自主多步研究 |
| [postgres](https://github.com/sanjay3290/ai-skills/tree/main/skills/postgres) | ⭐364 | 对 PostgreSQL 执行安全的只读 SQL 查询 |
| [recursive-research](https://github.com/Anjos2/recursive-research) | ⭐37 | 跨领域递归研究，可深入到博士级别 |


### 🔐 安全取证（4 个）

| Skill | 星数 | 说明 |
|-------|------|------|
| [computer-forensics](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/computer-forensics) | ⭐656 | 数字取证分析与调查技术 |
| [file-deletion](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/file-deletion) | ⭐656 | 安全删除文件与数据清除方法 |
| [metadata-extraction](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/metadata-extraction) | ⭐656 | 提取分析文件元数据用于取证 |
| [FFUF Web Fuzzing](https://github.com/jthack/ffuf_claude_skill) | ⭐204 | 集成 ffuf 做 Web 模糊测试 |


---

## 📚 资源大全

| 仓库 | ⭐ | 说明 |
|------|-----|------|
| [anthropics/skills](https://github.com/anthropics/skills) | 166,200 | 官方仓库，质量最有保证 |
| [obra/superpowers](https://github.com/obra/superpowers) | 266,215 | agentic skills 框架与开发方法论 |
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | 91,811 | MCP 服务大全（连接外部系统） |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 81,564 | 生产级工程类 skills |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 71,763 | 社区精选列表，分类齐全 |

---

## 怎么自己写一个 Skill

```
my-skill/
└── SKILL.md          # 必需
    references/       # 可选：参考资料
    scripts/          # 可选：脚本
```

`SKILL.md` 基本结构：

```markdown
---
name: my-skill
description: 一句话说明何时该用（AI 靠这句判断是否激活）
---

## 什么时候用
## 怎么做
## 注意事项
```

推荐用官方 [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 生成。

---

## ⚠️ 安全提醒

Skills 可包含**可执行脚本**。安装第三方 skill 前：

1. 先看 `SKILL.md` 内容，确认行为符合预期
2. 检查 `scripts/` 目录，里面的脚本会被执行
3. 优先选官方仓库或星数高、有活跃维护的来源

---

*收录有误或想推荐新 Skill？欢迎 [提 Issue](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues)*
