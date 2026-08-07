# 实测数据：15 个高增长仓库的仓库门面

> 采集时间 2026-08-07，用 GitHub REST API。
> **样本是"已经火了的"，存在幸存者偏差，下面所有数字都只是相关性。**

## 样本与筛选

从 GitHub 搜索近 60–180 天创建、星数较高的仓库中取 15 个，
覆盖英文/中文、工具/列表/Skill 三类。**没有对照组**——
用同样结构但没火的仓库拿不到（GitHub 搜索按星排序，低星的搜不到）。
这是这份数据最大的局限。

## 一、结构特征

| 仓库 | 星/天 | README | 图 | 首屏图 | 徽章 | 首屏demo | 首屏装 |
|------|------:|-------:|---:|------:|:----:|:-------:|:-----:|
| DietrichGebert/ponytail | 1751 | 19KB | 13 | 7 | ✅ | | |
| KKKKhazix/human-writing | 920 | 5KB | 4 | 4 | ✅ | | ✅ |
| img2threejs/img2threejs | 441 | 26KB | 16 | 9 | ✅ | | |
| thebuggeddev/anatomy | 389 | 3KB | 0 | 0 | | | ✅ |
| mshumer/Claude-of-Duty | 227 | 6KB | 0 | 0 | | | ✅ |
| ayghri/i-have-adhd | 210 | 3KB | 2 | 2 | ✅ | | |
| Donchitos/Claude-Code-Game-Studios | 135 | 15KB | 10 | 7 | ✅ | | |
| helloianneo/ian-xiaohei-illustrations | 127 | 8KB | 9 | 0 | | | |
| freestylefly/awesome-gpt-image-2 | 95 | 32KB | 49 | 6 | ✅ | | |
| laoma2053/awesome-zhuiju-free | 86 | 42KB | 30 | 4 | ✅ | ✅ | |
| isjiamu/gzh-design-skill | 78 | 19KB | 20 | 5 | ✅ | | ✅ |
| vinhhien112/img2obj | 54 | 7KB | 4 | 2 | | ✅ | |
| jnMetaCode/superpowers-zh | 54 | 26KB | 10 | 5 | ✅ | | |
| agiwhitelist/auteur | 33 | 14KB | 17 | 6 | ✅ | ✅ | |
| VoltAgent/awesome-claude-design | 30 | 15KB | 8 | 5 | ✅ | | |

**汇总**

- 首屏有图 **12/15**
- 首屏有徽章 **11/15**
- 首屏有安装命令 4/15
- 首屏能点到 demo 3/15
- 标题用中文 2/15
- README 中位数 **15 KB**，图片中位数 **10 张**
- 仓库名长度中位数 **14 字符**，topics 中位数 **9 个**

**一个反直觉的点**：`VoltAgent/awesome-claude-design` 全仓库只有 **2 个文件、16 KB**，
拿到 3,349 星。体量和结果没有明显关系，**定位清不清楚更重要**。

## 二、作者影响力（判断"打法可复制性"的关键）

| 仓库 | 星 | 作者粉丝 | 账号年龄 | 公开库 |
|------|---:|--------:|--------:|------:|
| DietrichGebert/ponytail | 98,055 | 1,414 | 3年 | 3 |
| Donchitos/Claude-Code-Game-Studios | 23,684 | 262 | 2年 | 1 |
| ayghri/i-have-adhd | 18,031 | 183 | 8年 | 78 |
| img2threejs/img2threejs | 10,150 | 64 | 0年 | 4 |
| freestylefly/awesome-gpt-image-2 | 9,855 | 1,479 | 7年 | 81 |
| helloianneo/ian-xiaohei-illustrations | 9,150 | 488 | 4年 | 6 |
| jnMetaCode/superpowers-zh | 7,541 | 715 | 11年 | 122 |
| **laoma2053/awesome-zhuiju-free** | **5,438** | **47** | 2年 | 23 |
| VoltAgent/awesome-claude-design | 3,349 | 3,774 | 1年 | 19 |
| mshumer/Claude-of-Duty | 2,949 | 1,730 | 8年 | 41 |
| isjiamu/gzh-design-skill | 2,901 | 73 | 9年 | 32 |
| thebuggeddev/anatomy | 1,944 | 512 | 0年 | 71 |
| KKKKhazix/human-writing | 1,841 | 2,963 | 0年 | 3 |
| **vinhhien112/img2obj** | **1,566** | **14** | 8年 | 4 |
| **agiwhitelist/auteur** | **901** | **4** | 0年 | 10 |

**分布**

```
0–50 粉（素人）      3 个  ███
50–500 粉           5 个  █████
500–5000 粉         7 个  ███████
5000+ 粉（大 V）      0 个
```

**读法**：
- 没有一个是大 V，说明这不是"名人效应"游戏
- 但 12/15 有 50 粉以上，说明"完全零基础"是少数（3/15 = 20%）
- 最鼓舞人的样本是 `laoma2053`：**47 个粉丝，做到 5,438 星**

## 三、测不到的（重要）

**stargazer 时间线全部 404。**

尝试用 `/repos/{owner}/{repo}/stargazers` 配 `application/vnd.github.star+json`
拉前 100 个 star 的时间戳，想据此判断是"一夜爆发"（≈外部推荐）还是"持续增长"（≈内容驱动）。
对自己的仓库可以，对别人的仓库**一律 404**。

**后果**：无法区分某个仓库是靠 README 好，还是靠某个大号转发。
这是"打法"最核心的因果问题，而这份数据回答不了。

## 四、采集方法（可复现）

```
GET /search/repositories?q=created:>YYYY-MM-DD stars:>N&sort=stars
GET /repos/{full}                → 星数、创建时间、描述、topics、license
GET /users/{owner}               → 粉丝数、账号年龄、公开库数
GET /repos/{full}/readme         → README 原文，取前 1200 字符作为"首屏"
GET /repos/{full}/git/trees/{branch}?recursive=1  → 文件构成
```

"首屏"定义为 README 前 1200 字符——对应 GitHub 上大约不滚动能看到的高度。
这是个近似值，实际取决于窗口大小和内容密度。
