#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt responsive WebP-Varianten (480/960/1600 px Breite) fuer jedes Bild in img/.

- stdlib + Pillow.
- Dateiname: <name>-480.webp, <name>-960.webp, <name>-1600.webp (Original bleibt liegen).
- Idempotent: bereits erzeugte Groessen werden uebersprungen.
- Kein Hochskalieren: Zielbreiten >= Originalbreite werden ausgelassen.
- Schreibt img/_manifest.json  {relpfad: {"w":..,"h":..,"v":[erzeugte Breiten]}}
"""
import os, json, sys
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGDIR = os.path.join(ROOT, 'img')
WIDTHS = [480, 960, 1600]
EXTS = ('.jpg', '.jpeg', '.png', '.webp')
SUFFIX = tuple(f'-{w}' for w in WIDTHS)

def is_variant(stem):
    return stem.endswith(SUFFIX)

def main():
    manifest = {}
    made = 0
    for dirpath, _dirs, files in os.walk(IMGDIR):
        for fn in files:
            low = fn.lower()
            if not low.endswith(EXTS):
                continue
            stem, ext = os.path.splitext(fn)
            if is_variant(stem):
                continue  # a generated variant, skip
            src = os.path.join(dirpath, fn)
            rel = os.path.relpath(src, ROOT).replace(os.sep, '/')
            try:
                im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
            except Exception as e:
                print('  SKIP (unreadable):', rel, e)
                continue
            w, h = im.size
            have = []
            for tw in WIDTHS:
                if tw >= w:
                    continue  # never upscale
                out = os.path.join(dirpath, f'{stem}-{tw}.webp')
                have.append(tw)
                if os.path.exists(out):
                    continue
                th = round(h * tw / w)
                im.resize((tw, th), Image.LANCZOS).save(out, 'WEBP', quality=82, method=6)
                made += 1
            manifest[rel] = {'w': w, 'h': h, 'v': have}
    with open(os.path.join(IMGDIR, '_manifest.json'), 'w') as f:
        json.dump(manifest, f, separators=(',', ':'), sort_keys=True)
    print(f'Bilder im Manifest: {len(manifest)} | neue Varianten erzeugt: {made}')

if __name__ == '__main__':
    main()
