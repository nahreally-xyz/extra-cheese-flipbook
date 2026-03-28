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
  #progress-wrap {
    width: 100%; max-width: 920px; padding: 6px 12px 2px;
    display: flex; flex-direction: column; align-items: center; gap: 4px;
  }
  #progress-bar-track {
    width: 100%; height: 2px; background: #444; border-radius: 2px; overflow: hidden;
  }
  #progress-bar-fill {
    height: 100%; background: #ffe033; border-radius: 2px;
    transition: width 0.2s ease;
  }
  #progress-label {
    font-size: 0.65rem; color: #666; letter-spacing: 1px;
  }
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
    #thumb-strip { display: none; }
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
<div id="progress-wrap">
  <div id="progress-bar-track"><div id="progress-bar-fill"></div></div>
  <div id="progress-label"></div>
</div>
<div id="thumb-strip"></div>
<div style="width:100%;max-width:700px;margin:16px auto 0;padding:0 12px;">
  <iframe style="border: 0; width: 100%; height: 515px;" src="https://bandcamp.com/EmbeddedPlayer/album=1340709460/size=large/bgcol=ffffff/linkcol=0687f5/artwork=none/transparent=true/" seamless><a href="https://threedollarpistol.com/album/extra-cheese">EXTRA CHEESE by NAHreally</a></iframe>
</div>
<div style="width:100%;max-width:700px;margin:24px auto 0;padding:0 12px;text-align:center;">
  <p style="font-family:'Bookman Old Style','Bookman',Georgia,serif;font-style:italic;font-size:1.1rem;color:#aaa;margin-bottom:14px;">Print copies of the Extra Cheese booklet are available for $10 + shipping at the link below.</p>
  <a href="https://www.lulu.com/shop/nahreally-and-nate-leblanc-and-thomas-mattera/extra-cheese/paperback/product-w4w96e7.html" target="_blank" style="display:inline-block;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;font-style:normal;font-size:0.9rem;font-weight:700;color:#111;background:#ffe033;padding:10px 28px;border-radius:4px;text-decoration:none;letter-spacing:1px;transition:background 0.15s;" onmouseover="this.style.background='#ffd000'" onmouseout="this.style.background='#ffe033'">ORDER A COPY</a>
  <div style="margin-top:8px;">
    <img src="data:image/png;base64,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" alt="Three Dollar Pistol" style="width:90px;opacity:0.6;filter:invert(1);margin-top:24px;margin-bottom:20px;">
  </div>
  <div style="margin-bottom:48px;">
    <p style="font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;font-size:0.75rem;color:#888;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">SUBSCRIBE TO THE NAHREALLY EMAIL LIST</p>
    <form id="substack-form" style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;">
      <input type="email" id="substack-email" placeholder="your@email.com" required style="font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;font-size:0.85rem;padding:9px 14px;border:1px solid #555;border-radius:4px;background:#2e2e2e;color:#eee;outline:none;width:220px;">
      <button type="submit" id="substack-btn" style="font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;font-size:0.8rem;font-weight:700;padding:9px 20px;background:#ffe033;color:#111;border:none;border-radius:4px;cursor:pointer;letter-spacing:1px;">SUBSCRIBE</button>
    </form>
    <script>
      document.getElementById('substack-form').addEventListener('submit', function(e) {
        e.preventDefault();
        var email = document.getElementById('substack-email').value;
        var btn = document.getElementById('substack-btn');
        fetch('https://nahreally.substack.com/api/v1/free', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({email: email})
        }).catch(function(){});
        btn.textContent = '✓';
        btn.style.background = '#4caf50';
        btn.style.color = '#fff';
        btn.disabled = true;
        document.getElementById('substack-email').disabled = true;
      });
    </script>
  </div>
</div>
<div id="progress-wrap">
  <div id="progress-bar-track"><div id="progress-bar-fill"></div></div>
  <div id="progress-label"></div>
</div>
<div id="thumb-strip"></div>



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

    const atEnd = currentPage >= TOTAL_PAGES - 1;
    document.getElementById('prevBtn').disabled = currentPage === 0;
    document.getElementById('nextBtn').disabled = false;
    document.getElementById('nextBtn').innerHTML = atEnd ? '↺' : '&#9654;';
    document.getElementById('nextBtn').style.fontSize = atEnd ? '1.1rem' : '0.9rem';
    document.getElementById('nextBtn').onclick = atEnd ? () => { currentPage = 0; currentSpread = 0; render(); } : () => navigate(1);
    document.getElementById('progress-bar-fill').style.width = ((currentPage + 1) / TOTAL_PAGES * 100) + '%';
    document.getElementById('progress-label').textContent = (currentPage + 1) + ' / ' + TOTAL_PAGES;

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

    const atEnd = currentSpread >= TOTAL_SPREADS - 1;
    document.getElementById('prevBtn').disabled = currentSpread === 0;
    document.getElementById('nextBtn').disabled = false;
    document.getElementById('nextBtn').innerHTML = atEnd ? '↺' : '&#9654;';
    document.getElementById('nextBtn').onclick = atEnd ? () => { currentSpread = 0; currentPage = 0; render(); } : () => navigate(1);
    document.getElementById('progress-bar-fill').style.width = ((currentSpread + 1) / TOTAL_SPREADS * 100) + '%';
    document.getElementById('progress-label').textContent = (currentSpread + 1) + ' / ' + TOTAL_SPREADS;

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
