#!/usr/bin/env python3
"""Render a crawlable, no-JavaScript Agent Skills catalog from skills.json."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "skills.json"
OUTPUT_PATH = ROOT / "catalog" / "index.html"
BASE_URL = "https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def safe_http_url(value: object) -> str:
    url = str(value or "").strip()
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Skill URL must be absolute HTTP(S): {url!r}")
    return esc(url)


def render_catalog(data: dict) -> str:
    skills = data.get("skills", [])
    categories = data.get("categories", {})
    if not skills or not categories:
        raise ValueError("skills.json must contain non-empty skills and categories")

    names = [item.get("name") for item in skills]
    if any(not name for name in names) or len(names) != len(set(names)):
        raise ValueError("Every Skill needs a unique non-empty name")

    unknown = sorted({item.get("cat") for item in skills} - set(categories))
    if unknown:
        raise ValueError(f"Unknown categories: {', '.join(map(str, unknown))}")

    checked = str(data.get("skillsCheckedAt") or data.get("updated") or "")
    ours = sum(bool(item.get("ours")) for item in skills)
    category_order = [key for key in categories if any(item.get("cat") == key for item in skills)]

    category_nav = []
    category_sections = []
    position = 0
    list_items = []
    for cat in category_order:
        meta = categories[cat]
        group = sorted(
            (item for item in skills if item.get("cat") == cat),
            key=lambda item: (not bool(item.get("ours")), str(item["name"]).casefold()),
        )
        label = meta.get("label") or cat
        category_nav.append(
            f'<a href="#cat-{esc(cat)}"><b>{esc(label)}</b><span>{len(group)} 个</span></a>'
        )
        cards = []
        for item in group:
            position += 1
            name = esc(item["name"])
            url = safe_http_url(item.get("url"))
            description = esc(item.get("desc") or "上游暂无中文摘要")
            if item.get("ours"):
                source = "本站原创"
                source_class = "ours"
            elif item.get("official"):
                source = "官方"
                source_class = "official"
            else:
                source = "第三方资料"
                source_class = "third-party"
            cards.append(
                '<article class="skill-card">'
                f'<div class="card-top"><span class="source {source_class}">{source}</span>'
                f'<code>{name}</code></div>'
                f'<h3><a href="{url}">{name}</a></h3>'
                f'<p>{description}</p>'
                f'<a class="visit" href="{url}" rel="noopener">查看来源与安装说明 →</a>'
                "</article>"
            )
            list_items.append(
                {"@type": "ListItem", "position": position, "name": str(item["name"]), "url": str(item["url"])}
            )
        category_sections.append(
            f'<section class="category" id="cat-{esc(cat)}">'
            f'<div class="section-head"><div><span>SCENE / {esc(cat.upper())}</span>'
            f'<h2>{esc(label)}</h2></div><b>{len(group)} 个条目</b></div>'
            f'<div class="skill-grid">{"".join(cards)}</div></section>'
        )

    structured = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "中文 Agent Skills 静态目录",
        "description": "无需 JavaScript 即可按场景浏览的 Agent Skills 中文目录。",
        "numberOfItems": len(skills),
        "itemListElement": list_items,
    }
    structured_json = json.dumps(structured, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{len(skills)} 个中文 Agent Skills 静态目录｜按场景浏览</title>
<meta name="description" content="无需 JavaScript，按中文表达、开发、设计、办公、数据、安全等场景浏览 {len(skills)} 个 Agent Skills；标明本站原创、官方与第三方资料边界。">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{BASE_URL}catalog/">
<meta property="og:type" content="website"><meta property="og:locale" content="zh_CN">
<meta property="og:title" content="{len(skills)} 个中文 Agent Skills 静态目录">
<meta property="og:description" content="不用 JavaScript，按真实场景浏览；来源标签不等于兼容或安全认证。">
<meta property="og:url" content="{BASE_URL}catalog/">
<meta property="og:image" content="{BASE_URL}og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="中文 AI Skills 库">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{len(skills)} 个中文 Agent Skills 静态目录"><meta name="twitter:description" content="不用 JavaScript，按真实场景浏览 Agent Skills。"><meta name="twitter:image" content="{BASE_URL}og.png"><meta name="twitter:image:alt" content="中文 AI Skills 库">
<script type="application/ld+json">{structured_json}</script>
<style>
:root{{--paper:#f1eadc;--sheet:#fffaf0;--ink:#19221d;--muted:#5e675f;--line:#c9beaa;--jade:#275f4d;--red:#a74638;--gold:#946719;--blue:#315f78;--mono:ui-monospace,SFMono-Regular,Menlo,monospace;--sans:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;--serif:"Songti SC","Noto Serif CJK SC",serif}}*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.72 var(--sans)}}a{{color:var(--jade)}}.wrap{{width:min(1180px,calc(100% - 38px));margin:auto}}.top{{padding:20px 0;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;font-size:13px}}.top a{{font-weight:800;text-decoration:none}}.top span{{font:11px var(--mono);letter-spacing:.12em;color:var(--muted)}}.hero{{padding:68px 0 45px;display:grid;grid-template-columns:1.2fr .8fr;gap:50px;align-items:end}}.eyebrow,.section-head span{{font:800 11px var(--mono);letter-spacing:.14em;color:var(--red)}}h1,h2{{font-family:var(--serif)}}h1{{font-size:clamp(43px,7vw,78px);line-height:1.05;margin:17px 0;max-width:10em}}.lead{{font-size:20px;color:#455149;max-width:38em}}.proof{{background:var(--sheet);border:1px solid var(--ink);padding:27px;box-shadow:9px 9px 0 rgba(39,95,77,.18)}}.proof b{{display:block;font:700 38px var(--serif);color:var(--jade)}}.proof p{{color:var(--muted);margin:5px 0 0}}.notice{{border-block:1px solid var(--line);background:rgba(255,250,240,.65);padding:21px 0}}.notice p{{margin:0}}.category-nav{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding:38px 0 22px}}.category-nav a{{display:flex;justify-content:space-between;gap:12px;background:var(--sheet);border:1px solid var(--line);padding:14px;text-decoration:none}}.category-nav span{{color:var(--muted);white-space:nowrap}}.category{{padding:42px 0;border-top:1px solid var(--line);scroll-margin-top:12px}}.section-head{{display:flex;justify-content:space-between;gap:22px;align-items:end;margin-bottom:22px}}.section-head h2{{font-size:clamp(31px,5vw,48px);margin:4px 0 0}}.section-head>b{{color:var(--muted)}}.skill-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}.skill-card{{background:var(--sheet);border:1px solid var(--line);padding:20px;min-height:260px;display:flex;flex-direction:column}}.card-top{{display:flex;align-items:center;justify-content:space-between;gap:10px}}.card-top code{{font:11px var(--mono);color:var(--muted);overflow-wrap:anywhere}}.source{{font:800 10px var(--mono);padding:4px 6px;border:1px solid;white-space:nowrap}}.source.ours{{color:var(--red)}}.source.official{{color:var(--blue)}}.source.third-party{{color:var(--gold)}}.skill-card h3{{font-size:20px;line-height:1.3;margin:16px 0 8px;overflow-wrap:anywhere}}.skill-card h3 a{{color:var(--ink);text-decoration:none}}.skill-card p{{font-size:14px;color:var(--muted);margin:0 0 18px}}.visit{{margin-top:auto;font-size:12px;font-weight:800}}footer{{padding:38px 0 55px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;color:var(--muted);font-size:13px}}@media(max-width:850px){{.hero{{grid-template-columns:1fr}}.skill-grid{{grid-template-columns:1fr 1fr}}.category-nav{{grid-template-columns:1fr 1fr}}}}@media(max-width:560px){{.wrap{{width:calc(100% - 26px)}}.skill-grid,.category-nav{{grid-template-columns:1fr}}.section-head{{align-items:start;flex-direction:column}}}}
</style></head>
<body><header class="wrap top"><a href="../">← 在线搜索与筛选</a><span>STATIC CATALOG · NO JAVASCRIPT REQUIRED</span></header>
<main><section class="wrap hero"><div><div class="eyebrow">AGENT SKILLS · 中文静态目录</div><h1>不用加载脚本，<br>直接按场景找。</h1><p class="lead">面向搜索引擎、阅读器和禁用 JavaScript 的访问者。全部条目从同一份 <code>skills.json</code> 自动生成，不手写数量，不按 Star 排名。</p></div><aside class="proof"><b>{len(skills)} 个条目</b><p>{ours} 个本站原创；最近来源复检：{esc(checked or '未记录')}。来源存在不等于功能、兼容或安全认证。</p></aside></section>
<section class="notice"><div class="wrap"><p><strong>怎么读：</strong>“本站原创”表示本仓库维护；“官方”表示上游来源身份；“第三方资料”只表示目录线索。安装前仍应检查 <code>SKILL.md</code>、脚本、联网与文件权限。想交互搜索请回到<a href="../">首页</a>。</p></div></section>
<nav class="wrap category-nav" aria-label="按场景跳转">{''.join(category_nav)}</nav>
<div class="wrap">{''.join(category_sections)}</div></main>
<footer class="wrap"><span><a href="../audit-skill/">安装前只读审计</a> · <a href="../compatibility/">兼容性证据</a> · <a href="../SKILLS.md">Markdown 完整清单</a></span><span>数据源：<a href="../data/skills.json">skills.json</a> · <a href="https://github.com/sanhuang520-ship-it/awesome-chinese-ai-tools">觉得有用再 Star</a></span></footer></body></html>
'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the committed page is stale")
    args = parser.parse_args()
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    rendered = render_catalog(data)
    current = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
    if args.check:
        if current != rendered:
            raise SystemExit("static catalog is stale; run python3 scripts/render_static_catalog.py")
        print(f"static catalog OK: {len(data['skills'])} skills")
        return
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    print(f"rendered {OUTPUT_PATH.relative_to(ROOT)}: {len(data['skills'])} skills")


if __name__ == "__main__":
    main()
