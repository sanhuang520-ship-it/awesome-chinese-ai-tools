#!/usr/bin/env python3
"""Generate the evidence-only RSS feed from committed repository data."""

import argparse
import html
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "feed.xml"
BASE = "https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/"


def outcome_counts():
    data = json.loads((ROOT / "data" / "compatibility.json").read_text(encoding="utf-8"))
    results = data["results"]["codexActivation"]["skillResults"].values()
    return Counter(result["outcome"] for result in results)


def item(title, path, pub_date, description, guid=None):
    url = BASE + path
    guid_url = guid or url
    return f'''    <item>
      <title>{html.escape(title)}</title>
      <link>{url}</link>
      <guid isPermaLink="{'true' if guid is None else 'false'}">{guid_url}</guid>
      <pubDate>{pub_date}</pubDate>
      <description><![CDATA[
        <p>{description}</p>
      ]]></description>
    </item>'''


def render_feed():
    counts = outcome_counts()
    if counts != {"completed": 10, "waiting-input": 1, "bounded-retest": 2}:
        raise ValueError(f"unexpected compatibility outcome totals: {dict(counts)}")
    entries = [
        item(
            "chinese-design-md 前瞻复测：茶品牌选型 4/4 门槛通过",
            "cases/chinese-design-md-prospective-retest-2026-08-13.md",
            "Thu, 13 Aug 2026 11:06:00 +0800",
            "在只含单个 Skill 的隔离 Codex 项目中执行运行前公开任务；未点名 Skill 时主动读取现有方案，只推荐宋韵与新中式并解释差异，只问一个决策问题，项目未被修改。结果不外推为视觉质量或跨客户端认证。",
        ),
        item(
            "book-digest-cn 前瞻复测：无原文时 4/4 门槛通过",
            "cases/book-digest-cn-prospective-retest-2026-08-13.md",
            "Thu, 13 Aug 2026 10:51:00 +0800",
            "任务与四项成功门槛先公开，再在只含单个 Skill 的隔离 Codex 项目中执行；未点名 Skill 时主动读取，询问必要材料，只给空白三层骨架且未修改项目。结果仅限所记录的客户端、模型、任务与环境。",
        ),
        item(
            "Agent Skill 怎么更新：skills update 项目级实测",
            "update-agent-skill/",
            "Thu, 13 Aug 2026 10:10:00 +0800",
            "在有 skills-lock.json 的隔离项目中，13 个受控历史夹具经 skills CLI 1.5.22 更新后与当前公开仓库完整一致，全局 Skill 文件哈希未变；不外推到全局更新或无锁场景。",
        ),
        item(
            "skills CLI 1.5.22 隔离安装与项目更新复测：13/13 一致",
            "cases/skills-cli-isolated-install-2026-08-13.md",
            "Thu, 13 Aug 2026 00:51:00 +0800",
            "在临时 Git 项目复制安装 13 个原创 Skill，全部与当前仓库逐字一致；再用受控历史夹具验证 13/13 项目副本可更新到当前完整文件夹，全局 Skill 哈希未变。同时公开旧全局副本 0/13 当前一致，说明安装不会持续同步。",
        ),
        item(
            "Agent Skill 安装前安全检查：只读本地审计器",
            "audit-skill/",
            "Thu, 13 Aug 2026 00:36:00 +0800",
            "开源 Python 工具只读检查脚本、符号链接、联网、凭据词、文件写删和高风险命令；不执行目标 Skill，也不把规则命中包装成安全认证。",
        ),
        item(
            "如何创建 Codex Skill：从 SKILL.md 到自动触发",
            "create-codex-skill/",
            "Wed, 12 Aug 2026 23:52:00 +0800",
            "按 OpenAI 当前文档从成功工作流开始，创建最小 SKILL.md，写清触发范围，按需拆分资源，再验证发现、自动选择和最终交付。",
        ),
        item(
            "Codex Skill 安装了却不触发？5 步定位",
            "codex-skill-not-triggering/",
            "Wed, 12 Aug 2026 23:58:00 +0800",
            "按 CLI 发现、文件落盘、客户端读取、任务完成和环境阻断逐层排查，连接可复制命令、逐字实测与隐私优先的本地报告生成器。",
        ),
        item(
            "Agent Skills 兼容性怎么测试：四层证据法",
            "method/",
            "Wed, 12 Aug 2026 23:28:00 +0800",
            "公开区分 CLI 发现、文件安装、自动触发与任务完成的测试协议，并给出逐字任务模板、失败分类和环境阻断边界。",
        ),
        item(
            "13 个原创中文 Agent Skills 方法与证据总览",
            "guides/",
            "Wed, 12 Aug 2026 22:55:00 +0800",
            "按使用场景连接 13 个原创 Skill 的方法说明、Codex 实测状态、原始案例和质量边界；10 项当次任务完成，1 项按流程等待必要输入，2 项大任务失败后缩小复测通过。",
        ),
        item(
            "13 个原创 Skill 均已具备独立说明页",
            "guides/",
            "Wed, 12 Aug 2026 22:37:00 +0800",
            "每个本站原创 Skill 均有独立的方法与证据页面，并接入完整社交分享卡、结构化数据和站内链接；页面不把单次任务结果外推为准确率或认证。",
            "urn:awesome-chinese-ai-tools:update:first-party-explainers:2026-08-12",
        ),
        item(
            "13 个中文 Agent Skills 的 Codex 自动触发实测",
            "compatibility/",
            "Wed, 12 Aug 2026 18:38:00 +0800",
            "13/13 在未点名 Skill 的任务中发生自动触发；任务完成、等待必要输入与缩小复测分别记录。7 条保留逐字任务原文，6 条仅保留摘要，失败和证据边界均公开。",
        ),
        item(
            "本站原创 Skills 增加静态质量与安全标签",
            "QUALITY.md",
            "Wed, 12 Aug 2026 17:58:00 +0800",
            "公开 13 个原创 Skill 的脚本、运行时网络、凭据和写文件能力静态检查结果；明确这不是正式安全认证。",
        ),
    ]
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>中文 AI Skills 库 — 可验证更新</title>
    <link>{BASE}</link>
    <description>只发布 Agent Skills 实测、维护记录和可复核的数据更新；不转述 AI 新闻，不自动生成工具推荐。</description>
    <language>zh-CN</language>
    <lastBuildDate>Thu, 13 Aug 2026 11:06:00 +0800</lastBuildDate>
    <atom:link href="{BASE}feed.xml" rel="self" type="application/rss+xml"/>

{chr(10).join(entries)}
  </channel>
</rss>
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    expected = render_feed()
    current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
    if args.write:
        OUTPUT.write_text(expected, encoding="utf-8")
    elif current != expected:
        raise SystemExit("feed.xml is stale; run scripts/sync_feed.py --write")


if __name__ == "__main__":
    main()
