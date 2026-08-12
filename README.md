<div align="center">

<img src="https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/assets/readme-banner.webp" alt="chinese-web-themes 的 4 套中式主题与 guofeng-threejs 水墨 shader 的真实渲染" width="100%">

# 中文 AI Skills 库

**给 AI 助手装上中文场景的专业技能包**

[![Skills](https://img.shields.io/badge/Skills-184%20个-e0795a?style=flat-square)](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/)
[![原创](https://img.shields.io/badge/本站原创-13%20个-86b894?style=flat-square)](EXAMPLES.md)
[![Daily Check](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/actions/workflows/daily-check.yml/badge.svg)](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/actions/workflows/daily-check.yml)
[![Stars](https://img.shields.io/github/stars/sanhuang520-ship-it/awesome-chinese-ai-tools?style=flat-square&color=e0795a)](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/stargazers)
[![License](https://img.shields.io/badge/License-MIT-83808d?style=flat-square)](LICENSE)

**[🌐 在线浏览（可搜索筛选）](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/)**　·　[🧪 兼容性实测](COMPATIBILITY.md)　·　[🛡️ 质量与安全标签](QUALITY.md)　·　[🧰 中文开箱组合](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/bundles/)　·　[📋 完整清单](SKILLS.md)　·
[📸 真实渲染截图](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/shots/)　·　[🎨 12 种画风对照](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/guochao/)　·　[✒️ 中文排版实测](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/typography/)

</div>

> **和别的 awesome 列表有什么不一样**<br>
> ① 13 个 Skill 是我们自己写的，不是搬运<br>
> ② 184 个仓库**每天自动复检**一次还在不在<br>
> ③ 不转述任何 AI 新闻——[原因](CONTENT_POLICY.md)

```bash
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --list
```

---

## 这是什么

**Skills 是给 AI 助手加的「专业技能包」。**

技术上就是一个文件夹 + 一份 `SKILL.md` 说明书，告诉 AI：什么时候该用、按什么步骤做。
AI 会自动判断何时激活，不需要手动切换。

|  | 是什么 | 解决什么 |
|---|--------|---------|
| **Skills** | 一份工作说明书（Markdown + 可选脚本） | 教 AI **怎么做**某类任务 |
| **MCP** | 一个后台服务 | 让 AI **连上**外部系统（数据库、浏览器） |
| **插件** | 打包分发的组合 | 把 skills + MCP 打包一键装 |

---

## ⚠️ 一个实测发现：很多教程写的安装路径是错的

7 万星的 `awesome-claude-skills` 教你装到 `~/.config/claude-code/skills/`。
**我照做，装完没生效——那个目录在我这台 macOS 上根本不存在。**

用官方 CLI 实测（skills 1.5.22）：

```bash
$ npx skills add <repo> --skill <name>
✓ ~/.agents/skills/<name>          # 文件实际在这里（多家 agent 共用）

$ ls -l ~/.claude/skills/
lrwxr-xr-x  <name> -> ../../.agents/skills/<name>   # 这里是符号链接
```

Claude Code 读的是 `~/.claude/skills/`，所以两个路径下都能看到。

**两条经验**：高星不等于正确，路径命令这类可验证的东西花 10 秒实测比信任星数靠谱；
**而且工具会变——这个结论我们复测过一次才发现要补细节。**

---

## 怎么装

```bash
# 先看仓库里有哪些
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --list

# 装单个（推荐）
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill chinese-typography

# 全部装上
npx skills add https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools --skill '*'
```

装好后重启 Claude Code，**无需手动调用**——描述任务，AI 自动激活。

安装与自动触发不是一回事。本站 13 个原创 Skill 已完成 CLI 发现与当前 Codex 安装内容核验，已有 **3 个 Skill** 完成不点名名称的 Codex 自动触发实测；其余逐项触发、Claude Code 和 Cursor 仍在继续测试，详见 **[兼容性实测表](COMPATIBILITY.md)**。

---

## 用过之后，留下一个可复现结果

这个项目现在最需要的不是一句“好用”，而是其他人能够照着重现的真实案例。成功、失败和“不如预期”都可以，只需写清楚 5 件事：

1. 使用的 Skill
2. 使用环境与版本（Codex / Claude Code / Cursor 等）
3. 你交给 AI 的任务
4. 实际发生了什么
5. 哪一步有效，哪一步需要改进

**[→ 在置顶 Discussion 分享第一次使用结果](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/discussions/4)**

请先移除 Token、邮箱、私人路径和未公开业务数据。被整理进仓库的案例会保留原讨论链接，并明确标注是用户反馈，不会把个别体验写成普遍结论。

---

## ✍️ 本站原创 Skill（13 个）

这是这个仓库和其他 awesome 列表的区别：**下面这些是我们自己写的，不是搬运的。**

| Skill | 做什么 |
|-------|--------|
| [`ai-learning-coach`](skills/ai-learning-coach/) | 学习教练：定目标 → 主动回忆 → 输出 → 纠错归因 → 间隔复习。不直接给答案 |
| [`book-digest-cn`](skills/book-digest-cn/) | 拆书三层法：作者在答什么问题 → 核心主张 → 对我有什么用。拒绝抄目录式笔记 |
| [`bookkeeping-cn`](skills/bookkeeping-cn/) | 记账整理。**明确不做**税务筹划、投资建议，不替代会计 |
| [`chinese-design-md`](skills/chinese-design-md/) | 中式 DESIGN.md 设计系统（本站原创）：8 套可直接丢进项目根目录的设计文档，AI 读了就按规范生成界面。含中文排版规则（行高 1.75 / 不用 justify / 着重号代替斜体 / CJK 避头尾），对比度逐项实测并标出不达标项 |
| [`chinese-lesson-plan`](skills/chinese-lesson-plan/) | 中小学教案。含防套话机制：学情分析要写这个年龄段的具体特征 |
| [`chinese-typography`](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/typography/) | 中文排版：中英间距、CJK 断行避头尾、字体栈、标点全半角，含错误对照与可直接复制的 CSS |
| [`chinese-web-themes`](skills/chinese-web-themes/) | 8 套中式网页主题（水墨/青绿/宋韵/敦煌/朱砂/新中式/竹韵/夜宴），对比度全过 WCAG AA |
| [`chinese-work-report`](skills/chinese-work-report/) | 周报 / 述职 / 项目汇报，讲清楚做了什么、结果如何、下一步 |
| [`ecommerce-copywriting`](skills/ecommerce-copywriting/) | 电商文案，内置《广告法》违禁词红线。**不编造**材质、成分、认证参数 |
| [`github-readme-cn`](skills/github-readme-cn/) | GitHub 中文项目门面优化（本站原创）：首屏结构、真实截图怎么截、命名与 topics、发布前自查清单。附 15 个高增长仓库的实测数据，明确区分相关性与不可验证的部分，不承诺涨星 |
| [`guochao-visual-cn`](skills/guochao-visual-cn/) | 12 种中国美学画风配方，输出可直接用的 AI 绘图提示词 |
| [`guofeng-threejs`](skills/guofeng-threejs/) | 国风 Three.js 渲染：水墨 shader 三技法。只做中式渲染，不做通用 Three.js 教程 |
| [`homework-tutor-cn`](skills/homework-tutor-cn/) | 家长辅导作业。**不给答案**，给引导话术；还处理「家长自己要发火」的场景 |

📋 **[看它们实际输出什么 → EXAMPLES.md](EXAMPLES.md)**

### 统一的设计原则：写清楚「不做什么」

写这些 skill 时最大的领悟是——**真正决定一个 skill 好不好用的，往往是它的边界。**

> 记账不做税务筹划 · 辅导作业不给答案 · 学习教练不替你完成输出 · 国潮视觉不伪造文物

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
| 🇨🇳 中文原创仓库 | 68 |
| 📄 官方收录 | 19 |
| ✍️ 本站原创 | 13 |
| **合计** | **184** |

**[→ 看完整清单 SKILLS.md](SKILLS.md)**（每天从数据自动重建，不会和实际对不上）

另附 **47 个 AI 工具导航**，链接每日自动实测。

---

## 🔄 每天自动做的事

| 步骤 | 做什么 |
|------|--------|
| 1 | 今日工具推荐 |
| 2 | 核对 [SOURCES.md](SOURCES.md) 里各家 AI 官方公告页链接 |
| 3 | 47 个工具链接实测可访问性 |
| 4 | **184 个 skill 仓库复检**：还在不在、星数、最后更新时间 |
| 5 | 从数据重建 SKILLS.md |

这套流程跑在 **GitHub Actions** 上，[运行记录公开可查](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/actions/workflows/daily-check.yml)——不依赖任何人的电脑，也不用你相信我说的话。

最近复检：**2026-08-12**，失效 0 个。
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

**[7 万星仓库教的安装路径是错的——整理 130 个 AI Skill 的踩坑记录](https://juejin.cn/post/7671196739655352339)**

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

本站原创的 13 个 Skill 已完成首轮静态文件检查；当前没有独立可执行脚本，`guofeng-threejs` 浏览器 Demo 存在已披露的 CDN 依赖。完整范围和限制见 **[质量与安全标签](QUALITY.md)**，结论不适用于其余第三方收录。

---

## 贡献

收录有误、链接失效、想推荐新 Skill，可以选择对应的 [Issue 表单](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new/choose)，
使用问题和实际效果欢迎放到 [Discussions](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/discussions)，或查看 [CONTRIBUTING.md](CONTRIBUTING.md)。

**发现事实错误请一定告诉我们** —— 这个项目全部的价值就在"可信"两个字上。

---

<div align="center">
<sub>MIT License · 数据最后复检 2026-08-12 · 公开统计由脚本同步于 2026-08-12</sub>
</div>
