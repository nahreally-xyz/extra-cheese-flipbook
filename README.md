# Extra Cheese Flipbook

Interactive HTML flipbook for *Extra Cheese* by NAHreally (Three Dollar Pistol, 2026).

A fully self-contained single HTML file — no server, no dependencies. Open in any browser.

## Setup

```bash
pip install pdf2image Pillow

# Place source PDFs:
# assets/source-pdfs/extra_cheese_cover.pdf
# assets/source-pdfs/Extra_Cheese_interior.pdf

bash scripts/rebuild.sh
open output/extra_cheese_flipbook.html
```

## Controls

| Action | Control |
|--------|---------|
| Next spread | → arrow key, click right page, or Next button |
| Previous spread | ← arrow key, click left page, or Prev button |
| Jump to spread | Click thumbnail in strip |

## Docs

- [`docs/page-index.md`](docs/page-index.md) — every page mapped by index, spread, and content
- [`docs/architecture.md`](docs/architecture.md) — HTML/JS structure, data format, build pipeline
- [`docs/enhancements.md`](docs/enhancements.md) — planned improvements and roadmap
- [`docs/project-context.md`](docs/project-context.md) — album info, collaboration history

## Structure

```
40 pages → 20 two-page spreads
Spread 1:  Front Cover + Title Page
Spreads 2–19: Interior content
Spread 20: On Cheesiness p.2 + Back Cover (green)
```

## Important

The source cover PDF is a **landscape** image with front and back side by side:
- **Right half** = Front Cover (cheese still life, white/red background)
- **Left half** = Back Cover (green background, man + dog + cheese prop)

This is handled correctly in `extract_pages.py`. Don't swap them.
