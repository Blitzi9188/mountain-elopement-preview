# Redirect-Map & Migration — mountain-elopement.com (WordPress → statischer Rebuild)

Stand: 2026-07-11 · Repo: `Dropbox/HP NEU/mountain-elopement` · Branch `main`
Quelle der URL-Liste: `our-packages/export-all-urls-*.csv` (27 alte WP-URLs).

**Kurzfazit:** 24 der 27 alten URLs existieren im neuen Build 1:1 → kein Redirect nötig.
Nur **1 echter 301-Redirect** wird gesetzt (`/blitzkneisser/` → `/our-team/`).
Die Danke-Seite wird **neu gebaut** (kein Redirect, GTM-Conversion bleibt messbar) und
ist **noindex** + **nicht in der Sitemap**. Ein Fall (`proofing-gallery`) bleibt als **TODO** offen.

---

## Aufgabe 1 — Danke-Seite (neu gebaut, KEIN Redirect)

- Neu im Build: `/thank-you-for-your-inquiry/` in **allen 4 Sprachen**
  (`/`, `/de/`, `/es/`, `/it/…`), generiert von `build_thankyou()` in `build.py`.
- Inhalt: schlichte Bestätigung — H1 „Thank you" + „We've received your message and will
  get back to you within 48 hours." + Button zurück zur Startseite.
- **`<meta name="robots" content="noindex">` gesetzt** (via neuen `noindex`-Parameter in `head()`).
  Auf noindex-Seiten wird **kein** `rel="canonical"` und **keine** JSON-LD ausgegeben.
- **Grund fürs Neu-Bauen statt Redirect:** Auf dieser URL hängt vermutlich das
  GTM-Conversion-Tracking. Würde die URL verschwinden/umgeleitet, brächen die Messwerte.

**Formular-Check (`/get-in-touch/`):** Das Formular ist ein **Prototyp** — `<form … onsubmit="return false">`.
Es sendet/leitet **nirgendwohin** weiter und zeigt **nicht** auf die alte WP-URL.
→ **Kein Handlungsbedarf.** Wenn das Formular später scharf geschaltet wird (z. B. Formspree/Resend),
sollte es nach erfolgreichem Submit auf `/thank-you-for-your-inquiry/` weiterleiten (dann greift GTM).

---

## Aufgabe 2 — Redirects

### Echter Redirect (gesetzt)

| Alt (WordPress) | Neu | Status |
|---|---|---|
| `/blitzkneisser/` | `/our-team/` | **301** |

Begründung: `/blitzkneisser/` war die alte Autoren-/Team-Seite; Entsprechung im neuen Build ist `/our-team/`.

### Bewusst NICHT gesetzt (TODO)

- `/proofing-gallery/proofing-gallery-locked/` → **noch kein Redirect.**
  Passwortgeschützte Kundengalerie; Entscheidung offen. **TODO:** Ziel klären
  (eigene Galerie-Lösung? 410 Gone? Redirect auf Startseite/Kontakt?) und danach ergänzen.

### Keine Redirects nötig

24 der 27 alten URLs existieren 1:1 im neuen Build (Startseite, alle `portfolio-item/*`,
`our-packages`, `get-in-touch`, `stories-elopement-mountain`, `how-to-elope-in-the-europe-mountains`,
`imprint`, `privacy-policy`). Die Danke-Seite (Aufgabe 1) wird neu gebaut, nicht umgeleitet.

**Backlink-Hinweis:** Externe Backlinks bestehen laut Analyse **nur auf die Startseite**
(7 Links, 3 Domains). Alle Unterseiten haben keine externen Backlinks → das Redirect-Risiko
ist minimal; die Startseite bleibt unverändert erreichbar.

### Datei-Format & was greift

Zwei Varianten wurden im Repo-Root angelegt:

- **`_redirects`** — Netlify **und** Cloudflare Pages.
- **`netlify.toml`** — **nur** Netlify (Cloudflare Pages ignoriert Redirects hier).

**Empfehlung:** Es existiert noch keine Deployment-Config. Sobald das Ziel-Hosting feststeht:
- **Cloudflare Pages** → **`_redirects`** ist die einzige, die greift. `netlify.toml` löschen.
- **Netlify** → beide würden funktionieren; um Doppelregeln/Verwirrung zu vermeiden,
  **nur eine** behalten. `_redirects` ist die portablere Wahl (funktioniert auf beiden Hosts),
  daher empfehle ich, `_redirects` als führende Datei zu behalten und `netlify.toml` zu entfernen.

**Nicht beide gleichzeitig aktiv lassen.**

---

## Aufgabe 3 — Sitemap

- Neue `sitemap.xml` enthält **140 `<loc>`-Einträge** = alle indexierbaren Seiten in EN/DE/ES/IT
  (35 Seiten × 4 Sprachen), jeweils mit `hreflang`-Alternates inkl. `x-default`.
- Die **noindex-Danke-Seite steht NICHT in der Sitemap** (geprüft: 0 Treffer für `thank-you`),
  weil `build_thankyou()` bewusst **nicht** über `all_rels()` läuft.
- Die alte Yoast-Aufteilung (`page-sitemap.xml` + `portfolio-item-sitemap.xml`) wird durch
  **eine einzige** `sitemap.xml` ersetzt, die alle Seiten enthält — funktional gleichwertig.
- `robots.txt` verweist auf `https://mountain-elopement.com/sitemap.xml`.

---

## Build-Status

- `python3 build.py` → `ALL DONE ['en','de','es','it']`, Exitcode 0.
- `python3 verify.py` → **5761 Refs geprüft, 0 broken**, `gallery missing: []`.

---

## Offene TODOs

1. **`/proofing-gallery/proofing-gallery-locked/`** — Redirect-/Behandlungsentscheidung treffen.
2. **Ziel-Hosting festlegen** und die nicht genutzte Redirect-Datei (`_redirects` **oder** `netlify.toml`) entfernen.
3. **Kontaktformular scharf schalten** und nach Submit auf `/thank-you-for-your-inquiry/` weiterleiten
   (damit GTM-Conversion auf der neuen Danke-Seite feuert).
4. Input-CSVs liegen aktuell unter `our-packages/` (generiertes Verzeichnis) — vor Go-Live
   besser nach `_migration/` verschieben, damit sie nicht mit ausgeliefert werden.
