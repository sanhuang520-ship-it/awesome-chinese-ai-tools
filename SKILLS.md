# 🧩 AI Agent Skills 中文合集

> **114 个 Skill｜55 个中文｜✍️ 9 个本站原创**
> 每一个都经 GitHub API 验证仓库真实存在

📋 **[看原创 Skill 实际输出什么 → EXAMPLES.md](EXAMPLES.md)**　🌐 [在线浏览](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/)

---

## 什么是 Skills

**一句话：Skills 是给 AI 助手加的「专业技能包」。**

一个文件夹 + 一份 `SKILL.md` 说明书，告诉 AI 什么时候该用、按什么步骤做。AI 自动判断何时激活。

| | 是什么 | 解决什么 |
|---|--------|---------|
| **Skills** | 工作说明书（Markdown + 可选脚本） | 教 AI **怎么做**某类任务 |
| **MCP** | 后台服务 | 让 AI **连上**外部系统 |
| **插件** | 打包组合 | skills + MCP 一键装 |

---

## 怎么安装

```bash
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --list          # 先看有哪些
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill guochao-visual-cn
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill '*'             # 全部
```

> ⚠️ **实测提醒**：部分英文教程（包括 7 万星仓库）写的路径是 `~/.config/claude-code/skills/`，
> 经本机实测，macOS 上**实际生效的是 `~/.claude/skills/`**。

装好后重启 Claude Code，**无需手动调用**——描述任务，AI 自动激活。

---

## Skill 清单


### 🇨🇳 中文原创（55 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [ai-learning-coach](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/ai-learning-coach) | **✍️ 本站原创** | AI 学习教练（本站原创）：不直接给答案，带你走完整学习循环——定目标→主动回忆→输出→纠错→间隔复习→项目交付，含错因分析模板 |
| [book-digest-cn](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/book-digest-cn) | **✍️ 本站原创** | 拆书助手（本站原创）：三层拆解（作者在答什么问题→核心主张→对我有什么用），拒绝抄目录式笔记 |
| [bookkeeping-cn](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/bookkeeping-cn) | **✍️ 本站原创** | 记账整理助手（本站原创）：流水分类、收支表、预算跟踪；明确不做税务与投资建议 |
| [chinese-lesson-plan](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-lesson-plan) | **✍️ 本站原创** | 中文教案助手（本站原创）：按新课标三维目标生成中小学教案，含分层作业、板书设计、说课稿 |
| [chinese-typography](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-typography) | **✍️ 本站原创** | 中文排版助手（本站原创）：中英间距、CJK 断行避头尾、字体栈、标点全半角、行高行宽，附可直接用的 CSS 与公众号排版规则 |
| [chinese-work-report](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/chinese-work-report) | **✍️ 本站原创** | 职场汇报助手（本站原创）：周报/月报/述职/项目汇报，结论先行、卖点翻价值，含 PPT 大纲 |
| [ecommerce-copywriting](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/ecommerce-copywriting) | **✍️ 本站原创** | 电商文案助手（本站原创）：商品标题/详情页/卖点提炼，分平台规则，含广告法违禁词红线 |
| [guochao-visual-cn](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/guochao-visual-cn) | **✍️ 本站原创** | 国潮视觉助手（本站原创）：12 种中国美学画风配方（水墨/工笔/青绿/敦煌/年画/剪纸/国漫等），输出可直接用的提示词，附纹样寓意与传统配色速查 |
| [homework-tutor-cn](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/main/skills/homework-tutor-cn) | **✍️ 本站原创** | 家长辅导作业助手（本站原创）：不给答案给引导话术，分学科方法，含情绪对抗处理 |
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
| [humanities-writing-companion](https://github.com/tizzy916/humanities-writing-companion) | ⭐325 | 人文学科写作助手：11 种模式覆盖构思到成稿 |
| [opencode-skills](https://github.com/zrt-ai-lab/opencode-skills) | ⭐263 | 技能库：视频生成、图片生成、Agent 互联、智能问数 |
| [universal-examprep-skill](https://github.com/ZeKaiNie/universal-examprep-skill) | ⭐263 | 考前突击教练：把课件资料变成应试重点 |
| [skills_collection](https://github.com/wwwzhouhui/skills_collection) | ⭐257 | 个人实用技能集，覆盖开发效率与内容创作 |
| [humanizer-zh-academic](https://github.com/redbaronyyyyy-eng/humanizer-zh-academic) | ⭐234 | 降低中文学术写作 AIGC 检测率 |
| [awesome-skills-cn](https://github.com/lingxling/awesome-skills-cn) | ⭐224 | 热门 Skills 中文学习版 + 教程，7000+ 收录 |
| [Bloom](https://github.com/Li-Evan/Bloom) | ⭐218 | 私人 AI 家教：识别你的学习方式，安排下一课 |
| [niubiskill](https://github.com/nathanskill/niubiskill) | ⭐208 | 中文变现决策：判断一件事是否接近收入再投入 |
| [Vibe_coding_guide](https://github.com/Lling0000/Vibe_coding_guide) | ⭐205 | 中文优先的 Vibe Coding 工程化流程指南 |
| [technical-writing](https://github.com/luoling8192/technical-writing) | ⭐204 | 中文技术写作：设计文档、评审稿、复盘、分享稿 |
| [SecSkills](https://github.com/Arenbai/SecSkills) | ⭐200 | 渗透测试技能模块，遵循 PTES 标准全阶段覆盖 |
| [openclaw-guide](https://github.com/liyupi/openclaw-guide) | ⭐185 | OpenClaw 中文文档站：安装部署、Agent 架构、Skills 配置 |
| [makeownsrt](https://github.com/joshhu/makeownsrt) | ⭐175 | 从 MKV 提取英文字幕并翻成繁中双语 SRT |
| [Auto-CV](https://github.com/flamingoTOM/Auto-CV) | ⭐163 | LaTeX 中文简历模板 + 自动提取内容生成 |
| [JobOK](https://github.com/GresonKwan/JobOK) | ⭐115 | 中文求职：优势挖掘、岗位匹配、简历优化、面试训练 |
| [hermes-arxiv-agent](https://github.com/genggng/hermes-arxiv-agent) | ⭐107 | 每天自动抓 arXiv 论文，生成中文摘要推送到飞书 |
| [kc_ai_skills](https://github.com/KerberosClaw/kc_ai_skills) | ⭐77 | 中文优先的 Claude Code / Codex skills 合集 |
| [wechat-writing-style](https://github.com/yaoleifly/wechat-writing-style) | ⭐73 | 微信公众号中文写作风格 |
| [stop-slop-zh](https://github.com/VincentOld/stop-slop-zh) | ⭐60 | 消除中文 AI 写作痕迹：拆排比、去名词化、换具体细节 |
| [cnki-aigc---skill](https://github.com/qingshanliuci/cnki-aigc---skill) | ⭐33 | 知网 AIGC 降重：实测把 AI 率从 20.6% 降到 10.1% |
| [awesome-skills-zh](https://github.com/yzfly/awesome-skills-zh) | ⭐25 | 精选 Claude / Agent / LLM Skills 中文资源列表 |
| [awesome-claude-skills-zh-TW](https://github.com/ammosu/awesome-claude-skills-zh-TW) | ⭐24 | awesome-claude-skills 繁体中文化版本 |
| [scholar-wendao-skill](https://github.com/tizzy916/scholar-wendao-skill) | ⭐20 | 学者问道：把学者视角提炼成可复用框架 |
| [awesome-claude-skills-zh](https://github.com/shishirui/awesome-claude-skills-zh) | ⭐14 | 中文社区优先的 Claude skills 精选收录 |
| [refine-legal-chinese](https://github.com/katejianglaw/refine-legal-chinese) | ⭐13 | 法言法语：把口语化表述改写为规范法律中文 |
| [ip-character-designer](https://github.com/Beatatata/ip-character-designer) | ⭐11 | 自媒体 IP 配图生成器：10 种画风 × 双版本 × 中文提示词 |
| [awesome-claude-skills-cn](https://github.com/bbylw/awesome-claude-skills-cn) | ⭐9 | Awesome Claude Skills 中文版 |
| [CN-The-Complete-Guide-to-Building-Skill-for-Claude](https://github.com/chenqing0106/CN-The-Complete-Guide-to-Building-Skill-for-Claude) | ⭐5 | 《为 Claude 构建技能的完整指南》中文翻译：结构、模式、测试、分发 |
| [ai-video-creator](https://github.com/Frank-oll/ai-video-creator) | ⭐5 | 把生活妙招选题端到端做成可发布的竖屏 AI 短视频（含配音） |
| [cn-humanizer-academic](https://github.com/ranranrannervous/cn-humanizer-academic) | ⭐5 | 中文学术论文降 AI 痕迹，针对 BERT 语义检测器 |


### 📄 文档办公（9 个）

| Skill | 来源 | 说明 |
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


### 💻 开发工程（21 个）

| Skill | 来源 | 说明 |
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
| [AppGenesisForge](https://github.com/pcliangx/AppGenesisForge) | ⭐413 | 19 个角色协作的 AI Agent 团队脚手架，按阶段门禁推进 |
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

| Skill | 来源 | 说明 |
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

| Skill | 来源 | 说明 |
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

| Skill | 来源 | 说明 |
|-------|------|------|
| [root-cause-tracing](https://github.com/obra/superpowers/tree/main/skills/root-cause-tracing) | ⭐266,215 | 错误深藏在执行链路时，追溯根本原因 |
| [CSV Data Summarizer](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill) | ⭐442 | 自动分析 CSV 文件并生成完整数据报告 |
| [deep-research](https://github.com/sanjay3290/ai-skills/tree/main/skills/deep-research) | ⭐364 | 调用 Gemini Deep Research 做自主多步研究 |
| [postgres](https://github.com/sanjay3290/ai-skills/tree/main/skills/postgres) | ⭐364 | 对 PostgreSQL 执行安全的只读 SQL 查询 |
| [recursive-research](https://github.com/Anjos2/recursive-research) | ⭐37 | 跨领域递归研究，可深入到博士级别 |


### 🔐 安全取证（5 个）

| Skill | 来源 | 说明 |
|-------|------|------|
| [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | ⭐17,460 | 逆向工程与授权渗透测试的 Skill 路由包 |
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
    references/       # 可选
```

**一个建议**：写清楚「不做什么」和「能做什么」同样重要。
我们 9 个原创 Skill 都写明了边界——记账不做税务筹划、辅导作业不给答案、
学习教练不替你完成输出、国潮视觉不伪造文物。

推荐用官方 [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 生成。

---

## ⚠️ 安全提醒

Skills 可含**可执行脚本**。装第三方前先看 `SKILL.md` 和 `scripts/` 内容。

---

*收录有误或想推荐新 Skill？欢迎 [提 Issue](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues)*
