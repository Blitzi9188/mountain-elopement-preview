#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt schlanke, selbst gehostete Schriften fuer mountain-elopement.

- Laedt die Variable Fonts (Newsreader roman+italic, Archivo) von Google Fonts.
- Subsettet auf Latin (U+0000-00FF deckt DE/ES/IT-Umlaute & Akzente ab) + noetige
  Interpunktion/Symbole. KEIN latinext (auf keiner der vier Sprachen genutzt).
- Newsreader: opsz-Achse gepinnt, wght-Achse 200..800 -> EINE Roman- + EINE Italic-Datei.
- Archivo: wght-Achse 400..700 -> EINE Datei (statt 4 Kopien der Variable Font).

Abhaengigkeiten:  pip install fonttools brotli
Aufruf:           python3 tools/fonts.py
"""
import os, re, sys, subprocess, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, 'fonts')
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
# Latin-1 + Interpunktion/Symbole (deckt ä ö ü ß à è é ì ò ù á é í ó ú ñ ab)
UNICODES = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,"
            "U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")

def fetch_css(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=30).read().decode()

def latin_woff2(css, want_italic):
    """Finde die woff2-URL des Latin-@font-face (roman oder italic) im css2-Output."""
    for block in re.findall(r'@font-face\s*\{[^}]*\}', css):
        ur = re.search(r'unicode-range:\s*([^;]+);', block)
        if not ur:
            continue
        low = ur.group(1).lower()
        is_latin = ('u+0-' in low or 'u+000' in low or 'u+00' in low)
        if not is_latin:
            continue
        style = re.search(r'font-style:\s*(\w+)', block).group(1)
        if (style == 'italic') != want_italic:
            continue
        return re.search(r'url\((https://[^)]+\.woff2)\)', block).group(1)
    return None

def download(url, path):
    data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
    open(path, 'wb').write(data)

def subset(src, out, axes):
    """axes: z.B. ['wght=200:800','opsz=18'] (opsz gepinnt -> Achse entfaellt)."""
    tmp = out + '.tmp.ttf'
    subprocess.run([sys.executable, '-m', 'fontTools.varLib.instancer', src, *axes,
                    '-o', tmp], check=True, stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable, '-m', 'fontTools.subset', tmp,
                    f'--output-file={out}', '--flavor=woff2', '--layout-features=*',
                    f'--unicodes={UNICODES}', '--desubroutinize'], check=True)
    os.remove(tmp)

def main():
    tmp = os.path.join(FONTS, '_src')
    os.makedirs(tmp, exist_ok=True)

    # 1) Newsreader (variable: wght 200..800, opsz 6..72), roman + italic
    ns_css = fetch_css("https://fonts.googleapis.com/css2?family=Newsreader:"
                       "ital,opsz,wght@0,6..72,200..800;1,6..72,200..800&display=swap")
    for italic, tag in [(False, 'roman'), (True, 'italic')]:
        url = latin_woff2(ns_css, italic)
        raw = os.path.join(tmp, f'newsreader-{tag}.woff2')
        download(url, raw)
        # wght-Achse behalten (200..800), opsz auf Default (18) gepinnt -> Achse entfaellt
        subset(raw, os.path.join(FONTS, f'newsreader-{tag}-latin.woff2'), ['wght=200:800', 'opsz=18'])

    # 2) Archivo (variable: wght 100..900) -> eine Datei, wght 400..700 (genutzte Staerken)
    ar_css = fetch_css("https://fonts.googleapis.com/css2?family=Archivo:wght@400..700&display=swap")
    url = latin_woff2(ar_css, False)
    raw = os.path.join(tmp, 'archivo.woff2')
    download(url, raw)
    subset(raw, os.path.join(FONTS, 'archivo-latin.woff2'), ['wght=400:700'])

    # 3) alte, jetzt ueberfluessige Dateien entfernen
    keep = {'newsreader-roman-latin.woff2', 'newsreader-italic-latin.woff2', 'archivo-latin.woff2'}
    removed = []
    for fn in os.listdir(FONTS):
        if fn.endswith('.woff2') and fn not in keep:
            os.remove(os.path.join(FONTS, fn)); removed.append(fn)
    # temp aufraeumen
    for fn in os.listdir(tmp):
        os.remove(os.path.join(tmp, fn))
    os.rmdir(tmp)

    total = 0
    print("Finale Schriften:")
    for fn in sorted(keep):
        s = os.path.getsize(os.path.join(FONTS, fn)); total += s
        print(f"  {s//1024:4} KB  {fn}")
    print(f"Summe: {total//1024} KB   (entfernt: {len(removed)} alte Dateien)")

if __name__ == '__main__':
    main()
