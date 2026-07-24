#!/usr/bin/env python3
"""
prepare_images.py — reusable image pipeline for a new Mountain Elopement story.

What it does
------------
1. Finds the photos for a couple even when the path contains spaces / "|" (Finder
   folders like "10.06 Sussette & Gabriel | Lago") by walking a parent dir.
2. If a curated "Blog" folder exists but the files are tiny (a botched small export),
   it recovers the FULL-RESOLUTION originals from a "Photos" folder by matching the
   Adobe XMP `OriginalDocumentID` (stable per photo across Lightroom exports).
   Falls back to a perceptual fingerprint if IDs are missing.
3. Optimizes the chosen photos to web-friendly WebP (exif-corrected, <=1600px, q82).
4. Writes an optional labelled contact sheet so a human can pick the best 20 and the order.

It deliberately does NOT decide the final gallery order or which frame is the hero —
that is human/editorial judgement. Run it in two modes:

  # Mode A — recon: build a contact sheet + report matches, change nothing in the repo
  python3 prepare_images.py --parent "/Volumes/2026 II/Elopement" --match "Sussette" \
      --contact /tmp/contact.jpg

  # Mode B — commit curated images into the repo
  #   --order is the narrative sequence of *source BLOG numbers* (or Photos indices),
  #   position 1..N -> img/gallery/<slug>/01.webp ..; --hero is the source number for sXX.webp
  python3 prepare_images.py --parent "/Volumes/2026 II/Elopement" --match "Sussette" \
      --repo "/Users/.../mountain-elopement" --slug rainy-lago-di-braies-pizza-elopement \
      --order 1 2 8 3 4 5 6 24 23 17 21 20 25 7 12 9 15 11 16 31 --hero 21

Notes
-----
* --match is a case-insensitive substring of the couple folder (e.g. a surname / first name).
* Source numbering: if a Blog folder exists, sources are its BLOG-<n>.jpg numbers; otherwise
  they are the sorted index (1-based) of the Photos folder.
* The hero MUST be a landscape (Querformat) frame — the script refuses a portrait hero.
* Next free sNN is auto-detected from <repo>/img/stories/.
"""
import argparse, os, re, sys

def _lazy_pil():
    from PIL import Image, ImageOps, ImageDraw  # noqa
    Image.MAX_IMAGE_PIXELS = None
    return Image, ImageOps, ImageDraw

def find_couple_dir(parent, match):
    """Return (couple_dir, blog_files{num:path}, photos[paths]) tolerating odd chars."""
    couple = None
    for name in os.listdir(parent):
        if match.lower() in name.lower() and not name.startswith('._') \
           and os.path.isdir(os.path.join(parent, name)):
            couple = os.path.join(parent, name); break
    if not couple:
        sys.exit(f"No couple folder under {parent!r} matching {match!r}")
    def jpgs(sub):
        d = os.path.join(couple, sub)
        if not os.path.isdir(d):
            return []
        return [os.path.join(d, f) for f in os.listdir(d)
                if f.lower().endswith(('.jpg', '.jpeg')) and not f.startswith('._')]
    blog = {}
    for p in jpgs('Blog'):
        m = re.search(r'(\d+)\.jpe?g$', os.path.basename(p), re.I)
        if m:
            blog[int(m.group(1))] = p
    photos = sorted(jpgs('Photos'))
    return couple, blog, photos

def original_document_id(path):
    Image, *_ = _lazy_pil()
    try:
        xmp = Image.open(path).info.get('xmp', b'')
        if isinstance(xmp, bytes):
            xmp = xmp.decode('utf-8', 'ignore')
        m = re.search(r'OriginalDocumentID[>=]["\']?([0-9A-Fa-f]{16,}|xmp[^"\'<> ]+)', xmp)
        return m.group(1) if m else None
    except Exception:
        return None

def fingerprint(path):
    Image, ImageOps, _ = _lazy_pil()
    im = ImageOps.exif_transpose(Image.open(path)).convert('L').resize((32, 32))
    return list(im.getdata())

def _dist(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)

def resolve_fullres(blog, photos):
    """Map each Blog number -> best full-res path. Prefer OID, fall back to perceptual."""
    if not photos:                       # no separate full-res set; Blog IS full-res
        return {n: p for n, p in blog.items()}
    by_oid = {}
    for p in photos:
        o = original_document_id(p)
        if o:
            by_oid.setdefault(o, []).append(p)
    out, need_fp = {}, []
    for n, bp in blog.items():
        o = original_document_id(bp)
        if o and o in by_oid:
            out[n] = by_oid[o][0]
        else:
            need_fp.append(n)
    if need_fp:                          # perceptual fallback
        pfp = [(p, fingerprint(p)) for p in photos]
        for n in need_fp:
            bfp = fingerprint(blog[n])
            out[n] = min(pfp, key=lambda pp: _dist(bfp, pp[1]))[0]
    return out

def optimize(src, dst, px=1600, q=82):
    Image, ImageOps, _ = _lazy_pil()
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    im.thumbnail((px, px))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, 'WEBP', quality=q, method=6)
    return im.size, os.path.getsize(dst) // 1024

def next_free_s(repo):
    d = os.path.join(repo, 'img', 'stories')
    used = {int(m.group(1)) for f in os.listdir(d)
            if (m := re.match(r's(\d+)\.webp$', f))}
    n = 1
    while n in used:
        n += 1
    return f's{n:02d}'

def contact_sheet(sources, out, cols=6, cell=300):
    Image, _, ImageDraw = _lazy_pil()
    from PIL import ImageOps
    items = sorted(sources.items())
    rows = (len(items) + cols - 1) // cols
    pad = 6
    W = cols * cell + pad * (cols + 1)
    H = rows * cell + pad * (rows + 1)
    sheet = Image.new('RGB', (W, H), (20, 20, 20))
    dr = ImageDraw.Draw(sheet)
    for i, (num, path) in enumerate(items):
        im = ImageOps.exif_transpose(Image.open(path)); im.thumbnail((cell, cell))
        r, c = divmod(i, cols)
        x = pad + c * (cell + pad); y = pad + r * (cell + pad)
        sheet.paste(im, (x + (cell - im.width) // 2, y + (cell - im.height) // 2))
        dr.rectangle([x, y, x + 34, y + 20], fill=(0, 0, 0))
        dr.text((x + 4, y + 4), str(num), fill=(255, 255, 0))
    sheet.save(out, 'JPEG', quality=88)
    return sheet.size

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--parent', required=True, help='dir that contains the couple folder')
    ap.add_argument('--match', required=True, help='substring of the couple folder name')
    ap.add_argument('--contact', help='write a labelled contact sheet here (recon mode)')
    ap.add_argument('--repo', help='mountain-elopement repo root (commit mode)')
    ap.add_argument('--slug', help='story slug (commit mode)')
    ap.add_argument('--order', nargs='+', type=int,
                    help='narrative sequence of source numbers -> 01.webp,02.webp,... (max 20 shown)')
    ap.add_argument('--hero', type=int, help='source number to become the landscape hero sNN.webp')
    args = ap.parse_args()

    couple, blog, photos = find_couple_dir(args.parent, args.match)
    sources = resolve_fullres(blog, photos) if blog else {i + 1: p for i, p in enumerate(photos)}
    print(f"couple: {couple}")
    print(f"blog selects: {len(blog)}  |  full-res photos: {len(photos)}  |  usable sources: {len(sources)}")

    if args.contact:
        sz = contact_sheet(sources, args.contact)
        print(f"contact sheet: {args.contact} {sz}")

    if args.repo and args.slug and args.order:
        Image, ImageOps, _ = _lazy_pil()
        # hero must be landscape
        if args.hero:
            hp = sources[args.hero]
            w, h = ImageOps.exif_transpose(Image.open(hp)).size
            if w <= h:
                sys.exit(f"--hero {args.hero} is portrait ({w}x{h}); pick a landscape (Querformat) frame")
            s = next_free_s(args.repo)
            sz, kb = optimize(hp, os.path.join(args.repo, 'img', 'stories', f'{s}.webp'))
            print(f"HERO {s} <- src {args.hero} {sz} {kb}KB   ->  use img '{s}' in the STORIES tuple")
        gdir = os.path.join(args.repo, 'img', 'gallery', args.slug)
        for i, num in enumerate(args.order[:20], 1):
            sz, kb = optimize(sources[num], os.path.join(gdir, f'{i:02d}.webp'))
            print(f"gallery {i:02d} <- src {num} {sz} {kb}KB")
        if len(args.order) > 20:
            print(f"NOTE: {len(args.order)-20} extra frames ignored — MAX_GALLERY=20 in build.py")

if __name__ == '__main__':
    main()
