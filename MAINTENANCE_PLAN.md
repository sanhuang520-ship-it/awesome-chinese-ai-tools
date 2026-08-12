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
- [x] 发布安装排错页，区分 CLI 发现、落盘、自动触发和任务完成。
- [ ] 记录用户真实报告的成功安装和兼容性问题，不根据 Clone 或 Star 推断实际使用。

### 3. 搜索与内容入口

- [x] 发布 Codex 兼容性实测页与 Agent Skills 安装排错页。
- [ ] 继续为高需求原创 Skill 建立独立说明页，包含用途、边界、安装、真实输出和常见问题；当前已发布 6 个：[中文排版](typography/)、[中式设计系统](design/)、[国潮视觉](guochao/)、[README 审查](readme-audit/)、[中文职场汇报](work-report/)和[中文电商文案校样](ecommerce-copywriting/)。
- [ ] 接入站长工具并提交 Sitemap，记录收录数、搜索展示和点击基线。
- [ ] 每月发布一篇基于可复现实测的长效文章，不转述无法核实的 AI 新闻。

## 如何贡献

- 发现失效链接、事实错误或安装问题：[提交 Issue](https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools/issues/new/choose)。
- 推荐 Skill 或工具：请提供干净官网链接，并按 [CONTRIBUTING.md](CONTRIBUTING.md) 说明来源和利益相关。
- 只接受可复核的数据与使用案例；如果一项结论仅是推断，请明确标注。
