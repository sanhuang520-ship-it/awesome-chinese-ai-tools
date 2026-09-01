<div align="center">

<img src="https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/assets/readme-banner.webp" alt="chinese-web-themes 的 4 套中式主题与 guofeng-threejs 水墨 shader 的真实渲染" width="100%">

# 中文 AI Skills 库

**中文 Agent Skills 合集：可搜索、可安装、带实测证据**

<sub>Chinese Agent Skills / Chinese AI Skills directory with reproducible Codex evidence and explicit Claude Code / Cursor test gaps.</sub>

[English](README.en.md) · [English web guide](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/chinese-agent-skills/)

[![Skills](https://img.shields.io/badge/Skills-211%20个-e0795a?style=flat-square)](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/)
[![原创](https://img.shields.io/badge/本站原创-13%20个-86b894?style=flat-square)](EXAMPLES.md)
[![Daily Check](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/actions/workflows/daily-check.yml/badge.svg)](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/actions/workflows/daily-check.yml)
[![License](https://img.shields.io/badge/License-MIT-83808d?style=flat-square)](LICENSE)

**[🌐 在线浏览与搜索](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/)**　·　[📦 安装与排错](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/install/)　·　[📋 看真实输出](EXAMPLES.md)　·　[🧪 看兼容性证据](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/compatibility/)

<sub>[📚 无 JavaScript？浏览完整静态目录](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/catalog/)</sub>

</div>

> **和别的 awesome 列表有什么不一样**<br>
> ① 13 个 Skill 是我们自己写的，不是搬运<br>
> ② 不是只验证“能安装”：13/13 在 Codex 中自动触发，失败过程也公开<br>
> ③ 211 个 Skill 条目来自 163 个仓库，来源仓库**定期复检**一次还在不在（最近 2026-09-01），不转述无法复核的 AI 新闻

```bash
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --list
```

---

## 这是什么

**Skills 是给 AI 助手加的「专业技能包」。**

技术上就是一个文件夹 + 一份 `SKILL.md` 说明书，告诉 AI：什么时候该用、按什么步骤做。
支持 Skills 的客户端可以按任务自动激活；是否触发取决于客户端、版本、安装位置和任务措辞，需分别实测。

|  | 是什么 | 解决什么 |
|---|--------|---------|
| **Skills** | 一份工作说明书（Markdown + 可选脚本） | 教 AI **怎么做**某类任务 |
| **MCP** | 一个后台服务 | 让 AI **连上**外部系统（数据库、浏览器） |
| **插件** | 打包分发的组合 | 把 skills + MCP 打包一键装 |

---

## ⚠️ 一个实测发现：很多教程写的安装路径是错的

7 万星的 `awesome-claude-skills` 教你装到 `~/.config/claude-code/skills/`。
**我照做，装完没生效——那个目录在我这台 macOS 上根本不存在。**

用 Vercel Labs 的 `skills` CLI 实测（**1.5.23，2026-08-19 复测**）：

```bash
# 默认是「项目级」——装进你当前所在的那个目录，不是家目录
$ cd /tmp && npx skills add <repo> --skill <name>
✓ ./.agents/skills/<name>          # 落在 /tmp/.agents/skills/

# 要装成全局（用户级），必须加 -g
$ npx skills add <repo> --skill <name> -g
✓ ~/.agents/skills/<name>

$ ls -l ~/.claude/skills/
lrwxr-xr-x  <name> -> ../../.agents/skills/<name>   # 同级目录下的符号链接
```

CLI 帮助原文：`-g, --global  Install skill globally (user-level) instead of project-level`。
安装器会在同级的 `.claude/skills/` 建符号链接，所以两个路径能看到同一份文件。
**这只证明安装结果；本轮没有运行 Claude Code，不能据此声称自动触发。**

> **⚠️ 2026-08-19 更正**：这一节此前写的是「`npx skills add` 把文件装到 `~/.agents/skills/`」，
> 不准确。默认行为是装进**当前工作目录**；当初那次实测是在家目录下跑的，
> 于是把「当时的当前目录恰好是家目录」当成了「工具装到家目录」。
> 本次交叉验证：在 `/tmp` 下跑落在 `/tmp/.agents/skills/`；
> 在一个 git 仓库的子目录下跑落在该子目录，**不会向上找项目根**；加 `-g` 才走家目录。
>
> 这和本节批评 7 万星仓库的，其实是同一类错误——**把测试环境的偶然当成工具的行为**。
> 记下来是因为它比结论本身更值得记：可验证的东西要换环境验，不是跑一次就下定论。

**三条经验**：高星不等于正确；工具会变，写死的结论要定期复测；
**同一个命令换个目录跑结果就不同的时候，说明你测的是环境不是工具。**

---

## 怎么装

**[→ 不知道先试哪个？查看 13 个单项安装命令与可复制首次任务](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/try-agent-skills/)**：7 条来自历史逐字原文；6 条是运行前公开的前瞻任务，6 条均已执行，两类证据不会混写。

**[→ 已有明确目标？按中文表达、国风视觉、学习家庭、办公经营选择 4 组开箱组合](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/bundles/)**：每个 Skill 名称直达方法、案例与边界页；组合是编辑入口，不代表会同时触发或已经跨客户端认证。

```bash
# 先看仓库里有哪些（只读，不写任何文件）
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --list

# 装单个（推荐）。-g = 装到用户级 ~/.agents/skills/，任何目录下都能用
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill chinese-typography -g

# 全部装上（13 个）
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill '*' -g

# 不加 -g 就是「项目级」：装进你当前所在的这个目录，只在这个项目里可用
cd ~/my-project && npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill chinese-typography

# 已在当前 Git 项目安装过：按锁文件更新项目副本
npx --yes skills@1.5.22 update -p -y
```

> **上面每条命令都在 2026-08-20 用 CLI 1.5.23 实测跑过**：`--list` 正常列出 13 个；
> `--skill <name> -g` 落在 `~/.agents/skills/`；`--skill '*'` 确实装满 13 个；
> 不加 `-g` 落在当前目录。**顺带一提，`--skill a,b,c` 这种逗号分隔写法不生效**
> （只会列出清单不安装），要装多个就重复执行或用 `'*'`。

最后一条只适用于已有 `skills-lock.json` 的项目级安装。本仓库用历史夹具隔离复测为 13/13 完整文件夹更新成功；没有验证全局 `update -g`，详见[安装与项目更新记录](cases/skills-cli-isolated-install-2026-08-13.md)。

装好后重启你使用的客户端，用一个**不点名 Skill 名称**的自然任务测试是否自动触发。不同客户端与版本的行为可能不同；当前只有 Codex 的任务级实测。

安装与自动触发不是一回事。本站 13 个原创 Skill 已完成 CLI 发现、当前 Codex 安装核验和各 1 次不点名名称的自动触发测试；2 项大任务失败后通过缩小复测，原失败仍公开保留。详见 **[兼容性实测表](COMPATIBILITY.md)**。

不知道怎样判断“兼容”的证据强度？查看 **[Agent Skills 兼容性四层测试法](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/method/)**：发现、安装、自动触发与任务完成分别记录，环境错误不归因给 Skill。

已经安装但没有自动触发？按 **[Codex Skill 不触发的 5 步诊断树](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/codex-skill-not-triggering/)** 依次检查 CLI 发现、文件路径、客户端读取、任务完成和环境阻断。

已经安装但内容可能过期？查看 **[Agent Skill 项目级更新实测](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/update-agent-skill/)**：先核对 `skills-lock.json`，再运行固定版本更新，并比较完整文件夹与全局边界。

想把重复工作变成 Skill？查看 **[创建 Codex Skill 中文实战](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/create-codex-skill/)**：从最小 SKILL.md、触发描述到安装与自动触发测试。

仓库也已被 [skills.sh 收录](https://skills.sh/sanhuang520-ship-it/awesome-chinese-ai-tools)，可查看 13 个 Skill 的独立页面和该平台记录的聚合安装次数。该数字来自 skills CLI 遥测，可能包含维护者安装核验，不等于独立用户、实际使用效果或质量认证。

[Agent-Skills.md 作者页](https://agent-skills.md/authors/sanhuang520-ship-it)也已展示全部 13 个原创 Skill。它是第三方目录入口，不代表独立兼容性实测、内容审核或质量认证；分类与标签正在刷新复核。

### 30 秒第一次试用

只装一个当前需要的 Skill，重启客户端，然后直接说一条自然任务。不要在任务里写 Skill 名称，这样才能观察客户端是否会自动选择它。

| 你想试什么 | 安装 | 复制给 AI 的任务 | 本仓库记录 |
|---|---|---|---|
| 审查中文网页排版 | `npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill chinese-typography -g` | `请检查下面这段网页 CSS 的中文排版问题，只做审查，不修改文件。明确列出问题、理由和建议值：body { font-family: Arial, sans-serif; font-size: 14px; line-height: 1.35; text-align: justify; word-break: break-all; }` | [Codex 单任务实测](cases/chinese-typography-codex.md) |
| 整理一份不编数据的周报 | `npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill chinese-work-report -g` | `帮我把下面素材整理成给老板看的中文周报：本周修复了登录问题，做了两个页面；结果数据暂时没有；下周继续优化。请按结论先行组织，不要编造数字。` | [Codex 单任务实测](cases/chinese-work-report-codex.md) |
| 校对一版不编参数的商品文案 | `npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill ecommerce-copywriting -g` | `给一款普通保湿面霜写电商主图文案。已知只有：50g、无香型、89元。没有提供的参数、认证和功效不要编造；先列出可写、待补和不应发布的信息。` | [Codex 单任务实测](cases/ecommerce-copywriting-codex.md) |
| 制定不靠刷视频的学习计划 | `npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill ai-learning-coach -g` | `我想用两周入门 SQL，但不想再看完教程就忘。先了解我的目标和基础，再带我制定能动手练习的计划。` | [Codex 单任务实测](cases/ai-learning-coach-codex.md) |

这些任务在记录的 Codex 版本中发生过自动触发；它们不是“必定触发”的保证。若结果不同，请保留客户端版本和任务原文，按[兼容性实测表单](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml)提交成功或失败结果。

---

## 用过之后，留下一个可复现结果

这个项目现在最需要的不是一句“好用”，而是其他人能够照着重现的真实案例。成功、失败和“不如预期”都可以，只需写清楚 5 件事：

1. 使用的 Skill
2. 使用环境与版本（Codex / Claude Code / Cursor 等）
3. 你交给 AI 的任务
4. 实际发生了什么
5. 哪一步有效，哪一步需要改进

**[→ 用结构化表单提交一次兼容性实测](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml)**　·　[在 Discussion 交流](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/discussions/4)

准备提 PR 的贡献者也可以复制[机器可读示例](examples/compatibility-result.example.json)，按 [JSON Schema](schemas/compatibility-result.schema.json)填写，并用仓库内的无依赖校验器检查环境阻断、证据边界和常见敏感信息。

请先移除 Token、邮箱、私人路径和未公开业务数据；敏感漏洞请按[🔒 安全报告](SECURITY.md)中的私密渠道提交。被整理进仓库的案例会保留原讨论链接，并明确标注是用户反馈，不会把个别体验写成普遍结论。

---

## ✍️ 本站原创 Skill（13 个）

这是这个仓库和其他 awesome 列表的区别：**下面这些是我们自己写的，不是搬运的。**

**[→ 按使用场景比较 13 个 Skill、实测状态和安全边界](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/guides/)**

**[→ 复制 7 条有逐字原文的首次测试任务](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/reproduce/)**（另外 6 条只有摘要，不反向补写）

**[→ 查看前瞻复测与修复闭环](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/retest/)**（6 条任务和门槛先公开；初次 4 条通过、2 条失败，针对性修复后两条用原任务均通过 4/4；旧失败不覆盖）

**[→ Agent Skill 测试失败后怎么修](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/fix-agent-skill/)**（不改题、不降门槛、不覆盖旧失败；含两条 3/4 → 4/4 的完整证据链）

**[→ 在一页选择全部 13 个首次试用任务](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/try-agent-skills/)**（单项安装、复制任务、历史证据或前瞻成功门槛）

| Skill | 做什么 |
|-------|--------|
| [`ai-learning-coach`](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/learning/) | 学习教练：先校准目标、基础、时间和验收标准，再进入主动回忆 → 输出 → 纠错归因 → 间隔复习；不直接代做学习产出 |
| [`book-digest-cn`](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/reading/) | 拆书三层法：作者在回答什么问题 → 核心主张与论证 → 我的行动、质疑和边界；不编造书中内容，不抄目录式笔记 |
| [`bookkeeping-cn`](skills/bookkeeping-cn/) | 记账整理。**明确不做**税务筹划、投资建议，不替代会计 |
| [`chinese-design-md`](skills/chinese-design-md/) | 中式 DESIGN.md 设计系统（本站原创）：8 套可直接丢进项目根目录的设计文档，AI 读了就按规范生成界面。含中文排版规则（行高 1.75 / 不用 justify / 着重号代替斜体 / CJK 避头尾），对比度逐项实测并标出不达标项 |
| [`chinese-lesson-plan`](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/lesson-plan/) | 中小学教案：先核对学段、教材版本和适用课标，再按核心素养、学习任务与评价证据组织目标；公开完整任务失败与缩小复测 |
| [`chinese-typography`](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/typography/) | 中文排版：中英间距、CJK 断行避头尾、字体栈、标点全半角，含错误对照与可直接复制的 CSS |
| [`chinese-web-themes`](skills/chinese-web-themes/) | 8 套中式网页主题（水墨/青绿/宋韵/敦煌/朱砂/新中式/竹韵/夜宴），对比度全过 WCAG AA |
| [`chinese-work-report`](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/work-report/) | 周报 / 述职 / 项目汇报，讲清楚做了什么、结果如何、下一步；没有结果数据时明确留空，不编数字 |
| [`ecommerce-copywriting`](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/ecommerce-copywriting/) | 电商文案上架前校样：区分可写、待补与不应发布；**不编造**材质、成分、认证、销量或功效 |
| [`github-readme-cn`](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/readme-audit/) | GitHub 中文项目门面优化（本站原创）：首屏结构、真实截图怎么截、命名与 topics、发布前自查清单。附 15 个高增长仓库的结构观察，明确区分相关性与不可验证的部分，不承诺涨星 |
| [`guochao-visual-cn`](skills/guochao-visual-cn/) | 12 种中国美学画风配方，输出可直接用的 AI 绘图提示词 |
| [`guofeng-threejs`](skills/guofeng-threejs/) | 国风 Three.js 渲染：水墨 shader 三技法。只做中式渲染，不做通用 Three.js 教程 |
| [`homework-tutor-cn`](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/homework/) | 家长辅导作业：**不生成给孩子直接抄写的成品**，先给引导话术，再单列家长核对结果；公开最终使用仍由人决定的边界 |

📋 **[看它们实际输出什么 → EXAMPLES.md](EXAMPLES.md)**

### 统一的设计原则：写清楚「不做什么」

写这些 skill 时最大的领悟是——**真正决定一个 skill 好不好用的，往往是它的边界。**

> 记账不做税务筹划 · 辅导作业不生成给孩子直接抄写的成品 · 学习教练不替你完成输出 · 国潮视觉不伪造文物

一个只写"能做什么"的 skill，用起来会发现它在你没问的地方也给意见，
在它不该确定的地方也很确定。

---

## 📸 真实渲染结果

两个代码类 Skill 的产出可以直接截图验证（**headless Chrome 实跑生成，不是示意图**）：

![chinese-web-themes 水墨主题真实渲染](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/assets/shots/theme-ink.webp)

![guofeng-threejs 水墨 shader 真实渲染](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/assets/shots/threejs-ink.webp)

**[看全部 8 套主题 + shader →](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/shots/)**

> 为什么画风类 Skill 那一页没有效果图？因为它的产出是**提示词**，
> 实际出图取决于你用哪个模型，我们没法用一张图替你保证结果，就不放。
> 能给的是[配色体系与纹样对照](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/guochao/)——那些是可以直接验证的。

---

## 收录了什么

| 分类 | 数量 |
|------|------|
| 🇨🇳 中文 Skill 条目 | 85 |
| 📄 官方 Skill 条目 | 19 |
| ✍️ 本站原创 | 13 |
| **合计** | **211** |

**[→ 看完整清单 SKILLS.md](SKILLS.md)**（每次维护时从数据自动重建，不会和实际对不上）

另附 **47 个 AI 工具导航**，链接定期自动实测。

---

## 🔄 每次维护自动做的事

| 步骤 | 做什么 |
|------|--------|
| 1 | 核对 [SOURCES.md](SOURCES.md) 里各家 AI 官方公告页链接 |
| 2 | 47 个工具入口复检：38 个直接成功，7 个返回机器人拦截响应，2 个白名单跳过请求 |
| 3 | **163 个来源仓库复检**（覆盖 211 个 Skill 条目）：还在不在、星数、最后更新时间 |
| 4 | 从数据重建 SKILLS.md，并同步公开统计 |

这套流程跑在 **GitHub Actions** 上，[运行记录公开可查](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/actions/workflows/daily-check.yml)——不依赖任何人的电脑，也不用你相信我说的话。

> 2026-08-18 起改为**手动触发**（此前是每天定时）。每次运行的时间、结果和完整日志都公开可查，
> 上方「最近复检」日期直接来自数据文件，所以你看到的永远是真实的上次复检时间，而不是一句「每天都在跑」的承诺。

最近复检：**2026-09-01**，失效 0 个。
白名单项是此前人工复核后为避免自动化反复误报而跳过，不等于本次工作流再次访问成功；机器人拦截响应也只说明目标服务有响应，不证明普通用户在所有地区都可访问。
超过半年没更新的会在站内标 🕰——停止维护不等于没价值，但你有权在点进去之前就知道。

### 检测抓到过的真实域名迁移

- `cursor.sh` → `cursor.com`
- Windsurf 被 Cognition 收购，并入 Devin Desktop
- `blackforestlabs.ai` → `bfl.ai`（Flux）
- `runwayml.com` → `runway.com`

---

## 📌 内容原则：不转述新闻

**我们不转述任何 AI 新闻。**

原因很实际：无法核实时效性新闻的真伪。这个项目早期干过这事，
出现过把几个月前的旧消息当作"今日新闻"发布的情况。

现在改为**只提供各家 AI 官方公告页的直达链接**（[SOURCES.md](SOURCES.md)），
读者点过去看原文，我们不做任何转述和担保。
早期那批内容归档在 [archive/news-2026/](archive/news-2026/)，附了说明——
保留是为了留下记录，但**请不要把那里的内容当作可靠信息使用**。

详见 [内容准则与维护说明](CONTENT_POLICY.md)。

---

## 📝 这个项目踩过的坑

整理这些 skill 的过程写成了一篇文章，包括一个 7 万星仓库文档里的路径错误、
一次让两个月访问数据全废的静默失败，和一次自己打自己脸的复检漏洞：

**[7 万星仓库教的安装路径是错的——整理 130 个 AI Skill 的踩坑记录](blog/skill-pitfalls.md)**

> 这篇文章后来被自己推翻过两次，更正都留在文内没有删。
> 最狠的一次是 2026-08-19：文章开头批评 7 万星仓库把安装路径写错，
> 而它自己写的路径也是错的——**而且是同一类错误**，
> 把"我当时恰好在家目录下敲的命令"当成了工具的行为。
> 教训因此从两条变成三条，第三条是：**换个环境再测一遍。跑过不等于跑对。**
>
> （[掘金版](https://juejin.cn/post/7671196739655352339)尚未同步这次更正，以仓库版为准。）

---

## 想写自己的 Skill

```
my-skill/
└── SKILL.md          # 必需
    references/       # 可选
    scripts/          # 可选
```

推荐用官方 [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 生成。

⚠️ **安全提醒**：Skills 可以包含**可执行脚本**。装第三方 skill 前，
先看一眼它的 `SKILL.md` 和 `scripts/` 内容。

也可以运行本站的**[只读安装前审计器](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/audit-skill/)**，本地检查脚本、符号链接、联网、凭据词、文件写删和高风险命令。它不执行目标 Skill、不上传内容；结果只是人工复核线索，不是恶意代码检测或安全认证。

本站原创的 13 个 Skill 已完成首轮静态文件检查；当前没有独立可执行脚本，`guofeng-threejs` 浏览器 Demo 存在已披露的 CDN 依赖。完整范围和限制见 **[质量与安全标签](QUALITY.md)**，结论不适用于其余第三方收录。

---

## 贡献

**[→ 第一次贡献：选择一个 10—20 分钟的真实任务](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/contribute/)**（跨客户端复测、Windows/Linux 安装路径、第三方条目事实复核；每项都有完成标准）

不会代码也可以贡献：[推荐 Skill 或工具](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=add-entry.yml) · [报告事实错误](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=report-problem.yml) · [改进原创 Skill](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=improve-skill.yml) · [提交兼容性实测](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new?template=compatibility-result.yml)。不知道的字段可以如实写“不确定”或“暂无”，不需要为了填满表单而猜测。

使用问题和实际效果欢迎放到 [Discussions](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/discussions)，想直接改数据请查看 [CONTRIBUTING.md](CONTRIBUTING.md)。

如果你用的是 Claude Code 或 Cursor，最有价值的贡献是提交一次成功或失败的真实结果：我们会把客户端版本、原始任务和证据边界整理进[兼容性实测表](COMPATIBILITY.md)，不会把单次体验包装成普遍结论。

在文章、研究或其他目录中引用本项目时，可使用 GitHub 的 **Cite this repository** 入口或查看 [CITATION.cff](CITATION.cff)。当前稳定引用版本为 [v1.2.0](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/tree/v1.2.0)；持续更新内容请链接仓库主页，并注明访问日期。

**发现事实错误请一定告诉我们** —— 这个项目全部的价值就在"可信"两个字上。

---

<div align="center">
<sub>MIT License · 数据最后复检 2026-09-01 · 公开统计由脚本同步于 2026-09-01</sub>
</div>
