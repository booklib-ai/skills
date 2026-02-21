# After

The navigation drawer animation switches to composite-only properties (`transform` + `opacity`), uses `ease-out` easing, a 250ms duration, and respects `prefers-reduced-motion`.

```css
/* Nav drawer — animate only composite properties (transform, opacity) */
.nav-drawer {
  /* Position off-screen using transform — not width/height */
  transform: translateX(-280px);
  opacity: 0;
  width: 280px;         /* fixed dimensions, never animated */
  height: 100vh;
  overflow: hidden;
  background-color: #1a1a2e;
  /* ease-out: fast start → gentle stop — natural for entering elements (Ch 1) */
  transition:
    transform 250ms ease-out,
    opacity   200ms ease-out;
  /* Hint the browser to promote this element to its own compositor layer */
  will-change: transform;
}

.nav-drawer.open {
  transform: translateX(0);
  opacity: 1;
}

/* Menu items stagger in using animation-delay for follow-through (Ch 1) */
.nav-drawer .menu-item {
  opacity: 0;
  transform: translateX(-12px);
  transition:
    opacity   180ms ease-out,
    transform 180ms ease-out;
}

.nav-drawer.open .menu-item {
  opacity: 1;
  transform: translateX(0);
}

/* Stagger each item for natural overlapping action */
.nav-drawer.open .menu-item:nth-child(1) { transition-delay: 60ms; }
.nav-drawer.open .menu-item:nth-child(2) { transition-delay: 90ms; }
.nav-drawer.open .menu-item:nth-child(3) { transition-delay: 120ms; }
.nav-drawer.open .menu-item:nth-child(4) { transition-delay: 150ms; }

/* Accessibility: remove all motion for users who prefer it (Ch 5) */
@media (prefers-reduced-motion: reduce) {
  .nav-drawer,
  .nav-drawer .menu-item {
    transition: opacity 150ms linear !important;
    transform: none !important;
  }
}
```

Key improvements:
- `transform: translateX()` replaces `width`/`height` animation — `transform` and `opacity` are the only composite-only properties that animate on the GPU without triggering layout recalculation (Ch 3: Performance — composite-only properties)
- Duration reduced from 1.5s to 250ms — functional UI animations should be 200–500ms; 1.5s feels sluggish and blocks the user (Ch 1: Timing and duration)
- `ease-out` replaces `linear` — entering elements should start fast and slow to a stop; linear easing feels robotic for UI elements (Ch 1: 12 Principles — ease in / ease out)
- `will-change: transform` promotes the drawer to its own compositor layer, enabling smooth 60fps animation on mobile devices (Ch 3: will-change)
- Staggered `transition-delay` on menu items creates overlapping action — the drawer and its children don't all stop simultaneously, producing a more natural feel (Ch 1: 12 Principles — follow-through and overlapping action)
- `@media (prefers-reduced-motion: reduce)` is implemented — users with vestibular disorders receive a simple fade instead of a lateral sweep (Ch 5: Accessibility — prefers-reduced-motion)
