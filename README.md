<div align="center">

<img src="https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/assets/readme-banner.webp" alt="chinese-web-themes 的 4 套中式主题与 guofeng-threejs 水墨 shader 的真实渲染" width="100%">

# 中文 AI Skills 库

**给 AI 助手装上中文场景的专业技能包**

[![Skills](https://img.shields.io/badge/Skills-129%20个-e0795a?style=flat-square)](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/)
[![原创](https://img.shields.io/badge/本站原创-11%20个-86b894?style=flat-square)](EXAMPLES.md)
[![复检](https://img.shields.io/badge/仓库复检-每日自动-d9a441?style=flat-square)](#-每天自动做的事)
[![Stars](https://img.shields.io/github/stars/sanhuang520-ship-it/awesome-chinese-ai-tools?style=flat-square&color=e0795a)](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/stargazers)
[![License](https://img.shields.io/badge/License-MIT-83808d?style=flat-square)](LICENSE)

**[🌐 在线浏览（可搜索筛选）](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/)**　·　[📋 完整清单](SKILLS.md)　·
[📸 真实渲染截图](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/shots/)　·　[🎨 12 种画风对照](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/guochao/)

</div>

> **和别的 awesome 列表有什么不一样**
> ① 11 个 Skill 是我们自己写的，不是搬运
> ② 129 个仓库**每天自动复检**一次还在不在
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
**我照做，装完没生效。**

本机实测（macOS）实际生效的是：

```bash
~/.claude/skills/
```

用官方 `npx skills add` CLI 装，落盘位置也是这里。
**高星不等于正确——路径、命令这类可验证的东西，花 10 秒实测比信任星数靠谱。**

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

---

## ✍️ 本站原创 Skill（11 个）

这是这个仓库和其他 awesome 列表的区别：**下面这些是我们自己写的，不是搬运的。**

| Skill | 做什么 |
|-------|--------|
| [`ai-learning-coach`](skills/ai-learning-coach/) | 学习教练：定目标 → 主动回忆 → 输出 → 纠错归因 → 间隔复习。不直接给答案 |
| [`book-digest-cn`](skills/book-digest-cn/) | 拆书三层法：作者在答什么问题 → 核心主张 → 对我有什么用。拒绝抄目录式笔记 |
| [`bookkeeping-cn`](skills/bookkeeping-cn/) | 记账整理。**明确不做**税务筹划、投资建议，不替代会计 |
| [`chinese-lesson-plan`](skills/chinese-lesson-plan/) | 中小学教案。含防套话机制：学情分析要写这个年龄段的具体特征 |
| [`chinese-typography`](skills/chinese-typography/) | 中文排版：中英间距、CJK 断行避头尾、字体栈、标点全半角，输出可直接用的 CSS |
| [`chinese-web-themes`](skills/chinese-web-themes/) | 8 套中式网页主题（水墨/青绿/宋韵/敦煌/朱砂/新中式/竹韵/夜宴），对比度全过 WCAG AA |
| [`chinese-work-report`](skills/chinese-work-report/) | 周报 / 述职 / 项目汇报，讲清楚做了什么、结果如何、下一步 |
| [`ecommerce-copywriting`](skills/ecommerce-copywriting/) | 电商文案，内置《广告法》违禁词红线。**不编造**材质、成分、认证参数 |
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
| 🇨🇳 中文原创仓库 | 58 |
| 📄 官方（anthropics/skills） | 17 |
| ✍️ 本站原创 | 11 |
| **合计** | **129** |

**[→ 看完整清单 SKILLS.md](SKILLS.md)**（每天从数据自动重建，不会和实际对不上）

另附 **47 个 AI 工具导航**，链接每日自动实测。

---

## 🔄 每天自动做的事

| 步骤 | 做什么 |
|------|--------|
| 1 | 今日工具推荐 |
| 2 | 核对 [SOURCES.md](SOURCES.md) 里各家 AI 官方公告页链接 |
| 3 | 47 个工具链接实测可访问性 |
| 4 | **129 个 skill 仓库复检**：还在不在、星数、最后更新时间 |
| 5 | 从数据重建 SKILLS.md |

最近复检：**2026-08-07**，失效 0 个。
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

详见 [内容准则与维护说明.md](内容准则与维护说明.md)。

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

---

## 贡献

收录有误、链接失效、想推荐新 Skill，欢迎 [提 Issue](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues)
或看 [CONTRIBUTING.md](CONTRIBUTING.md)。

**发现事实错误请一定告诉我们** —— 这个项目全部的价值就在"可信"两个字上。

---

<div align="center">
<sub>MIT License · 数据最后复检 2026-08-07 · README 由脚本从实际数据生成于 2026-08-07</sub>
</div>
