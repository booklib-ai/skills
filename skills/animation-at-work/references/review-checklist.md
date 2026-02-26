# Animation at Work — Design Review Checklist

Systematic checklist for reviewing web animations against the 5 chapters
from *Animation at Work* by Rachel Nabors.

---

## 1. Purpose & Patterns (Chapter 2)

- [ ] **Ch 2 — Purpose defined** — Does every animation have a clear purpose?
- [ ] **Ch 2 — Pattern classified** — Is each animation one of: transition, supplement, feedback, demonstration, decoration?
- [ ] **Ch 2 — Decorations justified** — Are decorative animations used sparingly and not distracting?
- [ ] **Ch 2 — Feedback present** — Do interactive elements provide animation feedback on user actions?
- [ ] **Ch 2 — Transitions contextual** — Do transitions convey spatial relationships between views?
- [ ] **Ch 2 — Demonstrations skippable** — Can instructional animations be dismissed or skipped?

---

## 2. Timing & Easing (Chapter 1)

- [ ] **Ch 1 — Duration appropriate** — Feedback <200ms, transitions 200–500ms, demos <1s?
- [ ] **Ch 1 — No excessive duration** — Are all functional animations under 1 second?
- [ ] **Ch 1 — Easing matches direction** — ease-out for enter, ease-in for exit, ease-in-out for reposition?
- [ ] **Ch 1 — No linear on UI** — Is linear easing only used for continuous motion (progress bars, spinners)?
- [ ] **Ch 1 — Stagger used** — Are grouped elements staggered for natural feel (overlapping action)?
- [ ] **Ch 1 — Anticipation present** — Do major animations have subtle preparatory motion?

---

## 3. Technology & Implementation (Chapter 3)

- [ ] **Ch 3 — Right tool chosen** — CSS transitions for simple, CSS animations for loops, WAAPI for control?
- [ ] **Ch 3 — Composite-only properties** — Are only `transform` and `opacity` animated?
- [ ] **Ch 3 — No layout thrashing** — Are `width`, `height`, `top`, `left`, `margin` NOT animated?
- [ ] **Ch 3 — will-change used correctly** — Applied before animation, removed after; not overused?
- [ ] **Ch 3 — RAIL compliance** — Animation frames under 16ms? Response under 100ms?
- [ ] **Ch 3 — requestAnimationFrame** — Are JS-driven animations using rAF, not setInterval/setTimeout?

---

## 4. Communication & Consistency (Chapter 4)

- [ ] **Ch 4 — Animation documented** — Are trigger, duration, easing, properties documented in specs?
- [ ] **Ch 4 — Motion tokens defined** — Are standard durations and easings defined as design tokens?
- [ ] **Ch 4 — Naming consistent** — Are animations named consistently across design and code?
- [ ] **Ch 4 — Storyboards for complex** — Do complex animations have storyboards or motion comps?
- [ ] **Ch 4 — Design system updated** — Are animation patterns documented in the motion design system?

---

## 5. Accessibility (Chapter 5)

- [ ] **Ch 5 — prefers-reduced-motion** — Is the media query implemented for all animations?
- [ ] **Ch 5 — Safe alternatives** — Are problematic animations replaced (not just removed) when motion reduced?
- [ ] **Ch 5 — No vestibular triggers** — No uncontrolled parallax, zooming, spinning, large slides?
- [ ] **Ch 5 — Flash rate safe** — No content flashing more than 3 times per second?
- [ ] **Ch 5 — Auto-play pausable** — Can all auto-playing animations be paused/stopped?
- [ ] **Ch 5 — Motion not required** — Is all information available without animation?
- [ ] **Ch 5 — Mobile tested** — Tested on real low-powered devices, not just dev machine?

---

## Quick Review Workflow

1. **Purpose pass** — Does every animation serve a classified purpose?
2. **Timing pass** — Are durations and easings appropriate for each pattern?
3. **Performance pass** — Only composite properties animated? No layout triggers?
4. **Accessibility pass** — prefers-reduced-motion implemented? No vestibular triggers?
5. **Consistency pass** — Are motion tokens and patterns documented and consistent?
6. **Prioritize findings** — Missing accessibility > performance issues > wrong timing > documentation gaps

## Severity Levels

| Severity | Description | Example |
|----------|-------------|---------|
| **Critical** | Accessibility or safety violation | No prefers-reduced-motion, flash rate >3/sec, seizure-triggering content |
| **High** | Performance or usability issue | Animating layout properties, >1s functional animation, missing feedback |
| **Medium** | Design quality gap | Wrong easing direction, no stagger, excessive decorations |
| **Low** | Polish or documentation | Missing motion tokens, undocumented animations, no storyboards |
