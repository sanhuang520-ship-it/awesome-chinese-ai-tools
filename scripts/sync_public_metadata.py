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

CAT_ORDER = ["cn", "doc", "ppt", "dev", "agent", "design", "biz", "data", "sec", "3d", "game"]


def build_stats(skills_data, tools_data):
    skills = skills_data.get("skills", [])
    return {
        "skills": len(skills),
        "cn": sum(1 for item in skills if item.get("cat") == "cn"),
        "ours": sum(1 for item in skills if item.get("ours")),
        "official": sum(1 for item in skills if item.get("official")),
        "tools": len(tools_data.get("tools", [])),
        "checked": skills_data.get("skillsCheckedAt") or datetime.date.today().isoformat(),
    }


def sync_readme_text(body, stats):
    """只同步 README 里的可计算统计，不改手写介绍。"""
    n, cn, ours = stats["skills"], stats["cn"], stats["ours"]
    official, tools, checked = stats["official"], stats["tools"], stats["checked"]
    today = datetime.date.today().isoformat()
    replacements = [
        (r"Skills-\d+%20个-", f"Skills-{n}%20个-"),
        (r"本站原创-\d+%20个-", f"本站原创-{ours}%20个-"),
        (r"① \d+ 个 Skill 是我们自己写的", f"① {ours} 个 Skill 是我们自己写的"),
        (r"② \d+ 个仓库\*\*每天自动复检\*\*", f"② {n} 个仓库**每天自动复检**"),
        (r"本站原创 Skill（\d+ 个）", f"本站原创 Skill（{ours} 个）"),
        (r"\| 🇨🇳 中文原创仓库 \| \d+ \|", f"| 🇨🇳 中文原创仓库 | {cn} |"),
        (r"\| 📄 官方（anthropics/skills） \| \d+ \|", f"| 📄 官方收录 | {official} |"),
        (r"\| 📄 官方收录 \| \d+ \|", f"| 📄 官方收录 | {official} |"),
        (r"\| ✍️ 本站原创 \| \d+ \|", f"| ✍️ 本站原创 | {ours} |"),
        (r"\| \*\*合计\*\* \| \*\*\d+\*\* \|", f"| **合计** | **{n}** |"),
        (r"另附 \*\*\d+ 个 AI 工具导航\*\*", f"另附 **{tools} 个 AI 工具导航**"),
        (r"\| (\d+) \| \d+ 个工具链接实测可访问性 \|", rf"| \1 | {tools} 个工具链接实测可访问性 |"),
        (r"\| 4 \| \*\*\d+ 个 skill 仓库复检\*\*", f"| 4 | **{n} 个 skill 仓库复检**"),
        (r"最近复检：\*\*\d{4}-\d{2}-\d{2}\*\*", f"最近复检：**{checked}**"),
        (
            r"MIT License · 数据最后复检 \d{4}-\d{2}-\d{2} · README 由脚本从实际数据生成于 \d{4}-\d{2}-\d{2}",
            f"MIT License · 数据最后复检 {checked} · 公开统计由脚本同步于 {today}",
        ),
        (
            r"MIT License · 数据最后复检 \d{4}-\d{2}-\d{2} · 公开统计由脚本同步于 \d{4}-\d{2}-\d{2}",
            f"MIT License · 数据最后复检 {checked} · 公开统计由脚本同步于 {today}",
        ),
    ]
    for pattern, value in replacements:
        body = re.sub(pattern, value, body)
    return body


def sync_index_text(body, stats):
    """同步首页 SEO 元数据和 JSON-LD。"""
    n, cn, ours = stats["skills"], stats["cn"], stats["ours"]
    tools, checked = stats["tools"], stats["checked"]
    title = f"中文 AI Skills 库 — {n} 个技能包，{ours} 个本站原创 | 每日自动复检"
    desc = (
        f"面向中文用户的 AI Agent Skills 合集：{n} 个技能包，"
        f"其中 {cn} 个中文项目、{ours} 个本站自写 Skill；"
        f"每天自动复检仓库是否失效，另附 {tools} 个 AI 工具导航。"
    )
    short_desc = f"{n} 个 AI 技能包，{ours} 个本站自写。每日自动复检，GitHub Actions 记录公开可查。"

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
                        f"本站收录了 {cn} 个中文 Skill 项目，其中有 {ours} 个本站自写 Skill。"
                        "全部经 GitHub API 验证仓库真实存在，并每天自动复检。"
                    )
    new_json = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    return body[: match.start()] + match.group(1) + new_json + match.group(3) + body[match.end() :]


def sync_sitemap_text(body, checked):
    """仅更新随数据变化的核心页，不伪造其他页面的时间。"""
    base = "https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/"
    core = {base, base + "SKILLS.md", base + "README.md"}
    lines = []
    for line in body.splitlines():
        loc = re.search(r"<loc>(.*?)</loc>", line)
        if loc and loc.group(1) in core:
            line = re.sub(
                r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>",
                f"<lastmod>{checked}</lastmod>",
                line,
            )
        lines.append(line)
    return "\n".join(lines) + ("\n" if body.endswith("\n") else "")


def sync_llms_text(body, stats):
    """同步供语言模型读取的顶层项目统计。"""
    n, ours, tools = stats["skills"], stats["ours"], stats["tools"]
    body = re.sub(r"收录 \d+ 个 Skill", f"收录 {n} 个 Skill", body, count=1)
    body = re.sub(r"其中 \d+ 个由本仓库维护", f"其中 {ours} 个由本仓库维护", body, count=1)
    body = re.sub(r"另有 \d+ 个 AI 工具入口", f"另有 {tools} 个 AI 工具入口", body, count=1)
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


def sync_public_metadata(github_api, repo):
    skills_body, _ = _repo_text(github_api, repo, "data/skills.json")
    tools_body, _ = _repo_text(github_api, repo, "data/tools.json")
    stats = build_stats(json.loads(skills_body), json.loads(tools_body))
    message = f"seo: 同步 {stats['skills']} 个 skill / {stats['ours']} 原创的公开统计"
    transforms = {
        "README.md": lambda text: sync_readme_text(text, stats),
        "index.html": lambda text: sync_index_text(text, stats),
        "llms.txt": lambda text: sync_llms_text(text, stats),
        "sitemap.xml": lambda text: sync_sitemap_text(text, stats["checked"]),
    }
    for path, transform in transforms.items():
        current, sha = _repo_text(github_api, repo, path)
        _put_if_changed(github_api, repo, path, current, transform(current), sha, message)


def sync_local(root, write=False):
    """计算本地公开统计差异；仅在 write=True 时写回文件。"""
    root = Path(root)
    skills_data = json.loads((root / "data/skills.json").read_text(encoding="utf-8"))
    tools_data = json.loads((root / "data/tools.json").read_text(encoding="utf-8"))
    stats = build_stats(skills_data, tools_data)
    transforms = {
        "README.md": lambda text: sync_readme_text(text, stats),
        "index.html": lambda text: sync_index_text(text, stats),
        "llms.txt": lambda text: sync_llms_text(text, stats),
        "sitemap.xml": lambda text: sync_sitemap_text(text, stats["checked"]),
    }
    changed = []
    for relative, transform in transforms.items():
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
