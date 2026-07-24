---
name: mountain-elopement-story
description: >
  Create a new Mountain Elopement story (portfolio-item) in build.py from a folder of
  photos plus a short blurb about the couple/day. Recovers full-resolution originals from
  tiny "Blog" exports, optimizes to WebP, wires the story in all four languages (EN/DE/ES/IT),
  and keeps titles/alt/text distinct from any hochzeitsfotograf.tirol post on the same subject
  (anti-cannibalization). Use whenever Andreas sends "here are the images + a few sentences,
  make me a story like the others."
---

# Mountain Elopement — new story from photos + a short text

Repo: `/Users/blitzkneisser/Desktop/Mountain Elopement/mountain-elopement`
Single source of truth: **`build.py`** (stdlib only). Static output → GitHub Pages
(`Blitzi9188/mountain-elopement-preview`). Live: https://blitzi9188.github.io/mountain-elopement-preview/

The user gives you: a **photo folder** (often on an external drive) and a **short blurb**
(couple names, location, what happened, the highlight). You produce a full editorial story
that matches every other story on the site.

---

## 0 · Golden rules

- **Match the existing stories exactly** — same structure, same tone (warm, editorial, "we"
  as the photo/planning team). Read a couple of existing `PI_TEXT` entries first and mirror them.
- **Anti-cannibalization (critical).** hochzeitsfotograf.tirol covers the same regions in German.
  Before writing, check `.../Neuer Versuch/content/journal/*.md` for any post on the SAME place/theme
  and read its `title / titleEn / seoDescription / teaserDescription`. Your **story title**
  (which is also the `alt` text on every gallery image AND the link text on the stories grid)
  and your **lead/description** must use a **different angle and different wording**. E.g. the DE
  site had "Regenhochzeit am Pragser Wildsee" / "A Rainy Wedding at Lago di Braies" → the
  Mountain-Elopement story led on **boats + lakeside pizza** instead ("Wooden Boats and Lakeside
  Pizza — a Lago di Braies Elopement"), using *Elopement* not *Hochzeit/Wedding*.
- **Headers/hero must be landscape (Querformat).** Portrait heroes crop badly. The helper refuses
  a portrait hero.
- **Only 20 gallery photos show** (`MAX_GALLERY=20`). Curate the best 20 in narrative order;
  filenames `01.webp…20.webp` set the order.
- Never invent facts. Describe only what the photos and the blurb actually show.

---

## 1 · Get & prepare the images

Folders on the drive often look like `10.06 Sussette & Gabriel | Lago/` with `Blog/`, `Photos/`,
`ARW/`, `INSTA/`. The curated **`Blog/`** selection is sometimes exported as tiny 60×40 px
thumbnails — unusable directly. The full-res frames live in **`Photos/`**. The helper recovers
the full-res version of each Blog select by matching Adobe's `OriginalDocumentID` (per-photo,
stable across exports), then optimizes to WebP.

**Recon first** — build a labelled contact sheet and view it to plan the edit:

```bash
python3 .claude/skills/mountain-elopement-story/scripts/prepare_images.py \
  --parent "/Volumes/2026 II/Elopement" --match "Sussette" \
  --contact /tmp/contact.jpg
```

Open `/tmp/contact.jpg`, then decide:
- the **narrative order** of source numbers (arrival → ceremony/rings → portraits/boats →
  the highlight → celebration), and
- which **landscape** frame is the hero.

**Commit the curated images** into the repo (position 1..N → `01.webp`…; `--hero` → next free `sNN.webp`):

```bash
python3 .claude/skills/mountain-elopement-story/scripts/prepare_images.py \
  --parent "/Volumes/2026 II/Elopement" --match "Sussette" \
  --repo "$PWD" --slug <SLUG> \
  --order 1 2 8 3 4 5 6 24 23 17 21 20 25 7 12 9 15 11 16 31 --hero 21
```

The script prints the hero image id (e.g. `s23`) — use it in the STORIES tuple.
Optimization params (keep consistent): `exif_transpose → RGB → thumbnail((1600,1600)) →
WEBP quality=82 method=6`. Each file lands ~80–320 KB.

If there is no `Photos/` folder (Blog is already full-res) or no `Blog/` folder (use `Photos/`
directly), the helper handles both.

---

## 2 · Wire the story in `build.py` (four edits)

Pick a **slug** that is distinct from existing ones (there is already
`lago-di-braies-elopement`), descriptive of the differentiating angle.

**(a) `STORIES` list** (after the last entry). Tuple is
`(num, slug, imgnum, [cats], {en,de,es title})`. `num` = next integer, `imgnum` = the `sNN`
the helper printed. Cats come from `CATS` (`couple, dolomites, mountain, lake, elopement,
engagement`); the first two show as the card tag.

```python
 (18,'rainy-lago-di-braies-pizza-elopement','s23',['elopement','lake','dolomites'],
   {'en':'Wooden Boats and Lakeside Pizza &mdash; a Lago di Braies Elopement',
    'de':'Ruderboote und Pizza am Pragser Wildsee &mdash; ein Elopement',
    'es':'Barcas de remos y pizza en el Lago di Braies &mdash; un elopement'}),
```

**(b) `IT_ST`** — add the Italian title keyed by slug:

```python
'rainy-lago-di-braies-pizza-elopement':'Barche a remi e pizza al Lago di Braies &mdash; un elopement'
```

**(c) `PI_TEXT`** — the story body, all four languages, keys `lead, p1, p2, quote`:
- `lead` — one evocative sentence (the promise of the day). Also the meta description.
- `p1` — the day itself: place, ceremony, the specific things in the photos.
- `p2` — the highlight + the "we make it effortless" note (planning/weather/logistics).
- `quote` — a short pull-quote (rendered ~40% into the gallery). Keep it distinct from the
  hochzeitsfotograf teaser line.

Mirror the length and cadence of neighbouring `PI_TEXT` entries. Use HTML entities
(`&mdash; &rsquo; &euro; &thinsp;`), never raw `—`/`'` inside the Python strings.

**(d) Nothing else** — `STORYBY`, category pages, sitemap, the stories grid and the IT title
merge (`for s in STORIES: s[4]['it']=IT_ST[s[1]]`) all pick the new story up automatically.

---

## 3 · Build, verify, show, ship

```bash
python3 build.py && python3 verify.py     # expect "0 broken" and "gallery missing: []"
```

Spot-check the generated page (all four langs exist under `portfolio-item/<slug>/`,
`de/…`, `es/…`, `it/…`; 20 gallery imgs; hero = your `sNN`; alt = the title). A quick local
static server (`python3 -m http.server 8777`) + screenshot is good proof for the user, who
reviews visually.

Commit and push (tokens are supplied by the user; **always redact** them in any echoed output;
never commit secrets):

```bash
git add -A && git commit -m "Neue Story: <Couple> am <Location> (Regen + Pizza)"
git push "https://x-access-token:${TOKEN}@github.com/Blitzi9188/mountain-elopement-preview.git" \
  HEAD:refs/heads/main 2>&1 | sed "s/${TOKEN}/***REDACTED***/g"
```

Ask before pushing unless the user already said to ship.

---

## Quick checklist

- [ ] Contact sheet reviewed; 20-frame narrative order + landscape hero chosen
- [ ] Full-res recovered (OID match) & optimized to WebP (≤1600 px, q82)
- [ ] Slug distinct from existing stories
- [ ] Title / alt / lead **differ in angle + wording** from any hochzeitsfotograf.tirol post
- [ ] STORIES + IT_ST + PI_TEXT added (4 languages, HTML entities)
- [ ] `build.py` + `verify.py` clean (0 broken, gallery present)
- [ ] Visual spot-check, then commit & push (token redacted)
