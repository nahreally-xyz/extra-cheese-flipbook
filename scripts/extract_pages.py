#!/usr/bin/env python3
"""
extract_pages.py
Converts source PDFs into individual JPEG page images.

Usage:
    python scripts/extract_pages.py [--dpi 150]

Outputs to pages/ directory (created if missing).
"""

import argparse
import os
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io


def pdf_to_pil_images(pdf_path, dpi):
    """Render each page of a PDF to a PIL Image using PyMuPDF."""
    doc = fitz.open(str(pdf_path))
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    images = []
    for page in doc:
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    doc.close()
    return images


def main():
    parser = argparse.ArgumentParser(description="Extract PDF pages to JPEGs")
    parser.add_argument("--dpi", type=int, default=150, help="Render DPI (default: 150)")
    args = parser.parse_args()

    root = Path(__file__).parent.parent
    pages_dir = root / "pages"
    pages_dir.mkdir(exist_ok=True)

    cover_pdf = root / "assets" / "source-pdfs" / "extra_cheese_cover.pdf"
    interior_pdf = root / "assets" / "source-pdfs" / "Extra_Cheese_interior.pdf"

    # --- Cover ---
    print(f"Extracting cover at {args.dpi} DPI...")
    cover_imgs = pdf_to_pil_images(cover_pdf, args.dpi)
    assert len(cover_imgs) == 1, f"Expected 1 cover page, got {len(cover_imgs)}"

    cover = cover_imgs[0]
    w, h = cover.size
    mid = w // 2

    # IMPORTANT: Right half = front cover, Left half = back cover
    # (counterintuitive — the green side is on the left and is the BACK cover)
    front = cover.crop((mid, 0, w, h))   # right half
    back  = cover.crop((0,   0, mid, h)) # left half

    # --- Interior (extract first to get reference dimensions) ---
    print(f"\nExtracting {interior_pdf.name} at {args.dpi} DPI...")
    interior_imgs = pdf_to_pil_images(interior_pdf, args.dpi)
    print(f"  {len(interior_imgs)} pages found")

    for i, img in enumerate(interior_imgs):
        out_path = pages_dir / f"interior_{i:03d}.jpg"
        img.save(str(out_path), "JPEG", quality=85)
        print(f"  interior_{i:03d}.jpg: {img.size}")

    # Crop covers to match interior aspect ratio.
    # Front cover: crop from left, top, bottom (preserve right/spine edge).
    # Back cover:  crop from right, top, bottom (preserve left/spine edge).
    iw, ih = interior_imgs[0].size
    target_ratio = iw / ih  # e.g. 912/1278

    def crop_to_ratio(img, spine_side):
        cw, ch = img.size
        # Trim 12px from the outer (non-spine) edge first.
        outer_trim = 12
        if spine_side == 'right':
            new_w = cw - outer_trim
            x0, x1 = outer_trim, cw          # crop left edge
        else:
            new_w = cw - outer_trim
            x0, x1 = 0, cw - outer_trim      # crop right edge
        new_h = round(new_w / target_ratio)
        h_crop = ch - new_h
        top = h_crop // 2
        bot = h_crop - top
        return img.crop((x0, top, x1, ch - bot))

    front = crop_to_ratio(front, spine_side='right')
    back  = crop_to_ratio(back,  spine_side='left')

    front.save(str(pages_dir / "front_cover.jpg"), "JPEG", quality=90)
    back.save( str(pages_dir / "back_cover.jpg"),  "JPEG", quality=90)
    print(f"\n  front_cover.jpg (cropped): {front.size}")
    print(f"  back_cover.jpg  (cropped): {back.size}")

    print(f"\nDone. {2 + len(interior_imgs)} images written to pages/")


if __name__ == "__main__":
    main()
