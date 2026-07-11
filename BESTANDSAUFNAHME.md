# Bestandsaufnahme — mountain-elopement.com (statischer Rebuild)

Stand: 2026-07-11 · Repo: `Dropbox/HP NEU/mountain-elopement` · Branch `main`
Quelle: temporärer Session-Output-Ordner (`…/outputs/prototype/`), gesichert per Erstimport.

**Kurzfazit:** Der Generator ist technisch solide (fehlerfreier, deterministischer Build,
0 Broken Links, gute Bild-Optimierung). Vor Go-Live fehlt jedoch strukturelles SEO:
**keine Canonicals, kein Open Graph, kein Schema.org/JSON-LD** auf allen 145 Seiten.
Das sind die eigentlichen Go-Live-Blocker.

---

## 1. Build — Fazit: **OK**

- `python3 build.py` → Exitcode **0**, Ausgabe `ALL DONE ['en', 'de', 'es', 'it']`.
- `python3 verify.py` → **5521 Refs geprüft, 0 broken**, `gallery missing: []`.
- **Determinismus:** Nach frischem Build `git status` = **0 geänderte Dateien**.
  Die eingecheckten HTMLs sind identisch mit einem frischen Build → reproduzierbar.
- Umfang: **145 generierte HTML-Seiten** in EN/DE/ES/IT.

---

## 2. SEO-Ist-Zustand — Fazit: **PROBLEM (Go-Live-Blocker)**

Geprüft an 4 Referenzseiten; die kritischen Lücken gelten **projektweit (alle 145 Seiten)**.

| Seite | `<title>` | `<meta description>` | H1 (Anzahl / Wortlaut) | canonical | OG | JSON-LD |
|---|---|---|---|---|---|---|
| `/index.html` | „Mountain Elopement — Where Adventure Meets Romance" | „Editorial elopement photography & planning in the Dolomites and the Alps." | **1** · „Adventure / Above the Clouds" | ❌ | ❌ | ❌ |
| `/how-to-elope-in-the-europe-mountains/` | „How to Elope in the European Mountains — Mountain Elopement" | „A guide to eloping in the Dolomites and the Alps." | **1** · „How to Elope in the European Mountains" | ❌ | ❌ | ❌ |
| `/get-in-touch/` | „Contact — Mountain Elopement" | „Tell us your story. Elopement photography & planning…" | **1** · „Get in Touch" | ❌ | ❌ | ❌ |
| `/portfolio-item/a-journey-of-love-and-adventure/` | „A Journey of Love on Top of Innsbruck — Mountain Elopement" | „Mountain elopement stories from the Dolomites and the Alps." | **1** · „A Journey of Love on Top of Innsbruck" | ❌ | ❌ | ❌ |

**Was da ist (OK):**
- Jede Seite hat **genau eine H1** (kein H1-Wildwuchs).
- `<title>` + `<meta description>` überall gesetzt (zentral in `TITLES`/`DESC`, build.py:633–648; IT in `IT_TITLES`/`IT_DESC`, build.py:516f).
- **hreflang-alternates** inkl. `x-default` sind vorhanden (build.py:539–542).

**Was fehlt (Blocker):** projektweiter grep über alle 145 HTML-Dateien:
- `application/ld+json` → **0 Seiten** (Schema.org fehlt komplett).
- `rel="canonical"` → **0 Seiten** (keine selbstreferenziellen Canonicals).
- `property="og:"` → **0 Seiten** (kein Open Graph / Social-Sharing-Meta).

Ursache zentral: `head()` (build.py:536) erzeugt hreflang + Favicon + GTM + Fonts + CSS,
aber weder canonical noch OG noch JSON-LD. → Ein Fix an einer Stelle greift für alle Seiten.

---

## 3. Bilder — Fazit: **OK** (kleine Optimierung nach Go-Live)

- `img/` gesamt: **46 MB**, **332 Bilddateien** (durchweg `.webp`).
- Größte 10 Dateien: max **0,7 MB** (`img/story/mission.webp`, `…/g07.webp`), Rest ≤0,5 MB → gut komprimiert, keine Ausreißer.
- **alt-Text:** von 1861 gerenderten `<img>`-Tags haben **0** kein `alt`-Attribut.
  Die einzigen leeren `alt=""` (69×) sind alle der Lightbox-Platzhalter `<img id="lbimg" alt="">`, der per JS befüllt wird → unkritisch.
- **loading="lazy":** 1100 von 1861 gesetzt (u. a. alle Galerie-Bilder, build.py:630f).
  Ohne lazy v. a. Story-Card-Thumbnails (`img/stories`, ~399, build.py:611) und Logos (`img/logo`, ~280).
  Story-Thumbnails stehen teils below-the-fold → **lazy nachrüsten ist eine sinnvolle, aber unkritische Optimierung.**

---

## 4. CMS-Vorbereitung (Decap) — Fazit: **FEHLT** (nicht Go-Live-kritisch)

- `build.py`: **971 Zeilen**.
- **Keine externen Content-Dateien** (keine `.md`/`.yaml`/`.json`-Inhalte) — **alle Texte sind hardcoded** im Python-Code.
- Datenmodell ist **inkonsistent**, was eine spätere Auslagerung erschwert:
  - EN/DE/ES liegen verschachtelt als `T[key][lang]` (build.py:32–270) plus `TITLES`, `DESC`, `CATS`, `STORIES`, `GUIDES`.
  - **Italienisch ist separat angeflanscht** als eigene Flach-Dicts `IT`, `IT_NAV`, `IT_LBL`, `IT_CATS`, `IT_ST`, `IT_TITLES`, `IT_DESC`, `IT_GUIDES`, `IT_EX` (build.py:453–531).

**Aufwands-Einschätzung Auslagerung nach Markdown/YAML für Decap:**
- **Mittel bis hoch.** Zwei Teilschritte:
  1. **Datenmodell vereinheitlichen** — IT in dieselbe `{key:{lang}}`-Struktur wie EN/DE/ES überführen (Voraussetzung, sonst wird die Auslagerung doppelt gebaut). Halber bis ganzer Tag.
  2. **Extraktion** — UI-Strings (`T`, `TITLES`, `DESC`) nach YAML pro Sprache, Repeatables (`STORIES`, `GUIDES`, `CATS`) nach Markdown-Collections; `build.py` liest daraus statt aus Inline-Dicts; `admin/config.yml` für Decap definieren. 1–2 Tage.
- Fazit: **klar machbar, aber eigenes Arbeitspaket** — nicht vor Go-Live nötig.

---

## Priorisierung

### Blocker vor Go-Live
1. **Schema.org / JSON-LD** auf allen Seiten (Organization; Unterseiten BreadcrumbList; portfolio-item ImageObject/Article) — fehlt komplett.
2. **Selbstreferenzielle Canonicals** auf allen 145 Seiten — fehlen komplett.
3. **Open Graph** (og:title/description/image/url) fürs Social-Sharing — fehlt komplett.
4. (Inhaltlich, separat beauftragt) **H1/Meta-Anpassung Startseite** auf Keyword „Mountain Elopement" + **Guide-H1** „How to Elope in Europe".

### Kann nach Go-Live
- `loading="lazy"` für below-the-fold Story-Thumbnails nachrüsten (build.py:611).
- `alt` für den Lightbox-`lbimg` dynamisch per JS mitsetzen (Feinschliff).
- CMS-Auslagerung nach Markdown/YAML + Decap-Anbindung (inkl. IT-Datenmodell vereinheitlichen).

---

### Randnotiz (aus separatem Auftrag mitgeprüft)
- Tippfehler `mounatin`: projektweiter grep → **keine Treffer** (existiert nicht im Projekt).
