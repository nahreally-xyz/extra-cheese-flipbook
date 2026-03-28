#!/usr/bin/env python3
"""
build_flipbook.py
Assembles all page images into a self-contained HTML flipbook.

Usage:
    python scripts/build_flipbook.py

Reads from pages/, writes to output/extra_cheese_flipbook.html
"""

import base64
import json
import os
from pathlib import Path


def encode(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def build_pages(pages_dir: Path) -> list:
    """Build ordered PAGES array: front cover + 38 interior + back cover."""
    pages = []

    # Front cover (right half of original landscape cover PDF)
    pages.append({
        "src":   encode(pages_dir / "front_cover.jpg"),
        "label": "Front Cover",
        "role":  "front",
    })

    # Interior pages in order
    interior_files = sorted(pages_dir.glob("interior_*.jpg"))
    assert len(interior_files) == 38, f"Expected 38 interior pages, found {len(interior_files)}"

    labels = [
        "Title Page", "Credits", "Table of Contents", "About the Authors",
        "Moving at the Speed of Life (1)", "Moving at the Speed of Life (2)",
        "Moving at the Speed of Life (3)",
        "How to Listen to NAHreally (1)", "How to Listen to NAHreally (2)",
        "How to Listen to NAHreally (3)", "How to Listen to NAHreally (4)",
        "How to Listen to NAHreally (5)", "How to Listen to NAHreally (6)",
        "The Lyrics",
        "1010 WINS", "1010 WINS — notes",
        "Moderately Well", "Moderately Well — notes",
        "Umpteen", "Umpteen — notes",
        "Kick in the Pants", "Kick in the Pants — notes",
        "FUKWITME 2", "FUKWITME 2 — notes",
        "I Need a Hobby", "I Need a Hobby — notes",
        "You've Got a Friend Type Beat", "You've Got a Friend — notes",
        "Too Many Cooks", "Too Many Cooks — notes",
        "How We Always Gotta Be", "How We Always Gotta Be — notes",
        "Find Our Way", "Find Our Way — notes",
        "Human Error", "Human Error — notes",
        "On Cheesiness (1)", "On Cheesiness (2) + Other Works",
    ]

    for i, path in enumerate(interior_files):
        pages.append({
            "src":   encode(path),
            "label": labels[i] if i < len(labels) else f"Page {i + 1}",
            "role":  "interior",
        })

    # Back cover (left half of original landscape cover PDF — the GREEN side)
    pages.append({
        "src":   encode(pages_dir / "back_cover.jpg"),
        "label": "Back Cover",
        "role":  "back",
    })

    assert len(pages) == 40, f"Expected 40 pages total, got {len(pages)}"
    return pages


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Extra Cheese — NAHreally</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; touch-action: manipulation; }
  body {
    background: #242424;
    font-family: 'Georgia', serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    color: #eee;
    user-select: none;
  }
  #header { padding: 48px 24px 8px; text-align: center; }
  #header h1 {
    font-family: 'Bookman Old Style', 'Bookman', Georgia, serif;
    font-style: italic; font-weight: 525;
    font-size: 2.2rem; letter-spacing: 3px;
    color: #ffe033;
  }
  #header .byline {
    font-family: 'Bookman Old Style', 'Bookman', Georgia, serif;
    font-style: italic; font-size: 1rem; color: #ccc;
    margin-top: 4px; letter-spacing: 1px;
  }
  #header .contributors {
    font-family: 'Bookman Old Style', 'Bookman', Georgia, serif;
    font-style: italic; font-size: 0.72rem; color: #888;
    margin-top: 3px; letter-spacing: 1px;
  }
  #viewer {
    width: 100%; max-width: 1040px;
    display: flex; align-items: center; justify-content: center;
    padding: 16px 10px 10px;
    gap: 12px;
  }
  #book { display: flex; justify-content: center; align-items: stretch; flex: 1; max-width: 920px; gap: 0; }
  .page-frame {
    position: relative; overflow: hidden; border-radius: 2px;
    background: #f5f0e8; flex: 1; max-width: 460px;
  }
  .page-frame:first-child {
    box-shadow: -4px 4px 20px rgba(0,0,0,0.4), 2px 0 4px rgba(0,0,0,0.2);
    border-radius: 2px 0 0 2px;
  }
  .page-frame:last-child {
    box-shadow: 4px 4px 20px rgba(0,0,0,0.4), -2px 0 4px rgba(0,0,0,0.2);
    border-radius: 0 2px 2px 0;
  }
  .page-frame img { display: block; width: 100%; height: auto; }
  #spine {
    width: 8px; flex-shrink: 0; align-self: stretch;
    background: linear-gradient(to right, #3a3a3a 0%, #888 40%, #ccc 50%, #888 60%, #3a3a3a 100%);
  }
  .nav-btn {
    flex-shrink: 0;
    background: rgba(255,255,255,0.12); border: none; color: #ccc;
    width: 42px; height: 64px; border-radius: 4px; cursor: pointer;
    font-size: 1.1rem; display: flex; align-items: center; justify-content: center;
    transition: background 0.15s, color 0.15s; backdrop-filter: blur(2px);
  }
  .nav-btn:hover:not(:disabled) { background: rgba(255,255,255,0.28); color: #fff; }
  .nav-btn:disabled { opacity: 0.15; cursor: default; }
  #thumb-strip {
    display: flex; gap: 5px; overflow-x: auto;
    padding: 8px 12px 12px; max-width: 960px; width: 100%;
    scrollbar-width: thin; scrollbar-color: #444 #222;
  }
  #thumb-strip::-webkit-scrollbar { height: 4px; }
  #thumb-strip::-webkit-scrollbar-track { background: #222; }
  #thumb-strip::-webkit-scrollbar-thumb { background: #555; border-radius: 2px; }
  .thumb {
    flex-shrink: 0; cursor: pointer; border: 2px solid transparent;
    border-radius: 2px; overflow: hidden; opacity: 0.55;
    transition: opacity 0.15s, border-color 0.15s;
    display: flex; gap: 1px; background: #333;
  }
  .thumb:hover { opacity: 0.85; }
  .thumb.active { border-color: #f0e040; opacity: 1; }
  .thumb img { width: 28px; display: block; }
  @media (max-width: 600px) {
    #header { padding: 28px 16px 6px; }
    #header h1 { font-size: 1.5rem; letter-spacing: 2px; }
    #header .byline { font-size: 0.85rem; }
    #header .contributors { font-size: 0.65rem; }
    #viewer { padding: 10px 0 6px; gap: 0; position: relative; }
    #book { max-width: 100%; }
    .page-frame { max-width: 100%; box-shadow: 0 4px 16px rgba(0,0,0,0.5); border-radius: 2px; }
    .nav-btn {
      position: absolute; top: 50%; transform: translateY(-50%);
      width: 36px; height: 56px; font-size: 0.9rem; z-index: 10;
      background: rgba(0,0,0,0.28); color: #fff;
    }
    .nav-btn:hover:not(:disabled) { background: rgba(0,0,0,0.45); color: #fff; }
    #prevBtn { left: 4px; }
    #nextBtn { right: 4px; }
  }
</style>
</head>
<body>

<div id="header">
  <h1>EXTRA CHEESE</h1>
  <div class="byline">By NAHreally</div>
  <div class="contributors">with Nate LeBlanc and Thomas Mattera</div>
</div>
<div id="viewer">
  <button class="nav-btn" id="prevBtn" onclick="navigate(-1)">&#9664;</button>
  <div id="book"></div>
  <button class="nav-btn" id="nextBtn" onclick="navigate(1)">&#9654;</button>
</div>
<div id="thumb-strip"></div>
<div style="width:100%;max-width:700px;margin:16px auto 32px;padding:0 12px;">
  <iframe style="border: 0; width: 100%; height: 472px;" src="https://bandcamp.com/EmbeddedPlayer/album=1340709460/size=large/bgcol=ffffff/linkcol=0687f5/artwork=none/transparent=true/" seamless><a href="https://threedollarpistol.com/album/extra-cheese">EXTRA CHEESE by NAHreally</a></iframe>
</div>

<script>
PAGES_PLACEHOLDER

const TOTAL_SPREADS = PAGES.length / 2;
const TOTAL_PAGES = PAGES.length;
let currentSpread = 0;
let currentPage = 0;

function isMobile() { return window.innerWidth <= 600; }

function render() {
  const book = document.getElementById('book');
  book.innerHTML = '';

  if (isMobile()) {
    // Single page mode
    const page = PAGES[currentPage];
    const pf = document.createElement('div'); pf.className = 'page-frame';
    const img = document.createElement('img');
    img.src = 'data:image/jpeg;base64,' + page.src; img.alt = page.label;
    pf.appendChild(img); book.appendChild(pf);

    document.getElementById('prevBtn').disabled = currentPage === 0;
    document.getElementById('nextBtn').disabled = currentPage >= TOTAL_PAGES - 1;

    document.querySelectorAll('.thumb').forEach((t, i) =>
      t.classList.toggle('active', i === currentPage));
    const at = document.querySelectorAll('.thumb')[currentPage];
    if (at) at.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });

  } else {
    // Two-page spread mode
    const [left, right] = [PAGES[currentSpread * 2], PAGES[currentSpread * 2 + 1]];

    const lf = document.createElement('div'); lf.className = 'page-frame';
    const li = document.createElement('img');
    li.src = 'data:image/jpeg;base64,' + left.src; li.alt = left.label;
    lf.appendChild(li); book.appendChild(lf);

    const spine = document.createElement('div'); spine.id = 'spine'; book.appendChild(spine);

    const rf = document.createElement('div'); rf.className = 'page-frame';
    const ri = document.createElement('img');
    ri.src = 'data:image/jpeg;base64,' + right.src; ri.alt = right.label;
    rf.appendChild(ri); book.appendChild(rf);

    document.getElementById('prevBtn').disabled = currentSpread === 0;
    document.getElementById('nextBtn').disabled = currentSpread >= TOTAL_SPREADS - 1;

    document.querySelectorAll('.thumb').forEach((t, i) =>
      t.classList.toggle('active', i === currentSpread));
    const at = document.querySelectorAll('.thumb')[currentSpread];
    if (at) at.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  }
}

function navigate(dir) {
  if (isMobile()) {
    currentPage = Math.max(0, Math.min(TOTAL_PAGES - 1, currentPage + dir));
    currentSpread = Math.floor(currentPage / 2);
  } else {
    currentSpread = Math.max(0, Math.min(TOTAL_SPREADS - 1, currentSpread + dir));
    currentPage = currentSpread * 2;
  }
  render();
}

function buildThumbs() {
  const strip = document.getElementById('thumb-strip');
  strip.innerHTML = '';
  if (isMobile()) {
    // One thumbnail per page
    for (let i = 0; i < TOTAL_PAGES; i++) {
      const thumb = document.createElement('div');
      thumb.className = 'thumb' + (i === 0 ? ' active' : '');
      const img = document.createElement('img'); img.src = 'data:image/jpeg;base64,' + PAGES[i].src;
      thumb.appendChild(img);
      thumb.onclick = () => { currentPage = i; currentSpread = Math.floor(i / 2); render(); };
      strip.appendChild(thumb);
    }
  } else {
    // One thumbnail per spread
    for (let i = 0; i < TOTAL_SPREADS; i++) {
      const [l, r] = [PAGES[i * 2], PAGES[i * 2 + 1]];
      const thumb = document.createElement('div');
      thumb.className = 'thumb' + (i === 0 ? ' active' : '');
      const li = document.createElement('img'); li.src = 'data:image/jpeg;base64,' + l.src;
      const ri = document.createElement('img'); ri.src = 'data:image/jpeg;base64,' + r.src;
      thumb.appendChild(li); thumb.appendChild(ri);
      thumb.onclick = () => { currentSpread = i; currentPage = i * 2; render(); };
      strip.appendChild(thumb);
    }
  }
}

// Swipe support for mobile
let touchStartX = 0;
document.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; });
document.addEventListener('touchend', e => {
  const delta = e.changedTouches[0].clientX - touchStartX;
  if (Math.abs(delta) > 50) navigate(delta < 0 ? 1 : -1);
});

document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') navigate(1);
  if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   navigate(-1);
});

let lastMobile = isMobile();
window.addEventListener('resize', () => {
  const mobile = isMobile();
  if (mobile !== lastMobile) { lastMobile = mobile; buildThumbs(); }
  render();
});

buildThumbs();
render();
</script>
</body>
</html>'''


def main():
    root = Path(__file__).parent.parent
    pages_dir = root / "pages"
    output_dir = root / "output"
    output_dir.mkdir(exist_ok=True)

    print("Building PAGES data...")
    pages = build_pages(pages_dir)
    print(f"  {len(pages)} pages encoded")

    pages_js = "const PAGES = " + json.dumps(pages) + ";"
    html = HTML_TEMPLATE.replace("PAGES_PLACEHOLDER", pages_js)

    out_path = output_dir / "extra_cheese_flipbook.html"
    with open(out_path, "w") as f:
        f.write(html)

    # Also write to docs/index.html for GitHub Pages
    docs_dir = root / "docs"
    docs_dir.mkdir(exist_ok=True)
    docs_path = docs_dir / "index.html"
    with open(docs_path, "w") as f:
        f.write(html)

    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f"\nWritten: {out_path}")
    print(f"Written: {docs_path} (GitHub Pages)")
    print(f"Size: {size_mb:.1f} MB")
    print(f"Spreads: {len(pages) // 2}")


if __name__ == "__main__":
    main()
