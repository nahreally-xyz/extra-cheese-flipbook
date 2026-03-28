# Architecture

## Output File

`output/extra_cheese_flipbook.html` — single self-contained HTML file, ~8.3 MB.
No server, no dependencies, no external resources. Opens directly in any browser.

---

## Data Structure

```javascript
const PAGES = [
  { src: "<base64 jpeg>", label: "Front Cover", role: "front" },
  { src: "<base64 jpeg>", label: "Page 1",      role: "interior" },
  // ... 38 interior pages ...
  { src: "<base64 jpeg>", label: "Back Cover",  role: "back" }
];
// Total: 40 items → 20 spreads
```

Each page object:
- `src` — base64-encoded JPEG (no data URI prefix in the array; prefix added in JS)
- `label` — display name shown in the page label bar and thumbnail tooltip
- `role` — `"front"` | `"interior"` | `"back"` (reserved for future logic)

---

## Spread Logic

```javascript
const TOTAL_SPREADS = PAGES.length / 2; // 20

function getSpreadPages(spreadIndex) {
  return [
    PAGES[spreadIndex * 2],      // left page
    PAGES[spreadIndex * 2 + 1]   // right page
  ];
}
```

State is a single integer `currentSpread` (0–19).

---

## Layout

```
[ left page frame ] [ spine div ] [ right page frame ]
```

- Both page frames are `flex: 1`, `max-width: 460px`
- Spine is `width: 8px` with a CSS gradient simulating a book binding
- Left frame: box-shadow leans left, `border-radius` on left corners
- Right frame: box-shadow leans right, `border-radius` on right corners
- Clicking left frame → `navigate(-1)`, clicking right frame → `navigate(1)`

---

## Navigation

**Buttons:** Prev / Next buttons call `navigate(dir)` which clamps `currentSpread` to `[0, TOTAL_SPREADS-1]`

**Keyboard:**
```javascript
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') navigate(1);
  if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   navigate(-1);
});
```

**Thumbnails:** Strip at bottom renders both pages of each spread as a paired thumbnail. Clicking any thumb sets `currentSpread` directly. Active spread highlighted with `border-color: #f0e040` (yellow).

---

## Render Cycle

```javascript
function render() {
  // 1. Clear book div
  // 2. Build left page frame with img
  // 3. Append spine div
  // 4. Build right page frame with img
  // 5. Update page indicator text ("Spread N of 20")
  // 6. Update page label ("Front Cover · Title Page")
  // 7. Toggle disabled state on Prev/Next buttons
  // 8. Sync thumbnail active state + scroll into view
}
```

`render()` is called after every navigation event and once on init.

---

## Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#1a1a1a` | Page body |
| Book page bg | `#f5f0e8` | Warm off-white, like real paper |
| Accent yellow | `#f0e040` | Buttons hover, active thumb border, header title |
| Subtitle/meta | `#888` | Secondary text |
| Button bg | `#2a2a2a` | Default button state |
| Spine gradient | `#3a3a3a → #888 → #ccc → #888 → #3a3a3a` | Book spine simulation |

---

## Build Pipeline

### Step 1: `scripts/extract_pages.py`
1. Converts `extra_cheese_cover.pdf` → one landscape JPEG
2. Crops right half → `pages/front_cover.jpg`
3. Crops left half → `pages/back_cover.jpg`
4. Converts `Extra_Cheese_interior.pdf` → `pages/interior_000.jpg` through `interior_037.jpg`
- DPI: 150 (balance of quality vs file size)
- Format: JPEG quality 85 (interior), 90 (covers)

### Step 2: `scripts/build_flipbook.py`
1. Reads all page images in order
2. Base64-encodes each
3. Builds `const PAGES = [...]` JS
4. Injects into HTML template
5. Writes `output/extra_cheese_flipbook.html`

---

## Image Specs

| Source | Resolution | Size |
|--------|-----------|------|
| Cover PDF (original) | 1787 × 1278 px | landscape |
| Front cover (cropped) | 894 × 1278 px | portrait |
| Back cover (cropped) | 893 × 1278 px | portrait |
| Interior pages | 912 × 1278 px | portrait |
| All at | 150 DPI | — |

---

## File Size Budget

- 40 pages × ~200KB average base64 ≈ 8.3 MB total HTML
- Acceptable for local use; would need lazy loading or a server-side approach for web deployment
