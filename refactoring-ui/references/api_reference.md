# Refactoring UI — Design Tokens & Systems Reference

Complete catalog of design systems, scales, and token values from all 9 chapters.

---

## Ch 1: Starting from Scratch

### Design Process
- Start with a feature, not a layout — don't begin with shell (navbar, sidebar, footer)
- Work low-fidelity first: grayscale, no shadows, system fonts, constrained sizes
- Design in cycles: design a simple version → build it → iterate on the real thing
- Hold the detail — don't waste time on perfect icons or color when the layout isn't right
- Don't over-design: only design the next thing you're going to build

### Choosing a Personality
Personality should be decided before picking any specific design values:

| Attribute | Elegant/Formal | Neutral/Safe | Playful/Fun |
|-----------|---------------|-------------|-------------|
| **Font** | Serif, thin sans-serif | System fonts, clean sans | Rounded sans, display fonts |
| **Color** | Muted, few hues, gold/navy | Blue, grey, safe palette | Bright, saturated, many hues |
| **Border-radius** | None or minimal (0–2px) | Small (4px) | Large (8px–full) |
| **Language** | Formal, professional | Neutral, clear | Casual, friendly, fun |

### Limiting Your Choices
- **Define systems in advance**: type scale, spacing scale, color palette, shadow scale, font weights, border-radius, width, opacity
- **Design by choosing from constrained options**, not by picking arbitrary values
- Systems provide speed (fewer decisions) and consistency (same values everywhere)

---

## Ch 2: Hierarchy is Everything

### The Three Levers of Hierarchy
1. **Size** — Larger = more important
2. **Weight** — Bolder = more important (use 600–700 for emphasis, 400–500 for normal; never go below 400 for UI text)
3. **Color** — Darker = more important

### Text Color System (Light Background)
| Role | Description | Example Value |
|------|-------------|---------------|
| **Primary** | Main content, headings, important text | `hsl(0, 0%, 10%)` — near-black |
| **Secondary** | Supporting text, descriptions, meta | `hsl(0, 0%, 45%)` — medium grey |
| **Tertiary** | Placeholders, disabled, timestamps | `hsl(0, 0%, 65%)` — light grey |

### Emphasis Techniques
- **Don't just make things bigger** — Try weight and color changes first
- **Emphasize by de-emphasizing surroundings** — Make competing elements less prominent
- **Labels as supporting cast** — Labels describe data; the data itself should be emphasized
- **Visual hierarchy ≠ document hierarchy** — An `<h1>` can be small if it's not the focal point
- **Bold icons need softer color** — Heavy visual weight + high contrast = too loud

### Icon Sizing in Context
- Icons next to text: match the font size or slightly smaller
- Icons as primary elements: can be larger, but tone down color/weight to balance
- Avoid scaling icons beyond their designed size — use different icon sets for different sizes

---

## Ch 3: Layout and Spacing

### Spacing Scale
A limited set of spacing values to use everywhere:

```
4px   — Tight: icon-to-label gap, inline element spacing
8px   — Compact: tight form fields, dense lists
12px  — Default small: label-to-input, list item padding
16px  — Default: standard padding, gaps between small elements
24px  — Comfortable: card padding, section gaps within a component
32px  — Roomy: between components in a group
48px  — Spacious: between distinct sections
64px  — Section: major section separators
96px  — Large: between page sections
128px — Extra large: hero/header padding
192px — Maximum padding for very large screens
256px — Full-width section padding on desktops
```

### Layout Principles
- **Start with too much white space, then remove** — Easier to tighten than to create breathing room
- **Don't fill the screen** — Use max-width (e.g., 600–800px for content, 1200px for full layouts)
- **Grids are a tool, not a rule** — Use them when you need proportional columns; many layouts don't need a grid
- **Relative sizing doesn't scale** — A 250px sidebar is fine at all widths; don't make it 20% of viewport
- **Dense UIs need smaller spacing** — Dashboards and data-heavy UIs can use tighter spacing from the scale
- **Generous UIs need larger spacing** — Marketing pages and hero sections use wider spacing

### Grouping with Spacing
- **Close = related** — Elements that belong together should have less space between them
- **Far = unrelated** — Use larger spacing to separate distinct groups
- **Ambiguous spacing is the enemy** — If spacing between items is uniform, the grouping is unclear

---

## Ch 4: Designing Text

### Type Scale
A limited set of font sizes to use everywhere:

```
12px — Fine print, captions, badges
14px — Secondary text, meta information, labels
16px — Body text (base size for most interfaces)
18px — Slightly emphasized body, lead paragraphs
20px — Large body, small headings, subheadings
24px — Section headings (h3 equivalent)
30px — Page section headings (h2 equivalent)
36px — Page titles, hero subheadings
48px — Display headings, hero titles
60px — Large display, landing page headlines
72px — Extra-large display, maximum emphasis
```

### Font Weight Scale
| Weight | Use |
|--------|-----|
| 400 (Regular) | Body text, descriptions, de-emphasized content |
| 500 (Medium) | Slightly emphasized body, labels, navigation |
| 600 (Semi-bold) | Headings, buttons, emphasized text |
| 700 (Bold) | Strong emphasis, primary headings |

**Never use weights below 400** for UI text — they're too hard to read.

### Line-Height Guidelines
| Font Size | Recommended Line-Height |
|-----------|------------------------|
| 12–14px | 1.5–1.75 (more leading for small text) |
| 16–18px | 1.5 (standard reading comfort) |
| 20–24px | 1.25–1.4 (can tighten slightly) |
| 30–48px | 1.1–1.25 (headings need less) |
| 48px+ | 1–1.1 (display text: nearly solid) |

### Line Length
- **Optimal**: 45–75 characters per line
- **Implementation**: `max-width: 20em` to `35em` on text containers
- **Centered text**: Only for 1–2 lines maximum; left-align everything else

### Letter-Spacing
| Context | Letter-Spacing |
|---------|---------------|
| Large headings (36px+) | -0.02em to -0.05em (tighten) |
| Normal body text | 0 (default) |
| Small uppercase labels | +0.05em to +0.1em (widen) |
| All-caps text | +0.05em (widen for readability) |

### Link Styling
- **In body text**: Colored + underlined (or underlined on hover)
- **In navigation**: No special color; use weight, underline-on-hover, or active indicator
- **In cards**: The whole card can be clickable; no link styling needed

---

## Ch 5: Working with Color

### HSL Color Model
```
hsl(hue, saturation%, lightness%)
```
- **Hue**: 0–360 (color wheel: 0=red, 120=green, 240=blue)
- **Saturation**: 0%=grey, 100%=vivid
- **Lightness**: 0%=black, 50%=pure color, 100%=white

### Building a Complete Palette

**Greys (8–9 shades)**:
| Shade | Lightness Range | Use |
|-------|----------------|-----|
| 50 | 97–98% | Page backgrounds, subtle tints |
| 100 | 93–95% | Card backgrounds, alternate rows |
| 200 | 85–90% | Borders, dividers |
| 300 | 75–80% | Disabled text, placeholder icons |
| 400 | 60–65% | Placeholder text |
| 500 | 45–50% | Secondary text |
| 600 | 35–40% | Icons, labels |
| 700 | 25–30% | Secondary headings |
| 800 | 15–20% | Primary text, headings |
| 900 | 5–10% | Maximum emphasis text |

**Primary/Accent colors (5–10 shades each)**:
Follow same pattern: pick middle (button bg), darkest (text), lightest (tinted bg), fill in between.

### Color Accessibility
| Standard | Ratio | When |
|----------|-------|------|
| WCAG AA (normal text) | 4.5:1 | Body text, labels, inputs |
| WCAG AA (large text) | 3:1 | Headings 18px+ bold, or 24px+ |
| WCAG AAA (normal) | 7:1 | Enhanced accessibility |

### Grey on Colored Backgrounds
**Problem**: Pure grey (`hsl(0, 0%, X%)`) looks washed out on colored backgrounds.

**Solutions**:
1. **Reduce opacity**: `rgba(255,255,255,0.8)` on dark bg; `rgba(0,0,0,0.5)` on light bg
2. **Hand-pick**: Choose a color with same hue as background but adjusted saturation/lightness

### Perceived Brightness by Hue
Hues have different apparent brightness at same HSL lightness:
- **Brightest** (feel lighter): Yellow (60°), Cyan (180°), Green (120°)
- **Darkest** (feel darker): Blue (240°), Red (0°), Magenta (300°)
- Adjust lightness values to compensate when building palettes across hues

### Dark Mode Adaptation
- Reverse the shade scale: shade-900 becomes background, shade-50 becomes text
- Reduce saturation slightly (vivid colors are harsh on dark backgrounds)
- Shadows are less visible on dark — use subtle glows or border accents instead
- Test carefully: contrast requirements still apply

---

## Ch 6: Creating Depth

### Shadow Elevation Scale

```css
--shadow-xs:  0 1px 2px rgba(0,0,0,0.05);
--shadow-sm:  0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
--shadow-md:  0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06);
--shadow-lg:  0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05);
--shadow-xl:  0 20px 25px rgba(0,0,0,0.15), 0 10px 10px rgba(0,0,0,0.05);
```

### Shadow Best Practices
- **Two shadows per level**: Large diffuse + small tight for realism
- **Raised elements**: Buttons, cards, navbars, floating action buttons
- **Inset elements**: Input fields, wells, pressed button states
- **Interactive shadows**: Increase shadow on hover (sm → md) to show clickability
- **Don't overdo flat design**: Some depth helps users understand interactive affordances
- **Keep it consistent**: Use only the defined scale; no random shadow values

### Depth Through Overlap
- Offset an element (e.g., card) so it overlaps a background section
- Creates visual layering without shadows
- Negative margins or absolute positioning to achieve the overlap

### Color and Depth
- **Lighter elements appear closer** to the viewer
- **Darker elements appear farther** away
- Use this with shadows: elevated elements can also be slightly lighter in bg color

---

## Ch 7: Working with Images

### Text on Images

| Technique | CSS | Best For |
|-----------|-----|----------|
| Dark overlay | `background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url(...)` | Hero sections |
| Lower brightness | `filter: brightness(0.7)` | Subtle dimming |
| Colorize | `filter: grayscale(100%); mix-blend-mode: multiply` + color overlay | Brand consistency |
| Text shadow | `text-shadow: 0 2px 4px rgba(0,0,0,0.5)` | Quick fix |
| Scrim/card | Semi-opaque `background-color` on text container | Readable blocks |

### Image Sizing

| Scenario | Approach |
|----------|----------|
| Icons at different sizes | Use different icon sets (16px, 24px, 32px) — don't scale |
| Screenshots in marketing | Capture at display size; don't scale down |
| User-uploaded avatars | `object-fit: cover` + fixed aspect ratio + bg color fallback |
| User-uploaded hero images | `object-fit: cover` + fixed height + handle extremes (panoramic, portrait) |

### Object-Fit Values
```css
object-fit: cover;   /* Crop to fill — best for avatars, hero images */
object-fit: contain;  /* Fit inside — best for product images, logos */
object-fit: fill;     /* Stretch — avoid for most UI use cases */
```

---

## Ch 8: Finishing Touches

### Accent Borders
```css
/* Top accent on card */
.card { border-top: 4px solid var(--primary-500); }

/* Left accent on alert */
.alert { border-left: 4px solid var(--warning-500); }

/* Color-code by type */
.alert-success { border-left-color: var(--success-500); }
.alert-danger  { border-left-color: var(--danger-500); }
```

### Replacing Borders
| Instead of Border | Try |
|-------------------|-----|
| Between list items | More padding/spacing between items |
| Around cards | Box-shadow (subtle shadow creates implied boundary) |
| Between sections | Different background color |
| Around inputs | Background color difference + subtle shadow |

### Empty States
- **Don't**: Show just "No items found" in grey text
- **Do**: Show an illustration + explanation + primary call to action
- **Example**: "No projects yet — Create your first project" with a big button
- Empty states are onboarding opportunities

### Custom Defaults
| Default Element | Upgrade |
|----------------|---------|
| Bullet lists | Icon lists (checkmarks, arrows, custom icons) |
| Blockquotes | Large border-left + background tint + italic |
| Form inputs | Colored focus ring, custom checkbox/radio |
| Tables | Alternating rows, sticky headers, row hover |
| Links | Custom underline color/thickness |

---

## Ch 9: Leveling Up

### Learning Approach
- **Steal from good designs** — Rebuild UIs you admire to understand why they work
- **Analyze decisions** — Ask "why does this work?" not just "what does it look like?"
- **Think in systems** — Every decision should fit into a reusable system
- **Look outside your domain** — SaaS, e-commerce, media, dashboards — all have lessons
- **Rebuild for practice** — Pick a well-designed app and recreate a page pixel-by-pixel

### Design System Assembly
Collect all your scales into one system:

```css
:root {
  /* Spacing */
  --space-1: 4px;   --space-2: 8px;   --space-3: 12px;
  --space-4: 16px;  --space-5: 24px;  --space-6: 32px;
  --space-8: 48px;  --space-10: 64px; --space-12: 96px;
  --space-16: 128px;

  /* Type */
  --text-xs: 12px;  --text-sm: 14px;  --text-base: 16px;
  --text-lg: 18px;  --text-xl: 20px;  --text-2xl: 24px;
  --text-3xl: 30px; --text-4xl: 36px; --text-5xl: 48px;

  /* Font Weight */
  --font-normal: 400; --font-medium: 500;
  --font-semibold: 600; --font-bold: 700;

  /* Shadows */
  --shadow-xs: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05);
  --shadow-xl: 0 20px 25px rgba(0,0,0,0.15), 0 10px 10px rgba(0,0,0,0.05);

  /* Border Radius */
  --radius-sm: 2px; --radius-md: 4px;
  --radius-lg: 8px; --radius-full: 9999px;

  /* Colors: define full shade scales for grey, primary, accent, etc. */
}
```
