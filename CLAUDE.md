# CLAUDE.md — Extra Cheese Flipbook Project

## Project Overview

This repo builds and iterates on an **interactive HTML flipbook** for *Extra Cheese*, the 10th album by rapper **NAHreally** (Three Dollar Pistol Music LLC, 2026). The flipbook is a fully self-contained single HTML file (~8.3 MB) with all page images base64-encoded inside it — no server required.

The current working deliverable is `output/extra_cheese_flipbook.html`. Open it in any browser.

See `docs/` for full project context, page index, and enhancement roadmap.

---

## Repo Structure

```
extra-cheese-flipbook/
├── CLAUDE.md                  ← you are here
├── README.md
├── assets/
│   └── source-pdfs/           ← place original PDFs here
│       ├── extra_cheese_cover.pdf
│       └── Extra_Cheese_interior.pdf
├── pages/                     ← generated JPEGs (gitignored, reproducible)
│   ├── front_cover.jpg        ← right half of cover PDF
│   ├── back_cover.jpg         ← left half of cover PDF
│   ├── interior_000.jpg       ← title page
│   └── interior_001..037.jpg  ← remaining interior pages
├── scripts/
│   ├── extract_pages.py       ← PDF → JPEG extraction + cover crop
│   ├── build_flipbook.py      ← assembles HTML from page images
│   └── rebuild.sh             ← runs both scripts end-to-end
├── output/
│   └── extra_cheese_flipbook.html   ← final deliverable
└── docs/
    ├── page-index.md          ← every page, its index, and content
    ├── architecture.md        ← how the HTML/JS works
    ├── enhancements.md        ← planned next steps
    └── project-context.md     ← album info, collaboration history
```

---

## Quick Start

```bash
# 1. Install dependencies
pip install pdf2image Pillow

# 2. Place source PDFs in assets/source-pdfs/

# 3. Extract pages and build flipbook
bash scripts/rebuild.sh

# 4. Open output
open output/extra_cheese_flipbook.html
```

---

## Critical Facts to Never Get Wrong

1. **Cover crop direction:**
   - The cover PDF is one **landscape** image with front and back side by side
   - **RIGHT half** = front cover (cheese still life, white + red background)
   - **LEFT half** = back cover (green background, man holding cheese prop + white dog)
   - This was corrected in iteration 3 — don't revert it

2. **Page count:** 40 total pages → 20 two-page spreads
   - Index 0: Front Cover
   - Index 1–38: Interior pages (000–037)
   - Index 39: Back Cover

3. **Spread formula:** `spread N = pages[N*2]` (left) + `pages[N*2+1]` (right)

4. **Output is self-contained:** All images are base64-encoded inline. Do not introduce external image references or CDN dependencies.

---

## User's Working Preferences

- Concise, direct instructions — don't over-explain back
- Iterative: make the change, show the result, move on
- Describes things visually ("the one with the green") — interpret and act
- Wants working output, not lengthy discussion of approach
- Low ceremony — skip confirmations for straightforward changes

---

## Current Status

✅ Cover extracted and correctly split (front = right half, back = left half)
✅ 38 interior pages extracted at 150 DPI
✅ 20-spread flipbook with spine, thumbnails, keyboard nav, click-to-turn
✅ Single self-contained HTML file delivered

See `docs/enhancements.md` for what to build next.
