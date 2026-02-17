# Refactoring UI — Design Review Checklist

Systematic checklist for reviewing UI designs against the 9 chapters
from *Refactoring UI* by Adam Wathan & Steve Schoger.

---

## 1. Visual Hierarchy (Chapter 2)

- [ ] **Ch 2 — Clear hierarchy** — Can you tell what's most important at a glance?
- [ ] **Ch 2 — Three levers used** — Is hierarchy controlled through size, weight, AND color (not just size)?
- [ ] **Ch 2 — Labels de-emphasized** — Are labels secondary to the data they describe?
- [ ] **Ch 2 — No competing elements** — Does only one element dominate attention per section?
- [ ] **Ch 2 — Font weight ≥400** — Are all UI font weights 400 or above?
- [ ] **Ch 2 — Icon weight balanced** — Are bold icons toned down with lighter color?
- [ ] **Ch 2 — Visual ≠ document hierarchy** — Are heading sizes based on design role, not HTML tag?

---

## 2. Layout & Spacing (Chapter 3)

- [ ] **Ch 3 — Spacing scale used** — Are all spacing values from a defined scale (e.g., 4/8/12/16/24/32/48/64)?
- [ ] **Ch 3 — No arbitrary values** — Are there any one-off spacing values not in the scale?
- [ ] **Ch 3 — Grouping clear** — Are related elements closer together, unrelated elements farther apart?
- [ ] **Ch 3 — White space generous** — Is there enough breathing room, or is everything crammed?
- [ ] **Ch 3 — Not filling the screen** — Are content areas max-width constrained?
- [ ] **Ch 3 — Grid justified** — If a grid is used, does the layout actually need one?

---

## 3. Typography (Chapter 4)

- [ ] **Ch 4 — Type scale defined** — Are all font sizes from a defined scale (e.g., 12/14/16/18/20/24/30/36/48)?
- [ ] **Ch 4 — No arbitrary sizes** — Are there any one-off font sizes not in the scale?
- [ ] **Ch 4 — Line length controlled** — Are paragraphs 45–75 characters wide (20–35em max-width)?
- [ ] **Ch 4 — Line-height appropriate** — Taller for body (1.5+), shorter for headings (1–1.25)?
- [ ] **Ch 4 — No long centered text** — Is centered text limited to 1–2 lines?
- [ ] **Ch 4 — Numbers right-aligned** — Are numbers in tables right-aligned?
- [ ] **Ch 4 — Letter-spacing adjusted** — Tightened for large headings, widened for small uppercase?
- [ ] **Ch 4 — Good font choice** — Is the font appropriate for the personality (serif vs sans, round vs sharp)?

---

## 4. Color (Chapter 5)

- [ ] **Ch 5 — HSL-based palette** — Are colors defined in HSL (not random hex picks)?
- [ ] **Ch 5 — Shade scales built** — Does each color have 5–10 shades (not just one value)?
- [ ] **Ch 5 — 8+ grey shades** — Is there a full grey palette from near-white to near-black?
- [ ] **Ch 5 — No grey on color** — Is grey text avoided on colored backgrounds (use opacity or hue-match)?
- [ ] **Ch 5 — Contrast accessible** — Does body text meet 4.5:1 ratio? Large text 3:1?
- [ ] **Ch 5 — Perceived brightness** — Are yellow/green hues darkened and blue/purple lightened to balance?
- [ ] **Ch 5 — Color not sole indicator** — Is information available without relying on color alone?

---

## 5. Depth & Shadows (Chapter 6)

- [ ] **Ch 6 — Shadow scale defined** — Are shadows from a defined scale (xs/sm/md/lg/xl)?
- [ ] **Ch 6 — No arbitrary shadows** — Are there any one-off shadow values not in the scale?
- [ ] **Ch 6 — Two-shadow technique** — Do shadows combine a large diffuse + small tight shadow?
- [ ] **Ch 6 — Shadows match elevation** — Are modals higher than cards, cards higher than buttons?
- [ ] **Ch 6 — Interactive shadows** — Do clickable elements change shadow on hover?
- [ ] **Ch 6 — Overlap used** — Are overlapping elements creating depth where appropriate?

---

## 6. Images (Chapter 7)

- [ ] **Ch 7 — Text on images readable** — Is text over images using overlay, scrim, or shadow?
- [ ] **Ch 7 — Icons not scaled** — Are icons used at their designed size (not stretched)?
- [ ] **Ch 7 — Screenshots actual size** — Are screenshots captured at display size, not scaled down?
- [ ] **Ch 7 — User content controlled** — Are user-uploaded images using object-fit + fixed aspect ratios?
- [ ] **Ch 7 — Fallback backgrounds** — Do image containers have background-color for loading/transparent images?

---

## 7. Finishing Touches (Chapter 8)

- [ ] **Ch 8 — Borders minimal** — Are borders replaced with spacing, bg color, or box-shadow where possible?
- [ ] **Ch 8 — Empty states designed** — Do empty states have illustrations and calls to action?
- [ ] **Ch 8 — Defaults enhanced** — Are bullet lists, blockquotes, form inputs enhanced beyond browser defaults?
- [ ] **Ch 8 — Accent borders used** — Do cards or alerts have colored top/left accent borders?
- [ ] **Ch 8 — Backgrounds decorated** — Are plain white sections enhanced with subtle patterns or color?

---

## 8. Process & Systems (Chapters 1, 9)

- [ ] **Ch 1 — Personality consistent** — Does every design choice align with the chosen personality?
- [ ] **Ch 1 — Systems defined** — Are spacing, type, color, and shadow scales documented?
- [ ] **Ch 1 — Low fidelity first** — Was the design started in low fidelity before adding detail?
- [ ] **Ch 9 — Reusable patterns** — Can these design decisions be applied to other components?
- [ ] **Ch 9 — Design system updated** — Are new tokens/patterns documented in the system?

---

## Quick Review Workflow

1. **Hierarchy pass** — Squint test: can you identify the most important element in each section?
2. **Systems pass** — Are spacing, type sizes, colors, and shadows all from defined scales?
3. **Typography pass** — Line length, line-height, alignment, letter-spacing all correct?
4. **Color pass** — Accessible contrast? No grey on color? Shade scales used?
5. **Depth pass** — Consistent shadow scale? Interactive elevation changes?
6. **Polish pass** — Empty states designed? Fewer borders? Enhanced defaults? Accent borders?
7. **Prioritize findings** — Hierarchy > Accessibility > Systems > Typography > Depth > Polish

## Severity Levels

| Severity | Description | Example |
|----------|-------------|---------|
| **Critical** | Accessibility or readability violation | Contrast below 3:1, font weight <400, unreadable text on image |
| **High** | Hierarchy or usability issue | No clear visual hierarchy, ambiguous spacing/grouping, line-length >80ch |
| **Medium** | Inconsistency or design quality gap | Arbitrary spacing values, missing shade scale, inconsistent shadow use |
| **Low** | Polish or documentation | Missing accent borders, default empty states, undocumented tokens |
