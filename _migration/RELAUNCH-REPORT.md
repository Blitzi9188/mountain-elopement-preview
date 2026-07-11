# Relaunch-Report — mountain-elopement.com (WordPress → statischer Rebuild)

Stand: 2026-07-11 · Repo: `Dropbox/HP NEU/mountain-elopement` · Branch `main`
Generator: `build.py` (reines stdlib-Python, keine Fremd-Pakete) → 4 Sprachen (EN/DE/ES/IT).

**Kurzfazit:** Der SEO-/Relaunch-Brief ist inhaltlich vollständig umgesetzt. Der Großteil war
bereits gebaut; dieser Durchgang hat nur noch die Deployment-Config finalisiert und den Zustand
dokumentiert. **Committen, nicht deployen** — Freigabe abwarten.

---

## Deployment

### Netlify-Build: Python-Build (Entscheidung)
`netlify.toml`:
```toml
[build]
  command = "python3 build.py"
  publish = "."
```
**Warum Python-Build statt vorab committetes HTML:** `build.py` nutzt ausschließlich die
Python-Standardbibliothek (`os, json, re, html`) — kein `pip install`, keine
`requirements.txt`. Netlifys Build-Image bringt Python 3 mit, der Generator läuft dort also
zuverlässig. Vorteil: das Git-Repo bleibt **quell-rein** (nur `build.py`/`css`/`img`, kein
generiertes HTML als Rauschen), und es gibt genau eine Wahrheitsquelle. Netlify baut bei jedem
Push frisch. (Fallback bei Build-Problemen wäre: generiertes HTML mitcommitten + Build-Command
entfernen — aktuell nicht nötig.)

### Redirects: nur `_redirects`
Redirect-Regeln liegen **nur** in `_redirects` (portabel: Netlify **und** Cloudflare Pages).
Der frühere doppelte `[[redirects]]`-Block in `netlify.toml` wurde entfernt, damit keine
konkurrierenden Regeln existieren. Einzige echte Regel:

| Alt (WordPress) | Neu | Status |
|---|---|---|
| `/blitzkneisser/` | `/our-team/` | **301** |

Details & Backlink-Analyse: siehe **`REDIRECT-REPORT.md`** (gleicher Ordner). 24 von 27 alten
URLs existieren 1:1 im neuen Build → kein Redirect nötig.

---

## SEO-Status (umgesetzt)

- **Startseite**: `<h1 class="hero-brand">Mountain Elopement</h1>` +
  `<h2 class="hero-sub">` Subline „Adventure Above the Clouds" / DE „Abenteuer über den Wolken".
- **How-to-Seite**: H1 „How to Elope in Europe" + eigener Meta-Title.
- **Canonicals**: self-referential, absolut `https`, mit Trailing-Slash, ohne `index.html`.
- **hreflang**: alle 4 Sprachen + `x-default` auf jeder Seite.
- **Schema.org JSON-LD** (`application/ld+json`):
  - **Organization** auf jeder indexierbaren Seite — `name`, `url`,
    `parentOrganization` = Blitzkneisser, `email` foto@blitzkneisser.com,
    `telephone` +43 664 39 18 228, `address` Rohracker 6, 6092 Birgitz, AT,
    `sameAs` Instagram. **Kein** LocalBusiness (bewusst).
  - **BreadcrumbList** auf allen Unterseiten.
  - **ImageObject** auf `portfolio-item/*`.
- **Contact-CTA** im Header, alle 4 Sprachen (Contact / Kontakt / Contacto / Contatto) →
  `/get-in-touch/`.
- **GTM** `GTM-MT6KGS4F` in `<head>` und `<body>`.
- **Danke-Seite** `/thank-you-for-your-inquiry/` in allen 4 Sprachen, `robots: noindex`,
  **nicht** in der Sitemap, ohne Canonical/JSON-LD.
- **Typo-Check**: „mounatin" existiert nirgends im Build.

---

## Sitemap & robots

- `sitemap.xml` enthält alle indexierbaren Seiten (EN/DE/ES/IT) mit hreflang-Alternates;
  die noindex-Danke-Seite ist **ausgeschlossen**.
- `robots.txt` verweist auf `https://mountain-elopement.com/sitemap.xml`.

---

## Build-Status

- `python3 build.py` → `ALL DONE ['en','de','es','it']`, Exitcode 0.
- `python3 verify.py` → siehe Konsolen-Output. Hinweis: solange die 6 Team-Bilder
  (`img/team/*.webp`) noch nicht abgelegt sind, meldet der Verifier deren Refs als fehlend —
  das ist erwartet und betrifft nur die Team-Seite.

---

## Offene TODOs

1. **`/proofing-gallery/proofing-gallery-locked/`** — Redirect-/Behandlungsentscheidung
   (410 Gone? Weiterleitung? eigene Galerie?) noch offen.
2. **Kontaktformular** ist Prototyp (`onsubmit="return false"`). Nach Scharfschaltung
   (Formspree/Resend) nach erfolgreichem Submit auf `/thank-you-for-your-inquiry/`
   weiterleiten, damit GTM die Conversion misst.
3. **Input-CSVs** liegen unter `our-packages/` — vor Go-Live nach `_migration/` verschieben,
   damit sie nicht ausgeliefert werden (`.gitignore` schließt `our-packages/*.csv` bereits aus).
4. **Team-Bilder** (`img/team/*.webp`) einbauen, dann rebuild bis 0 broken Refs.
