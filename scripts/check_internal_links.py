#!/usr/bin/env python3
"""Check explicit local links in published HTML pages."""

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK_ATTRIBUTES = {"href", "src"}
IGNORED_SCHEMES = {"data", "http", "https", "javascript", "mailto", "tel"}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in LINK_ATTRIBUTES and value:
                self.links.append(value.strip())


def published_pages(root: Path) -> list[Path]:
    ignored = {"node_modules", "work", ".git"}
    return sorted(
        page
        for page in root.rglob("*.html")
        if not any(part in ignored or part.startswith(".") for part in page.relative_to(root).parts)
    )


def missing_links(root: Path) -> list[str]:
    failures: list[str] = []
    root = root.resolve()

    for page in published_pages(root):
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for raw in parser.links:
            if not raw or raw.startswith("#") or "${" in raw:
                continue
            parsed = urlsplit(raw)
            if parsed.scheme.lower() in IGNORED_SCHEMES or parsed.netloc:
                continue
            local_path = unquote(parsed.path)
            if not local_path:
                continue
            target = (root / local_path.lstrip("/")) if local_path.startswith("/") else (page.parent / local_path)
            target = target.resolve()
            if target != root and root not in target.parents:
                failures.append(f"{page.relative_to(root)}: escapes site root: {raw}")
                continue
            exists = (target / "index.html").is_file() if target.is_dir() else target.is_file()
            if not exists:
                failures.append(f"{page.relative_to(root)}: missing {raw}")

    return failures


def main() -> None:
    failures = missing_links(ROOT)
    if failures:
        print("internal link check failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        raise SystemExit(1)
    print(f"internal links OK: {len(published_pages(ROOT))} HTML pages")


if __name__ == "__main__":
    main()
