# 90 天维护计划

> 目标：建立活跃的 GitHub 仓库历史，为申请 OpenAI 研究员/开发者资格提供参考

## 时间线

### Week 1-2：打基础（Day 1–14）
- [x] 创建仓库，提交初始 README
- [ ] 补充 LICENSE 文件（CC0 1.0）
- [ ] 添加 GitHub Actions：每周自动检查死链
- [ ] 创建 `issues` 模板（新工具建议、信息更新）
- [ ] 在相关社区发布（V2EX、少数派、掘金）

### Week 3-4：内容扩充（Day 15–30）
- [ ] 每天新增 1-2 个工具（保持 commit 连续性）
- [ ] 补充「本地部署」分类（Ollama、LM Studio 等）
- [ ] 补充「API 聚合平台」分类
- [ ] 写第一篇配套博客（可发到掘金/少数派）

### Month 2：社区建设（Day 31–60）
- [ ] 回应所有 Issues 和 PR，响应时间 < 24h
- [ ] 添加「月度更新日志」（每月1日发 Release）
- [ ] 在 README 添加社区讨论入口（Discussions）
- [ ] 联系 2-3 个相关项目互相 star/引用

### Month 3：申请准备（Day 61–90）
- [ ] 整理项目数据：star 数、PR 数、commit 数
- [ ] 写项目总结文档（impact statement）
- [ ] 截图保存活跃度证明
- [ ] Day 90：提交 OpenAI API 申请

---

## 每日维护 Checklist（5-10 分钟）

```
[ ] 检查是否有新 Issue/PR
[ ] 验证一个工具的免费额度是否变化
[ ] 如有变化，更新并 commit（哪怕只改一行）
[ ] 可选：在 Twitter/X 分享一个工具推荐
```

---

## OpenAI API 申请英文模板

> 适用场景：申请 OpenAI API 访问权限时的 use case 说明

---

**Subject:** API Access Request – AI Tools Directory for Chinese Developers

**Use Case Description:**

I am the maintainer of **Awesome Chinese AI Tools** (github.com/sanhuang520-ship-it/awesome-chinese-ai-tools), an open-source directory cataloging 100+ AI tools with a focus on free tiers, Chinese language support, and accessibility for developers in China.

I am requesting API access to:

1. **Automate tool verification** — Use the API to periodically validate tool availability and pricing accuracy across the directory
2. **Generate structured comparisons** — Build a comparison engine that helps users find the best tool for their specific use case using natural language queries
3. **Community Q&A** — Power a GitHub Discussions bot that answers questions about tool selection based on the directory content

**Project Details:**
- Repository: github.com/sanhuang520-ship-it/awesome-chinese-ai-tools
- Stars: [X] | Commits: [X] | Contributors: [X]
- Active since: [start date]
- Community: [link to discussions/issues]

**Expected Usage:**
- Volume: ~500–1,000 API calls/day
- Models: GPT-4o mini for cost efficiency, GPT-4o for complex comparisons
- No user data collection, fully open-source implementation

I am committed to responsible API use and am happy to share my implementation code upon request.

Thank you for considering my application.

[Your Name]
[GitHub Profile]
[Optional: Twitter/LinkedIn]

---

## 有用的资源

- [GitHub README Badges](https://shields.io)
- [Awesome Lint](https://github.com/sindresorhus/awesome-lint) — 检查你的列表是否符合 Awesome 规范
- [All Contributors](https://allcontributors.org) — 自动记录贡献者
- [Keepachangelog](https://keepachangelog.com/zh-CN) — 更新日志格式规范
