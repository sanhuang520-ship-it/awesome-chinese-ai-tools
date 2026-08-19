#!/usr/bin/env python3
"""从 data/*.json 同步 README、首页 SEO 元数据与 Sitemap 中的公开统计。

这些函数保持为纯文本变换，便于本地测试；GitHub 读写由 daily_check.py
注入，脚本本身不接触 token。
"""

import base64
import datetime
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

CAT_ORDER = ["cn", "doc", "ppt", "dev", "agent", "design", "biz", "data", "sec", "3d", "game"]


def build_stats(skills_data, tools_data):
    skills = skills_data.get("skills", [])
    repos = {
        "/".join(urlsplit(item.get("url", "")).path.strip("/").split("/")[:2]).lower()
        for item in skills
        if urlsplit(item.get("url", "")).netloc.lower() == "github.com"
    }
    tools = tools_data.get("tools", [])
    return {
        "skills": len(skills),
        "repos": len(repos),
        "cn": sum(1 for item in skills if item.get("cat") == "cn"),
        "ours": sum(1 for item in skills if item.get("ours")),
        "official": sum(1 for item in skills if item.get("official")),
        "tools": len(tools),
        "tools_direct_ok": sum(1 for item in tools if item.get("linkStatus") == "ok"),
        "tools_bot_blocked": sum(1 for item in tools if item.get("linkStatus") == "ok_bot_blocked"),
        "tools_whitelisted": sum(1 for item in tools if item.get("linkStatus") == "ok_whitelisted"),
        "checked": skills_data.get("skillsCheckedAt") or datetime.date.today().isoformat(),
    }


def sync_readme_text(body, stats):
    """只同步 README 里的可计算统计，不改手写介绍。"""
    original_body = body
    n, repos, cn, ours = stats["skills"], stats["repos"], stats["cn"], stats["ours"]
    official, tools, checked = stats["official"], stats["tools"], stats["checked"]
    direct_ok, bot_blocked, whitelisted = stats["tools_direct_ok"], stats["tools_bot_blocked"], stats["tools_whitelisted"]
    today = datetime.date.today().isoformat()
    replacements = [
        (r"Skills-\d+%20个-", f"Skills-{n}%20个-"),
        (r"本站原创-\d+%20个-", f"本站原创-{ours}%20个-"),
        (r"① \d+ 个 Skill 是我们自己写的", f"① {ours} 个 Skill 是我们自己写的"),
        (
            r"③ (?:\d+ 个仓库|\d+ 个 Skill 条目来自 \d+ 个仓库，来源仓库)\*\*(?:每天自动复检|定期复检)\*\*一次还在不在(?:（最近 \d{4}-\d{2}-\d{2}）)?",
            f"③ {n} 个 Skill 条目来自 {repos} 个仓库，来源仓库**定期复检**一次还在不在（最近 {checked}）",
        ),
        (r"本站原创 Skill（\d+ 个）", f"本站原创 Skill（{ours} 个）"),
        (r"\| 🇨🇳 (?:中文原创仓库|中文 Skill 条目) \| \d+ \|", f"| 🇨🇳 中文 Skill 条目 | {cn} |"),
        (r"\| 📄 官方（anthropics/skills） \| \d+ \|", f"| 📄 官方收录 | {official} |"),
        (r"\| 📄 (?:官方收录|官方 Skill 条目) \| \d+ \|", f"| 📄 官方 Skill 条目 | {official} |"),
        (r"\| ✍️ 本站原创 \| \d+ \|", f"| ✍️ 本站原创 | {ours} |"),
        (r"\| \*\*合计\*\* \| \*\*\d+\*\* \|", f"| **合计** | **{n}** |"),
        (r"另附 \*\*\d+ 个 AI 工具导航\*\*", f"另附 **{tools} 个 AI 工具导航**"),
        (
            r"\| (\d+) \| (?:\d+ 个工具链接实测可访问性|\d+ 个工具入口复检：[^|]+) \|",
            rf"| \1 | {tools} 个工具入口复检：{direct_ok} 个直接成功，{bot_blocked} 个返回机器人拦截响应，{whitelisted} 个白名单跳过请求 |",
        ),
        (
            r"\| (\d+) \| \*\*(?:\d+ 个 Skill 仓库复检|\d+ 个来源仓库复检\*\*（覆盖 \d+ 个 Skill 条目）)",
            rf"| \1 | **{repos} 个来源仓库复检**（覆盖 {n} 个 Skill 条目）",
        ),
        (r"最近复检：\*\*\d{4}-\d{2}-\d{2}\*\*", f"最近复检：**{checked}**"),
        # 页脚的两个日期不在这里处理，见下方——"同步于"那个日期只在内容真的
        # 变了才前移，否则每过一天就会跟自己对不上。
    ]
    for pattern, value in replacements:
        body = re.sub(pattern, value, body)

    # 迁移旧措辞，统一成"公开统计由脚本同步于"
    body = re.sub(
        r"MIT License · 数据最后复检 \d{4}-\d{2}-\d{2} · README 由脚本从实际数据生成于 (\d{4}-\d{2}-\d{2})",
        rf"MIT License · 数据最后复检 {checked} · 公开统计由脚本同步于 \1",
        body,
    )
    # 数据复检日期直接来自数据文件，照实写
    body = re.sub(
        r"(MIT License · 数据最后复检 )\d{4}-\d{2}-\d{2}( · 公开统计由脚本同步于 )",
        rf"\g<1>{checked}\g<2>",
        body,
    )

    # "公开统计由脚本同步于"只在这次同步真的改了东西时才前移到今天。
    #
    # 原来无条件写 today()，有两个问题：
    # ① 每过一天，已提交的 README 就和重新生成的结果对不上，
    #    test_committed_files_are_in_sync 会无缘无故报红（去掉 cron 之后尤其明显）；
    # ② 更要紧的是，一个「什么都没变也照样往前跳」的日期是误导——
    #    读者看到今天的日期会以为当天做过核对，其实数据可能是几天前的。
    if body != original_body:
        body = re.sub(
            r"(公开统计由脚本同步于 )\d{4}-\d{2}-\d{2}",
            rf"\g<1>{today}",
            body,
        )
    return body


def sync_index_text(body, stats):
    """同步首页 SEO 元数据和 JSON-LD。"""
    n, repos, cn, ours = stats["skills"], stats["repos"], stats["cn"], stats["ours"]
    tools, checked = stats["tools"], stats["checked"]
    title = f"Chinese Agent Skills / 中文 AI Skills 库 — {n} 个技能包，{ours} 个本站原创"
    desc = (
        f"Chinese Agent Skills / 中文 AI Skills 合集：{n} 个 Skill 条目，"
        f"其中 {cn} 个中文条目、{ours} 个本站自写 Skill，来自 {repos} 个来源仓库；"
        f"定期复检来源仓库是否失效，另附 {tools} 个 AI 工具导航。"
    )
    short_desc = f"Chinese AI Skills directory：{n} 个 Skill 条目，{ours} 个本站自写；定期复检，兼容性证据与失败边界公开。"

    body = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", body, count=1)
    body = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{desc}">',
        body,
        count=1,
    )
    for prop in ("og:title", "twitter:title"):
        body = re.sub(
            fr'<meta (?:property|name)="{re.escape(prop)}" content="[^"]*">',
            lambda match: re.sub(r'content="[^"]*"', f'content="{title}"', match.group(0)),
            body,
            count=1,
        )
    for prop in ("og:description", "twitter:description"):
        body = re.sub(
            fr'<meta (?:property|name)="{re.escape(prop)}" content="[^"]*">',
            lambda match: re.sub(r'content="[^"]*"', f'content="{short_desc}"', match.group(0)),
            body,
            count=1,
        )

    match = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', body, re.S)
    if not match:
        raise ValueError("首页缺少 JSON-LD")
    graph = json.loads(match.group(2))
    for item in graph.get("@graph", []):
        if item.get("@type") == "WebSite":
            item["description"] = short_desc
        elif item.get("@type") == "Dataset":
            item["name"] = f"AI Agent Skills 中文合集（{n} 个）"
            item["description"] = desc
            item["dateModified"] = checked
        elif item.get("@type") == "FAQPage":
            for question in item.get("mainEntity", []):
                if question.get("name") == "有哪些中文的 Claude Skills？":
                    question["acceptedAnswer"]["text"] = (
                        f"本站收录了 {cn} 个中文 Skill 条目，其中有 {ours} 个本站自写 Skill。"
                        f"这些条目来自 {repos} 个来源仓库，来源仓库经 GitHub API 核验并定期复检。"
                    )
    new_json = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    return body[: match.start()] + match.group(1) + new_json + match.group(3) + body[match.end() :]


def sync_sitemap_text(body, checked):
    """核心页 lastmod 只向前推进，避免数据日期覆盖更晚的内容更新。"""
    base = "https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/"
    core = {base, base + "SKILLS.md", base + "README.md", base + "README.en.md"}
    lines = []
    for line in body.splitlines():
        loc = re.search(r"<loc>(.*?)</loc>", line)
        if loc and loc.group(1) in core:
            lastmod = re.search(r"<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>", line)
            if not lastmod:
                raise ValueError(f"核心 Sitemap 条目缺少 lastmod：{loc.group(1)}")
            newest = max(lastmod.group(1), checked)
            line = line[: lastmod.start(1)] + newest + line[lastmod.end(1) :]
        lines.append(line)
    return "\n".join(lines) + ("\n" if body.endswith("\n") else "")


def sync_llms_text(body, stats):
    """同步供语言模型读取的顶层项目统计。"""
    n, ours, tools = stats["skills"], stats["ours"], stats["tools"]
    body = re.sub(r"收录 \d+ 个 Skill", f"收录 {n} 个 Skill", body, count=1)
    body = re.sub(r"其中 \d+ 个由本仓库维护", f"其中 {ours} 个由本仓库维护", body, count=1)
    body = re.sub(r"另有 \d+ 个 AI 工具入口", f"另有 {tools} 个 AI 工具入口", body, count=1)
    return body


def sync_english_readme_text(body, stats):
    """同步英文入口中的目录规模，防止双语数字漂移。"""
    n, repos, ours, tools = stats["skills"], stats["repos"], stats["ours"], stats["tools"]
    body = re.sub(
        r"\d+ Agent Skill entries from \d+ source repositories",
        f"{n} Agent Skill entries from {repos} source repositories",
        body,
    )
    body = re.sub(r"maintains \d+ first-party Skills and \d+ AI tool links", f"maintains {ours} first-party Skills and {tools} AI tool links", body)
    body = re.sub(r"rechecks the \d+ source repositories and \d+ tool links", f"rechecks the {repos} source repositories and {tools} tool links", body)
    return body


def sync_chinese_agent_skills_text(body, stats):
    """
    同步 chinese-agent-skills/index.html 里的计数。

    这一页是纯手写静态页，没有生成脚本，但测试会断言它的数字跟 data/skills.json 一致。
    在接进这里之前，每次增删 Skill 都要人工去改 6 处数字（08-14、08-17 各手改过一轮），
    漏改就等着 CI 报红。这里用跟 README/index.html 同一套正则替换的做法把它纳入自动同步。
    """
    n, repos, ours = stats["skills"], stats["repos"], stats["ours"]
    body = re.sub(
        r"<title>Chinese Agent Skills Directory: \d+ Skills, \d+ Tested First-Party Skills</title>",
        f"<title>Chinese Agent Skills Directory: {n} Skills, {ours} Tested First-Party Skills</title>",
        body,
    )
    body = re.sub(
        r"directory: \d+ entries, \d+ first-party Skills",
        f"directory: {n} entries, {ours} first-party Skills",
        body,
    )
    body = re.sub(
        r"content=\"\d+ Agent Skill entries, \d+ first-party Skills",
        f'content="{n} Agent Skill entries, {ours} first-party Skills',
        body,
    )
    body = re.sub(
        r'<aside class="proof"><strong>\d+</strong>',
        f'<aside class="proof"><strong>{n}</strong>',
        body,
    )
    body = re.sub(
        r"Agent Skill entries from \d+ source repositories",
        f"Agent Skill entries from {repos} source repositories",
        body,
    )
    body = re.sub(
        r"Search and filter \d+ entries by workflow",
        f"Search and filter {n} entries by workflow",
        body,
    )
    body = re.sub(r'"numberOfItems":\d+', f'"numberOfItems":{n}', body)
    return body


def _repo_text(github_api, repo, path):
    info = github_api("GET", f"/repos/{repo}/contents/{path}")
    if "content" not in info:
        raise RuntimeError(f"读取 {path} 失败：{info.get('message', info)}")
    return base64.b64decode(info["content"]).decode("utf-8"), info["sha"]


def _put_if_changed(github_api, repo, path, current, updated, sha, message):
    if current == updated:
        print(f"[{path}] 无变化，跳过")
        return False
    result = github_api(
        "PUT",
        f"/repos/{repo}/contents/{path}",
        {
            "message": message,
            "content": base64.b64encode(updated.encode("utf-8")).decode("ascii"),
            "sha": sha,
            "committer": {"name": "sanhuang520-ship-it", "email": "noreply@github.com"},
        },
    )
    if "content" not in result:
        raise RuntimeError(f"写回 {path} 失败：{result.get('message', result)}")
    print(f"[{path}] ✅ 已同步公开统计")
    return True


def _transforms(stats):
    """
    路径 → 转换函数。API 模式（sync_public_metadata）和本地模式（sync_local）共用同一份，
    以前这张表在两个函数里各写了一遍，加一个文件要记得改两处——漏一处就只在其中一种模式生效。
    """
    return {
        "README.md": lambda text: sync_readme_text(text, stats),
        "README.en.md": lambda text: sync_english_readme_text(text, stats),
        "index.html": lambda text: sync_index_text(text, stats),
        "llms.txt": lambda text: sync_llms_text(text, stats),
        "sitemap.xml": lambda text: sync_sitemap_text(text, stats["checked"]),
        "chinese-agent-skills/index.html": lambda text: sync_chinese_agent_skills_text(text, stats),
    }


def sync_public_metadata(github_api, repo):
    skills_body, _ = _repo_text(github_api, repo, "data/skills.json")
    tools_body, _ = _repo_text(github_api, repo, "data/tools.json")
    stats = build_stats(json.loads(skills_body), json.loads(tools_body))
    message = f"seo: 同步 {stats['skills']} 个 skill / {stats['ours']} 原创的公开统计"
    for path, transform in _transforms(stats).items():
        current, sha = _repo_text(github_api, repo, path)
        _put_if_changed(github_api, repo, path, current, transform(current), sha, message)


def sync_local(root, write=False):
    """计算本地公开统计差异；仅在 write=True 时写回文件。"""
    root = Path(root)
    skills_data = json.loads((root / "data/skills.json").read_text(encoding="utf-8"))
    tools_data = json.loads((root / "data/tools.json").read_text(encoding="utf-8"))
    stats = build_stats(skills_data, tools_data)
    changed = []
    for relative, transform in _transforms(stats).items():
        path = root / relative
        current = path.read_text(encoding="utf-8")
        updated = transform(current)
        if updated != current:
            changed.append(relative)
            if write:
                path.write_text(updated, encoding="utf-8")
    return stats, changed


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="检查或同步 README、首页、llms.txt 与 Sitemap 的公开统计")
    parser.add_argument("root", nargs="?", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--write", action="store_true", help="将计算结果写回；默认只检查且不修改文件")
    args = parser.parse_args()
    local_stats, local_changed = sync_local(args.root, write=args.write)
    mode = "write" if args.write else "check"
    print(json.dumps({"mode": mode, "stats": local_stats, "changed": local_changed}, ensure_ascii=False))
    if local_changed and not args.write:
        raise SystemExit(1)
