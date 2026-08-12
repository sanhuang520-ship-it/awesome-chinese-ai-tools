#!/usr/bin/env python3
"""Keep first-party explainer social-card metadata complete and consistent."""

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/"
DEFAULT_IMAGE = BASE + "og.png"
CUSTOM_IMAGES = {
    "guofeng-threejs": (BASE + "assets/shots/threejs-ink.webp", 1400, 933),
    "chinese-web-themes": (BASE + "assets/shots/theme-ink.webp", 1400, 1272),
}


def meta_value(body: str, attribute: str, name: str) -> str:
    match = re.search(
        rf'<meta\s+{attribute}="{re.escape(name)}"\s+content="([^"]*)"\s*/?>',
        body,
        re.I,
    )
    if not match:
        raise ValueError(f"missing {attribute}={name}")
    return match.group(1)


def strip_managed(body: str) -> str:
    names = (
        "og:image",
        "og:image:width",
        "og:image:height",
        "og:image:alt",
        "twitter:card",
        "twitter:title",
        "twitter:description",
        "twitter:image",
        "twitter:image:alt",
    )
    for name in names:
        body = re.sub(
            rf'<meta\s+(?:property|name)="{re.escape(name)}"\s+content="[^"]*"\s*/?>',
            "",
            body,
            flags=re.I,
        )
    return body


def sync_structured_image(body: str, image: str) -> str:
    match = re.search(r'(<script\s+type="application/ld\+json">)(.*?)(</script>)', body, re.I | re.S)
    if not match:
        raise ValueError("missing JSON-LD")
    data = json.loads(match.group(2))
    graph = data.get("@graph") if isinstance(data, dict) else None
    candidates = graph if isinstance(graph, list) else [data]
    target = next(
        (
            item
            for item in candidates
            if isinstance(item, dict) and item.get("@type") not in {"FAQPage", "BreadcrumbList"}
        ),
        None,
    )
    if target is None:
        raise ValueError("JSON-LD has no primary entity for image")
    target["image"] = image
    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return body[: match.start()] + match.group(1) + encoded + match.group(3) + body[match.end() :]


def sync_page(body: str, skill_name: str) -> str:
    title = meta_value(body, "property", "og:title")
    description = meta_value(body, "property", "og:description")
    image, width, height = CUSTOM_IMAGES.get(skill_name, (DEFAULT_IMAGE, 1200, 630))
    block = "\n".join(
        (
            f'<meta property="og:image" content="{image}">',
            f'<meta property="og:image:width" content="{width}">',
            f'<meta property="og:image:height" content="{height}">',
            f'<meta property="og:image:alt" content="{title}">',
            '<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:title" content="{title}">',
            f'<meta name="twitter:description" content="{description}">',
            f'<meta name="twitter:image" content="{image}">',
            f'<meta name="twitter:image:alt" content="{title}">',
        )
    )
    body = strip_managed(body)
    marker = re.search(r'^<meta\s+property="og:type"\s+content="[^"]*"\s*/?>', body, re.I | re.M)
    if not marker:
        raise ValueError("missing og:type")
    suffix = re.sub(r'^[ \t]*\n(?:[ \t]*\n)*', "\n", body[marker.end() :])
    body = body[: marker.end()] + "\n" + block + suffix
    return sync_structured_image(body, image)


def explainer_pages(root: Path = ROOT):
    catalog = json.loads((root / "data" / "skills.json").read_text(encoding="utf-8"))
    for skill in catalog["skills"]:
        if skill.get("ours") and skill.get("explainer"):
            yield skill["name"], root / skill["explainer"] / "index.html"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write synchronized metadata")
    args = parser.parse_args()
    changed = []
    for name, path in explainer_pages():
        current = path.read_text(encoding="utf-8")
        expected = sync_page(current, name)
        if current != expected:
            changed.append(path.relative_to(ROOT).as_posix())
            if args.write:
                path.write_text(expected, encoding="utf-8")
    if changed and not args.write:
        raise SystemExit("stale social metadata: " + ", ".join(changed))
    print(f"social metadata {'updated' if args.write else 'in sync'}: {len(list(explainer_pages()))} explainers")


if __name__ == "__main__":
    main()
