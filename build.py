#!/usr/bin/env python3
"""Build the Quijote website.

Reads content/*.json and templates/*.html and writes a finished static site to
_site/ (or the folder given as the first argument). Run:  python3 build.py
"""
import json
import shutil
import sys
from pathlib import Path

import re

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup, escape

ROOT = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "_site"

site = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))
LANGS = list(site["languages"])
texts = {l: json.loads((ROOT / "content" / f"{l}.json").read_text(encoding="utf-8")) for l in LANGS}

# Which template renders each page, and whether it shows the "get to know us" band.
PAGES = {
    "home": ("home.html", True),
    "concept": ("concept.html", True),
    "team": ("team.html", True),
    "reviews": ("reviews.html", True),
    "admission": ("admission.html", True),
    "faq": ("faq.html", True),
    "contact": ("contact.html", False),
    "legal": ("legal.html", False),
    "thanks": ("thanks.html", False),
}


def page_path(page, lang):
    """Site-relative folder of a page, e.g. 'de/konzept/' or 'en/'."""
    slug = site["pages"][page][lang]
    return f"{lang}/{slug}/" if slug else f"{lang}/"


def make_env():
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=True,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["rich"] = rich_text
    return env


def rich_text(text):
    """Escape text, then turn [label](https://…) into links and line breaks into <br>."""
    html = str(escape(text))
    html = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        lambda m: f'<a href="{m.group(2)}" target="_blank" rel="noopener">{m.group(1)}</a>',
        html,
    )
    return Markup(html.replace("\n", "<br>\n"))


def render_all():
    env = make_env()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT / "assets", OUT / "assets")

    for lang in LANGS:
        t = texts[lang]
        for page, (tpl, show_cta) in PAGES.items():
            rel = page_path(page, lang)
            depth = rel.count("/")
            root = "../" * depth

            def url(target, target_lang=lang, _root=root):
                return _root + page_path(target, target_lang)

            def img(name, _root=root):
                return {
                    "src": f"{_root}assets/img/{name}-800.jpg",
                    "srcset": f"{_root}assets/img/{name}-800.jpg 800w, {_root}assets/img/{name}-1600.jpg 1600w",
                    "w": site["image_sizes"][name][0],
                    "h": site["image_sizes"][name][1],
                }

            title = t["meta"]["homeTitle"] if page == "home" else (
                f'{page_title(page, t)} – {t["meta"]["siteName"]}')
            ctx = {
                "site": site,
                "t": t,
                "lang": lang,
                "page": page,
                "root": root,
                "url": url,
                "img": img,
                "title": title,
                "show_cta": show_cta,
                "canonical": site["site_url"].rstrip("/") + "/" + rel,
                "alternates": [
                    {"lang": l, "href": site["site_url"].rstrip("/") + "/" + page_path(page, l)} for l in LANGS
                ],
                "lang_links": [
                    {"code": l, **site["languages"][l], "href": url(page, l), "current": l == lang} for l in LANGS
                ],
                "nav_items": [
                    {"key": p, "label": t["nav"][p], "href": url(p), "current": p == page} for p in site["nav"]
                ],
                "noindex": page == "thanks",
            }
            html = env.get_template(tpl).render(**ctx)
            dest = OUT / rel / "index.html"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(html, encoding="utf-8")

    # Root: send visitors to their browser language, German by default.
    (OUT / "index.html").write_text(env.get_template("root.html").render(site=site, texts=texts, page_path=page_path), encoding="utf-8")

    # 404 page (GitHub Pages serves /404.html for unknown addresses). Uses absolute
    # links because it can be shown at any depth.
    t = texts[site["default_lang"]]
    (OUT / "404.html").write_text(env.get_template("404.html").render(site=site, texts=texts, page_path=page_path), encoding="utf-8")

    # robots.txt + sitemap.xml
    base = site["site_url"].rstrip("/")
    urls = [f"{base}/{page_path(p, l)}" for l in LANGS for p in PAGES if p != "thanks"]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    cname = ROOT / "CNAME"
    if cname.exists():
        shutil.copy(cname, OUT / "CNAME")

    count = len(LANGS) * len(PAGES)
    print(f"Built {count} pages in {len(LANGS)} languages -> {OUT}")


def page_title(page, t):
    special = {"legal": t["legal"]["h1"], "thanks": t["thanks"]["title"]}
    return special.get(page) or t["nav"][page]


if __name__ == "__main__":
    render_all()
