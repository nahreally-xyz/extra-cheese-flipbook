# Enhancements Roadmap

Potential next steps identified during the original build session, roughly prioritized.

---

## High Value / Straightforward

### 1. Page-Flip Animation
Add a CSS 3D transform flip effect when turning pages. The standard approach:
- Each page is a `div` with `transform-style: preserve-3d`
- Outgoing page rotates `0deg → -180deg` around its spine edge (Y axis)
- Incoming page is the back face (`rotateY(180deg)` initially)
- Use `transition: transform 0.5s ease-in-out`
- Trigger on navigate, disable button clicks mid-animation

Libraries to consider: `turn.js` (jQuery-based, classic), or a pure CSS implementation.

### 2. Mobile Swipe Gestures
```javascript
let touchStartX = 0;
document.addEventListener('touchstart', e => touchStartX = e.touches[0].clientX);
document.addEventListener('touchend', e => {
  const delta = e.changedTouches[0].clientX - touchStartX;
  if (Math.abs(delta) > 50) navigate(delta < 0 ? 1 : -1);
});
```

### 3. Clickable Table of Contents
Interior page at index 3 (interior_002.jpg) is the TOC. Make the thumbnail or a TOC button jump to specific spreads by name.

Map from TOC entries to spread indices (see `docs/page-index.md`):
```javascript
const TOC = {
  "Moving at the Speed of Life": 3,
  "How to Listen to NAHreally":  5,
  "Extra Cheese Lyrics":         8,
  "1010 WINS":                   8,
  "Moderately Well":             9,
  "Umpteen":                    10,
  "Kick in the Pants":          11,
  "FUKWITME 2":                 12,
  "I Need a Hobby":             13,
  "You've Got a Friend Type Beat": 14,
  "Too Many Cooks":             15,
  "How We Always Gotta Be":     16,
  "Find Our Way":               17,
  "Human Error":                18,
  "On Cheesiness":              19,
};
```

---

## Medium Value

### 4. Zoom on Click / Lightbox
Double-clicking a page opens it full-screen for reading. ESC or click-outside closes.
- Use a `<dialog>` element or a fixed overlay div
- Show the single page at max readable size
- Optionally add pinch-zoom support for mobile

### 5. Dark / Light Mode Toggle
Currently hardcoded dark. A toggle button could switch to:
- Light: `body { background: #f0ede8 }`, page frames with drop shadows, dark header text
- Could respect `prefers-color-scheme` automatically

### 6. Reduce File Size
Current: ~8.3 MB. Options:
- Lower DPI to 120 (from 150) — may affect readability of small text
- Use WebP instead of JPEG — ~30% smaller, supported in all modern browsers
- Lazy-load pages as user approaches them (requires splitting data out of inline)

### 7. Progress Bar
A thin bar at top of viewport showing reading progress (currentSpread / totalSpreads).

---

## Larger Scope

### 8. Web Deployment Version
For hosting online rather than local file:
- Serve images separately (not base64 inline)
- Implement lazy loading / preload next spread
- Add URL hash navigation (`#spread-5`) so links can point to specific pages
- Consider `IntersectionObserver` for scroll-based page turning

### 9. Print Stylesheet
```css
@media print {
  #header, #controls, #thumb-strip { display: none; }
  #book { page-break-inside: avoid; }
  /* render each spread on its own printed page */
}
```

### 10. Thematic Extras
Matching the album's personality:
- Cheese emoji cursor 🧀
- Sound effect on page turn (subtle paper rustle)
- Easter egg: Konami code triggers something cheesy
- "Now Playing" overlay that lists the current track if you're on a lyrics spread

---

## Technical Debt / Cleanup

- Extract HTML template from `build_flipbook.py` into a separate `template.html` for easier editing
- Add a `--dpi` flag to `extract_pages.py` for easy quality tuning
- Cache bust: add a `?v=` hash to output filename based on source PDF modification time
- Consider splitting `pages_data.js` as a separate file that gets `<script src="">` included, making the template HTML smaller and more readable
