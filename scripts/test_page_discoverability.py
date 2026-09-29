#!/usr/bin/env python3
"""每个正式页面都必须可被发现：有站内入口、在 sitemap 里、分享出去有卡片。

写这个测试的原因（2026-08-21 实测）：
`alternatives/` 子树 7 个页面 2026-08-12 上线，但站内 0 条 <a> 入口、
sitemap 0 条登记、og 卡片全缺。没有任何守卫会发现——
sync_social_cards.py 只管 data/skills.json 里的 13 个 explainer 页，
sync_public_metadata.py 的 sync_sitemap_text 只更新 4 个核心条目的 lastmod、从不新增。
手写页因此完全没有守卫。
"""

import re
import unittest
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from check_internal_links import published_pages

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/"

# 内嵌 demo：由讲解页 iframe 或链接引用，本身不作为独立入口收录。
# 新增 demo 必须显式加进来，避免"忘了登记"和"故意不登记"混为一谈。
DEMO_PAGES = {
    "skills/chinese-web-themes/demo.html",
    "skills/guofeng-threejs/demo.html",
    "skills/guofeng-threejs/gongbi-demo.html",
    "skills/guofeng-threejs/intro-demo.html",
    "skills/guofeng-threejs/papercut-demo.html",
    "themes/ink3d.html",
    "themes/intro.html",
}


# 不从站内首页链接、但确实有入口的页面。故意写成显式白名单：
# 新增条目必须是有意识的决定，而不是"忘了加链接"。
# 它在 README.md / README.en.md / llms.txt 里有入口，也在 sitemap 里。
# （chinese-agent-skills/ 已于 2026-08-21 在首页导航栏加了 EN 入口，故移出白名单。）
LINKED_ONLY_FROM_README = {
    # 无 JavaScript 的可爬目录，是首页列表的镜像；不从首页链接以免自我竞争。
    "catalog/index.html",
}


def rel(page: Path) -> str:
    return page.relative_to(ROOT).as_posix()


def is_noindex(body: str) -> bool:
    return bool(re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex', body, re.I))


def indexable_pages():
    for page in published_pages(ROOT):
        path = rel(page)
        if path in DEMO_PAGES:
            continue
        body = page.read_text(encoding="utf-8")
        if is_noindex(body):
            continue
        yield path, body


def canonical_of(body: str) -> str | None:
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', body, re.I)
    return m.group(1) if m else None


def outgoing_links(path: str, body: str) -> set[str]:
    """一个页面指向的本地页面，归一化成仓库相对路径。"""
    out: set[str] = set()
    src_dir = path.rsplit("/", 1)[0] + "/" if "/" in path else ""
    for raw in re.findall(r'<a\b[^>]*\bhref="([^"]+)"', body, re.I):
        raw = raw.strip()
        if not raw or raw.startswith("#") or "${" in raw or "'" in raw or "+" in raw:
            continue
        if raw.startswith(BASE):
            dest = raw[len(BASE):]
        elif urlsplit(raw).scheme or raw.startswith("//"):
            continue  # 站外
        else:
            dest = urljoin(src_dir, raw)
        dest = urlsplit(dest).path.lstrip("/")
        if dest.endswith("/") or dest == "":
            dest += "index.html"
        if dest != path:
            out.add(dest)
    return out


def reachable_from_home() -> set[str]:
    """从首页出发做广度优先遍历。

    ⚠️ 不能只检查"有没有入链"：alternatives/ 那 7 个页面互相链接成闭环，
    每一页都有入链，但整个簇从首页点不进去。必须从首页真正走一遍。
    """
    bodies = {rel(p): p.read_text(encoding="utf-8") for p in published_pages(ROOT)}
    seen = {"index.html"}
    queue = ["index.html"]
    while queue:
        current = queue.pop()
        for dest in outgoing_links(current, bodies.get(current, "")):
            if dest in bodies and dest not in seen:
                seen.add(dest)
                queue.append(dest)
    return seen


class PageDiscoverabilityTest(unittest.TestCase):
    def test_every_indexable_page_is_registered_in_sitemap(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        listed = set(re.findall(r"<loc>(.*?)</loc>", sitemap))
        for path, body in indexable_pages():
            with self.subTest(page=path):
                canonical = canonical_of(body)
                self.assertIsNotNone(canonical, f"{path} 缺 canonical")
                self.assertIn(
                    canonical, listed,
                    f"{path} 的 canonical 不在 sitemap.xml 里——页面上线了但搜索引擎不会知道",
                )

    def test_every_indexable_page_is_reachable_from_home(self):
        reachable = reachable_from_home() | LINKED_ONLY_FROM_README | {"index.html"}
        for path, _ in indexable_pages():
            with self.subTest(page=path):
                self.assertIn(
                    path, reachable,
                    f"{path} 从首页点不到，也不在 LINKED_ONLY_FROM_README 白名单里"
                    f"——要么补一条站内链接，要么把它加进白名单并写明理由",
                )

    def test_retired_pages_stay_out_of_sitemap(self):
        """带 noindex 的页面是被主动撤下搜索的，不能再被加回 sitemap。

        alternatives/ 那 7 页 2026-08-12 由提交 "retire stale alternative advice
        from search" 主动加上 noindex，因为推荐建议已过期。把它们加回 sitemap
        等于悄悄撤销那个决定——本测试就是防这个。
        """
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        listed = set(re.findall(r"<loc>(.*?)</loc>", sitemap))
        for page in published_pages(ROOT):
            body = page.read_text(encoding="utf-8")
            if not is_noindex(body):
                continue
            canonical = canonical_of(body)
            if canonical is None:
                continue
            with self.subTest(page=rel(page)):
                self.assertNotIn(
                    canonical, listed,
                    f"{rel(page)} 标了 noindex 却出现在 sitemap 里——自相矛盾",
                )

    def test_every_indexable_page_has_share_card(self):
        required_props = ("og:title", "og:description", "og:url", "og:image")
        for path, body in indexable_pages():
            with self.subTest(page=path):
                for prop in required_props:
                    self.assertIn(
                        f'property="{prop}"', body,
                        f"{path} 缺 {prop}——分享到微信/X 时没有预览卡片",
                    )
                self.assertIn(
                    '<meta name="twitter:card" content="summary_large_image">', body,
                    f"{path} 的 twitter:card 不是 summary_large_image",
                )

    def test_every_page_declares_doctype_and_language(self):
        """怪异模式与缺 lang 都是静默故障：页面照常显示，只是渲染模式和读屏语言是错的。"""
        for page in published_pages(ROOT):
            path = rel(page)
            body = page.read_text(encoding="utf-8")
            with self.subTest(page=path):
                self.assertTrue(
                    body.lstrip()[:15].lower().startswith("<!doctype"),
                    f"{path} 缺 <!DOCTYPE html>，浏览器会用怪异模式渲染",
                )
                self.assertRegex(
                    body[:400], r"<html[^>]*\slang=",
                    f"{path} 的 <html> 缺 lang 属性，屏幕阅读器只能猜语言",
                )


if __name__ == "__main__":
    unittest.main()
