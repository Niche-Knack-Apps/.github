#!/usr/bin/env python3
"""Render the GitHub organization profile artwork in the nk.tools style.

GitHub profile READMEs accept no CSS, so the design ships as images: section
bands in the social-banner style, app cards in the nk.tools card style, and link
pills. Every image carries its own parchment background, so it reads the same in
GitHub's light and dark themes.

    python3 design/render.py        # writes profile/assets/*.png

Edit APPS / OPEN_SOURCE / LINKS below when nk.tools changes, then re-render.
Needs Python Playwright with its Chromium (`pip install playwright && playwright install chromium`).
"""
from __future__ import annotations

import html
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "profile" / "assets"

APPS = [
    # slug, name, tagline, description, platforms, group
    ("pocket-nerd", "Pocket Nerd", "Open. Enter. Done.",
     "A scratchpad for money, in your pocket. Write down what you spent in seconds and see what it does to tomorrow.",
     "Android", "Money"),
    ("ledgerkeep", "LedgerKeep", "Your books. Your files. Your call.",
     "Double-entry books in plain-text Ledger files, with Git history, bill reminders and debts you can fight as bosses.",
     "Android, Linux, Windows, macOS", "Money"),
    ("clip-dr", "Clip Dr.", "Find the moment. Fix the sound.",
     "Turn a long recording into useful clips. Find the passage, make the edit, and keep every version.",
     "Linux, Windows, Android recorder", "Sound and research"),
    ("rabbit-trail", "Rabbit Trail", "Follow the clues. Keep the source.",
     "An evidence board and research archive. Follow names, dates and relationships back to the passages they came from.",
     "Android, Linux, Windows", "Sound and research"),
    ("choirboy", "Choirboy", "It’s your media. Enjoy it your way.",
     "Choose what gets filtered in media you own or legitimately access, from Plex, Emby, Jellyfin and more.",
     "Android, Linux, Roku", "Media and writing"),
    ("euphonics", "Euphonics", "Find your rhyme. Keep your voice.",
     "Find the right rhyme, try a near rhyme, and give a few words room to grow.",
     "Android", "Media and writing"),
]

OPEN_SOURCE = [
    # slug, name, tile, tagline, description, platforms
    ("z9s", "z9s", "z9s", "A k9s-style terminal UI for Zarf.",
     "Browse, inspect, build, deploy and remove Zarf packages for air-gapped Kubernetes, from one static binary.",
     "Go · Linux, macOS, Windows"),
    ("nines", "nines", "9s", "One terminal shell, two languages.",
     "The k9s-shaped shell behind z9s, specified once in a contract and implemented in Go and Rust.",
     "Go · Rust"),
]

SECTIONS = [
    # file, eyebrow, title
    ("section-apps", "nk.tools", "The apps"),
    ("section-open-source", "Free and open", "Open source"),
    ("section-find-us", "Elsewhere", "Find us"),
]

LINKS = [
    # file, label
    ("link-nk-tools", "nk.tools"),
    ("link-journal", "Dev Journal"),
    ("link-x", "X"),
    ("link-facebook", "Facebook"),
    ("link-instagram", "Instagram"),
    ("link-pinterest", "Pinterest"),
    ("link-coffee", "Buy Me a Coffee"),
]

FONTS = """
@font-face { font-family: 'Libre Baskerville'; font-weight: 400; font-style: normal; src: url(fonts/libre-baskerville-latin-400-normal.woff2); }
@font-face { font-family: 'Libre Baskerville'; font-weight: 400; font-style: italic; src: url(fonts/libre-baskerville-latin-400-italic.woff2); }
@font-face { font-family: 'Libre Baskerville'; font-weight: 700; font-style: normal; src: url(fonts/libre-baskerville-latin-700-normal.woff2); }
@font-face { font-family: 'IBM Plex Sans'; font-weight: 400; src: url(fonts/ibm-plex-sans-latin-400-normal.woff2); }
@font-face { font-family: 'IBM Plex Sans'; font-weight: 500; src: url(fonts/ibm-plex-sans-latin-500-normal.woff2); }
@font-face { font-family: 'IBM Plex Sans'; font-weight: 600; src: url(fonts/ibm-plex-sans-latin-600-normal.woff2); }
@font-face { font-family: 'IBM Plex Mono'; font-weight: 400; src: url(fonts/ibm-plex-mono-latin-400-normal.woff2); }
@font-face { font-family: 'IBM Plex Mono'; font-weight: 500; src: url(fonts/ibm-plex-mono-latin-500-normal.woff2); }
"""

# nk.tools design tokens (site/src/styles/global.css) plus the social-banner art.
CSS = FONTS + """
:root {
  --paper: #efe7d6; --paper-2: #e4d9c0; --paper-3: #fbf7ee;
  --ink: #181510; --ink-2: #4b443a; --ink-3: #62594b;
  --rule: #cdbfa2; --brass: #755a1d; --brass-2: #b8912f; --slate: #222620;
  --serif: 'Libre Baskerville', Georgia, serif;
  --sans: 'IBM Plex Sans', sans-serif;
  --mono: 'IBM Plex Mono', monospace;
}
* { box-sizing: border-box; }
html, body { margin: 0; background: transparent; }
body { font-family: var(--sans); color: var(--ink); -webkit-font-smoothing: antialiased; }

/* Section band: the social banners in miniature. */
.band { position: relative; width: 1000px; height: 150px; overflow: hidden;
  background: var(--paper); border-radius: 6px; }
.band .stripe { position: absolute; left: -10px; top: -40px; width: 200px; height: 260px;
  background: var(--paper-2); transform: skewX(38deg); }
.band .stripe-line { position: absolute; left: -40px; top: -40px; width: 1px; height: 260px;
  background: var(--brass-2); opacity: .45; transform: skewX(38deg); }
.band .stripe-line.b { left: -70px; opacity: .3; }
.band svg.corner { position: absolute; right: 0; top: 0; width: 120px; height: 150px; }
.band .rule-top, .band .rule-bottom { position: absolute; left: 28px; right: 92px; height: 1px; background: var(--rule); }
.band .rule-top { top: 22px; } .band .rule-bottom { bottom: 22px; }
.band .ticks { position: absolute; left: 52px; top: 22px; display: flex; gap: 11px; }
.band .ticks i { display: block; width: 1px; height: 6px; background: var(--brass-2); opacity: .7; }
.band .ticks i:nth-child(4n+1) { height: 10px; }
.band .cross { position: absolute; color: var(--brass-2); font: 400 16px/1 var(--mono); }
.band .text { position: absolute; left: 230px; top: 36px; }
.band .bar { width: 48px; height: 3px; background: var(--brass-2); margin-bottom: 12px; }
.band .eyebrow { font: 500 14px/1 var(--mono); letter-spacing: .22em; text-transform: uppercase; color: var(--brass); }
.band h2 { font: 400 40px/1.1 var(--serif); margin: 10px 0 0; letter-spacing: -.01em; }

/* App card: the nk.tools card. */
.pad { padding: 18px; display: inline-block; }
.card { width: 560px; height: 330px; display: flex; flex-direction: column; padding: 28px 30px;
  background: var(--paper-3); border: 1px solid var(--rule); border-radius: 6px;
  box-shadow: 0 1px 0 rgba(24,21,16,.06), 0 12px 30px -18px rgba(24,21,16,.35); }
.card .group { font: 500 13px/1 var(--mono); letter-spacing: .22em; text-transform: uppercase; color: var(--brass); margin-bottom: 18px; }
.card .head { display: flex; gap: 18px; align-items: center; }
.card .icon { width: 68px; height: 68px; border-radius: 14px; flex: none; }
.card .tile { width: 68px; height: 68px; border-radius: 14px; flex: none; display: grid; place-items: center;
  background: var(--slate); color: var(--paper); font: 500 22px/1 var(--mono); border: 2px solid var(--brass-2); }
.card h3 { font: 400 34px/1.1 var(--serif); margin: 0; }
.card .tag { font: italic 400 19px/1.3 var(--serif); color: var(--ink-2); margin: 6px 0 0; }
.card .desc { font: 400 19px/1.5 var(--sans); margin: 18px 0 0; color: var(--ink); }
.card .foot { margin-top: auto; display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.card .plat { font: 400 15px/1.3 var(--mono); color: var(--ink-3); }
.card .btn { font: 600 16px/1 var(--sans); padding: 12px 16px; border: 1.5px solid var(--ink); border-radius: 6px; white-space: nowrap; background: var(--paper-3); }

/* Link pill. */
.pill { display: inline-flex; align-items: center; gap: 10px; padding: 12px 18px; background: var(--paper-3);
  border: 1px solid var(--rule); border-radius: 999px; font: 500 15px/1 var(--mono); letter-spacing: .12em;
  text-transform: uppercase; color: var(--ink); }
.pill b { width: 8px; height: 8px; border-radius: 50%; background: var(--brass-2); display: block; }
"""


def page(body: str) -> str:
    return f"<!doctype html><meta charset=utf-8><style>{CSS}</style>{body}"


def band(eyebrow: str, title: str) -> str:
    ticks = "".join("<i></i>" for _ in range(14))
    return f"""<div class="band" id="shot">
  <div class="stripe"></div><div class="stripe-line"></div><div class="stripe-line b"></div>
  <div class="rule-top"></div><div class="rule-bottom"></div><div class="ticks">{ticks}</div>
  <span class="cross" style="left:22px;top:15px">+</span><span class="cross" style="left:22px;bottom:15px">+</span>
  <svg class="corner" viewBox="0 0 120 150"><path d="M30 0H120V62Z M30 150H120V88Z" fill="#222620"/>
    <path d="M12 0L120 72 M12 150L120 78" stroke="#b8912f" stroke-width="1" fill="none" opacity=".7"/></svg>
  <span class="cross" style="right:96px;top:15px">+</span><span class="cross" style="right:96px;bottom:15px">+</span>
  <div class="text"><div class="bar"></div><div class="eyebrow">{html.escape(eyebrow)}</div><h2>{html.escape(title)}</h2></div>
</div>"""


def card(group: str, icon: str, name: str, tagline: str, desc: str, plat: str, button: str) -> str:
    return f"""<div class="pad" id="shot"><div class="card">
  <div class="group">{html.escape(group)}</div>
  <div class="head">{icon}<div><h3>{html.escape(name)}</h3><p class="tag">{html.escape(tagline)}</p></div></div>
  <p class="desc">{html.escape(desc)}</p>
  <div class="foot"><span class="plat">{html.escape(plat)}</span><span class="btn">{html.escape(button)}</span></div>
</div></div>"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs: list[tuple[str, str]] = []
    for name, eyebrow, title in SECTIONS:
        jobs.append((name, band(eyebrow, title)))
    for slug, name, tagline, desc, plat, group in APPS:
        icon = f'<img class="icon" src="icons/{slug}.png" alt="">'
        jobs.append((f"app-{slug}", card(group, icon, name, tagline, desc, plat, f"Explore {name}")))
    for slug, name, tile, tagline, desc, plat in OPEN_SOURCE:
        icon = f'<div class="tile">{html.escape(tile)}</div>'
        jobs.append((f"oss-{slug}", card("Open source", icon, name, tagline, desc, plat, "View on GitHub")))
    for name, label in LINKS:
        jobs.append((name, f'<div class="pad" id="shot" style="padding:4px"><span class="pill"><b></b>{html.escape(label)}</span></div>'))

    with sync_playwright() as p:
        # The full Chromium build; the headless shell intermittently hangs on screenshots.
        browser = p.chromium.launch(channel="chromium")
        ctx = browser.new_context(device_scale_factor=2, viewport={"width": 1200, "height": 800})
        pg = ctx.new_page()
        for name, body in jobs:
            src = HERE / "_render.html"
            src.write_text(page(body))
            pg.goto(src.as_uri())
            pg.evaluate("document.fonts.ready")
            box = pg.locator("#shot").bounding_box()
            pg.screenshot(path=str(OUT / f"{name}.png"), clip=box, omit_background=True)
            print(f"{name}.png {int(box['width'])}x{int(box['height'])} css px")
        (HERE / "_render.html").unlink(missing_ok=True)
        browser.close()


if __name__ == "__main__":
    main()
