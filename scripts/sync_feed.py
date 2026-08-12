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
    <lastBuildDate>Wed, 12 Aug 2026 23:52:00 +0800</lastBuildDate>
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
