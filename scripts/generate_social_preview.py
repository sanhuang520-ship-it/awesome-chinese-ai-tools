#!/usr/bin/env python3
"""Generate the repository social preview from committed evidence."""

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from sync_public_metadata import build_stats


ROOT = Path(__file__).resolve().parents[1]
SVG_PATH = ROOT / "og.svg"
PNG_PATH = ROOT / "og.png"
# 记录「og.png 是照哪一版 og.svg 渲染的」。
#
# 为什么不在 CI 里直接渲染 PNG：这张图的文案是中文，SVG 指定 Songti SC /
# Noto Serif CJK SC，而 GitHub runner 默认没有中文字体，在那边渲染会出豆腐块，
# 产出的图比现在更糟；而且不同机器的 rsvg/字体版本渲染出的字节本来就不同，
# 两边各渲染一次就会互相覆盖、无限 churn。
#
# 所以 PNG 保持本地生成，但把当时 og.svg 的哈希记下来，让 CI 只做「是否过期」
# 的判断——不需要字体、不需要渲染，也不会再悄悄过期。
PNG_STAMP_PATH = ROOT / "og.png.sha256"


def svg_digest(svg_text: str) -> str:
    return hashlib.sha256(svg_text.encode("utf-8")).hexdigest()


def png_is_stale(svg_text: str) -> bool:
    """og.png 是否落后于当前 og.svg。"""
    if not PNG_PATH.exists():
        return True
    if not PNG_STAMP_PATH.exists():
        return True
    return PNG_STAMP_PATH.read_text(encoding="utf-8").strip() != svg_digest(svg_text)


def build_preview_stats(catalog: dict, tools: dict, compatibility: dict) -> dict[str, int]:
    """
    从已解析的三份数据算出社交预览图要用的统计。

    单独抽出来是为了让 daily_check.py 能用 GitHub API 取到的数据直接调用——
    load_stats() 只能读本地文件，接不进那套「读 API → 比对 → 有变化才写」的流程。
    """
    public_stats = build_stats(catalog, tools)
    verified = compatibility["results"]["codexActivation"]["verifiedSkills"]
    stats = {
        "skills": public_stats["skills"],
        "chinese": public_stats["cn"],
        "ours": public_stats["ours"],
        "repos": public_stats["repos"],
        "codex": len(verified),
    }
    if stats["codex"] != stats["ours"]:
        raise ValueError("social preview requires Codex activation evidence for every first-party Skill")
    return stats


def load_stats(root: Path = ROOT) -> dict[str, int]:
    return build_preview_stats(
        json.loads((root / "data" / "skills.json").read_text(encoding="utf-8")),
        json.loads((root / "data" / "tools.json").read_text(encoding="utf-8")),
        json.loads((root / "data" / "compatibility.json").read_text(encoding="utf-8")),
    )


def render_svg(stats: dict[str, int]) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
<title id="title">中文 AI Skills 库</title>
<desc id="desc">{stats['skills']} 个 Agent Skill 条目，{stats['ours']} 个本站原创；Codex {stats['codex']}/{stats['ours']} 有自动触发记录，Claude Code 和 Cursor 待测。</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#111719"/><stop offset=".62" stop-color="#17181b"/><stop offset="1" stop-color="#30201e"/></linearGradient>
  <radialGradient id="glow"><stop stop-color="#e0795a" stop-opacity=".24"/><stop offset="1" stop-color="#e0795a" stop-opacity="0"/></radialGradient>
  <filter id="shadow"><feDropShadow dx="0" dy="8" stdDeviation="14" flood-color="#000" flood-opacity=".45"/></filter>
</defs>
<rect width="1200" height="630" fill="url(#bg)"/>
<circle cx="103" cy="93" r="92" fill="url(#glow)"/>
<rect x="70" y="64" width="64" height="64" rx="18" fill="#e58a4f" filter="url(#shadow)"/>
<text x="102" y="108" text-anchor="middle" fill="#fff8eb" font-size="35" font-family="Songti SC,Noto Serif CJK SC,serif">技</text>
<text x="154" y="107" fill="#f4f0e8" font-size="30" font-weight="650" font-family="Songti SC,Noto Serif CJK SC,serif">中文 AI Skills 库</text>
<text x="70" y="229" fill="#f5f1e9" font-size="64" font-weight="650" font-family="Songti SC,Noto Serif CJK SC,serif">{stats['skills']} 个 Agent Skill 条目</text>
<text x="70" y="322" fill="#f5f1e9" font-size="55" font-weight="650" font-family="Songti SC,Noto Serif CJK SC,serif">其中 <tspan fill="#f07858">{stats['ours']} 个本站原创</tspan></text>
<text x="70" y="383" fill="#bfc1c6" font-size="25" font-weight="550" font-family="Avenir Next,PingFang SC,Noto Sans CJK SC,sans-serif">{stats['chinese']} 个中文 Skill 条目 · 来自 {stats['repos']} 个来源仓库 · 每日来源复检</text>
<g transform="translate(70 428)" font-family="Avenir Next,PingFang SC,Noto Sans CJK SC,sans-serif" font-size="19" font-weight="700">
  <rect width="304" height="54" rx="27" fill="#193b31" stroke="#70b59a"/><text x="152" y="34" text-anchor="middle" fill="#9ed8c0">Codex {stats['codex']}/{stats['ours']} 自动触发记录</text>
  <rect x="322" width="278" height="54" rx="27" fill="#352a1e" stroke="#d7a44d"/><text x="461" y="34" text-anchor="middle" fill="#efc470">Claude Code / Cursor 待测</text>
  <rect x="618" width="210" height="54" rx="27" fill="#202f39" stroke="#7397aa"/><text x="723" y="34" text-anchor="middle" fill="#9fc2d3">运行边界公开</text>
</g>
<line x1="70" y1="520" x2="1130" y2="520" stroke="#f4f0e8" stroke-opacity=".14"/>
<text x="70" y="571" fill="#a3a4aa" font-size="21" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">sanhuang520-ship-it.github.io/awesome-chinese-ai-tools</text>
<rect x="927" y="541" width="203" height="48" rx="11" fill="#17352d" stroke="#4c806d"/>
<text x="1028" y="571" text-anchor="middle" fill="#9ed8c0" font-size="18" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">npx skills add …</text>
</svg>
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write og.svg")
    parser.add_argument("--png", action="store_true", help="also render og.png with rsvg-convert")
    parser.add_argument("--check", action="store_true", help="fail if committed og.svg is stale")
    args = parser.parse_args()
    expected = render_svg(load_stats())

    if args.check:
        current = SVG_PATH.read_text(encoding="utf-8") if SVG_PATH.exists() else ""
        if current != expected:
            raise SystemExit("og.svg is stale; run python3 scripts/generate_social_preview.py --write --png")
        if png_is_stale(current):
            raise SystemExit(
                "og.png is stale relative to og.svg; run "
                "python3 scripts/generate_social_preview.py --write --png "
                "(needs rsvg-convert and CJK fonts, so it must be done locally, not in CI)"
            )
        print("social preview SVG and PNG are in sync")

    if args.write:
        SVG_PATH.write_text(expected, encoding="utf-8")
        print(f"wrote {SVG_PATH.relative_to(ROOT)}")

    if args.png:
        renderer = shutil.which("rsvg-convert")
        if not renderer:
            raise SystemExit("rsvg-convert is required for --png")
        if not args.write and not SVG_PATH.exists():
            raise SystemExit("og.svg is missing; add --write")
        subprocess.run([renderer, "-w", "1200", "-h", "630", "-o", str(PNG_PATH), str(SVG_PATH)], check=True)
        PNG_STAMP_PATH.write_text(
            svg_digest(SVG_PATH.read_text(encoding="utf-8")) + "\n", encoding="utf-8"
        )
        print(f"wrote {PNG_PATH.relative_to(ROOT)} + {PNG_STAMP_PATH.relative_to(ROOT)}")

    if not (args.check or args.write or args.png):
        parser.error("choose --check or --write [--png]")


if __name__ == "__main__":
    main()
