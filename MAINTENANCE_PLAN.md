# 公开维护路线图

> 目标：让中文用户更容易发现、安装和安全使用 Agent Skills。
> 原则：只记录真实维护和可验证结果；不做空提交、不互换 Star、不伪造安装量或用户案例。

## 长期维护内容

- 每日复检 Skill 仓库、官方信源和 AI 工具链接。
- 从 `data/skills.json` 重建 `SKILLS.md`，并同步 README、首页 SEO 元数据和 Sitemap 中的公开统计。
- 优先处理失效链接、错误描述、安装问题与安全风险。
- 对本站原创 Skill 维护清晰触发条件、执行边界、示例和可复现输出。

## 接下来 30 天

### 1. 可信度与自动化

- [x] 公开 GitHub Actions 日检记录。
- [x] 建立收录建议 Issue 模板和 PR 自查清单。
- [x] 将每日检查步骤相互隔离，避免单个网络错误中断全部任务。
- [x] 对 README、首页、结构化数据和 Sitemap 增加一致性测试。
- [x] 为公开 HTML、RSS、Sitemap、证据边界增加自动检查。
- [x] 建立变更日志与首个证据化版本标签，后续按月汇总重要维护变化。
- [ ] 在具备 GitHub Actions `workflow` 写入权限后，为 Pull Request 启用只读的 `python3 scripts/verify.py` 自动检查；当前贡献者可按贡献指南在本地运行同一命令。

### 2. 安装与使用验证

- [ ] 在 macOS、Windows 和 Linux 上复测 `npx skills add`，标注 CLI 版本和实际落盘路径。
- [x] 为 13 个本站原创 Skill 记录 Codex 自动触发任务、结果与证据边界。
- [x] 为缺少逐字历史任务的 6 项建立前瞻复测队列，在运行前公开提示和成功门槛；`planned` 不计为兼容通过。
- [x] 发布安装排错页，区分 CLI 发现、落盘、自动触发和任务完成。
- [x] 发布单次兼容性结果 JSON Schema、真实示例与本地校验器，分离环境阻断、自动触发和最终完成状态。
- [ ] 记录用户真实报告的成功安装和兼容性问题，不根据 Clone 或 Star 推断实际使用。
- [x] 建立所有者 Traffic API 聚合快照脚本；只保存浏览、克隆、热门来源与路径计数，不保存 Token、IP 或访客身份，并明确 Clone 不能称为用户。
- [x] 建立 GitHub 公开仓库搜索基线脚本；固定查询、排序与前 20 口径，只记录公开排名和总数，不把变化归因于单次文案或承诺 Star 增长。
- [x] 将 GitHub description、homepage 与 topics 固化为可审查配置，并提供只读公开 API 漂移检查器。

### 3. 搜索与内容入口

- [x] 发布 Codex 兼容性实测页与 Agent Skills 安装排错页。
- [x] 发布 Agent Skills 兼容性四层测试方法，统一发现、安装、自动触发、任务完成与环境阻断的记录口径。
- [x] 提交 Agent-Skills.md 目录并验证 13/13 已生成公开页面；标准格式验证 13/13 通过。分类和标签元数据已补齐，外部目录刷新结果待复核。
- [x] 为 13 个原创 Skill 全部建立独立说明页，包含用途、边界、安装、实测结果或可复现证据：[AI 学习教练](learning/)、[中文拆书与读书笔记](reading/)、[中文中小学教案](lesson-plan/)、[家长辅导作业](homework/)、[中文排版](typography/)、[中式设计系统](design/)、[国潮视觉](guochao/)、[README 审查](readme-audit/)、[中文职场汇报](work-report/)、[中文电商文案校样](ecommerce-copywriting/)、[中式网页主题库](themes/)、[Three.js 水墨 Shader](guofeng-threejs/)和[家庭流水整理](bookkeeping/)。
- [ ] 接入站长工具并提交 Sitemap，记录收录数、搜索展示和点击基线。
- [ ] 每月发布一篇基于可复现实测的长效文章，不转述无法核实的 AI 新闻。

## 如何贡献

- 发现失效链接、事实错误或安装问题：[提交 Issue](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new/choose)。
- 推荐 Skill 或工具：请提供干净官网链接，并按 [CONTRIBUTING.md](CONTRIBUTING.md) 说明来源和利益相关。
- 只接受可复核的数据与使用案例；如果一项结论仅是推断，请明确标注。
