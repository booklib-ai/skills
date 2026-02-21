# After

A pricing card with clear visual hierarchy achieved through size scale, weight contrast, and strategic color — the price is immediately scannable and the CTA stands out.

```css
/* Pricing card — clear hierarchy: plan name → price → description → features → CTA */
.pricing-card {
  padding: 32px;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 0 1px 3px rgba(0, 0, 0, 0.06);
}

/* Primary: the plan name — bold, medium size, dark */
.plan-name {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: hsl(217, 71%, 53%);   /* brand accent — signals plan identity */
  margin-bottom: 12px;
}

/* Hero element: price — the largest, heaviest thing on the card */
.plan-price {
  font-size: 48px;
  font-weight: 700;
  color: hsl(222, 47%, 11%);   /* near-black — maximum contrast */
  line-height: 1;
  margin-bottom: 4px;
}

.plan-billing-cycle {
  font-size: 13px;
  font-weight: 400;
  color: hsl(215, 16%, 57%);   /* light grey — tertiary, supporting */
  margin-bottom: 20px;
}

/* Secondary: description — readable but not competing with price */
.plan-description {
  font-size: 15px;
  font-weight: 400;
  color: hsl(215, 16%, 40%);   /* medium grey */
  line-height: 1.6;
  margin-bottom: 24px;
}

/* Tertiary: feature list — smallest, least emphasis */
.plan-feature {
  font-size: 14px;
  font-weight: 400;
  color: hsl(215, 16%, 47%);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* CTA: high contrast, full width, inviting */
.cta-button {
  width: 100%;
  padding: 14px;
  font-size: 15px;
  font-weight: 600;
  background-color: hsl(217, 71%, 53%);
  color: #ffffff;
  border: none;
  border-radius: 6px;
  margin-top: 28px;
  cursor: pointer;
}

.cta-button:hover {
  background-color: hsl(217, 71%, 46%);
}
```

Key improvements:
- Three-tier hierarchy established using size (48px → 15px → 14px → 13px), weight (700 → 600 → 400), and color (near-black → medium grey → light grey) — no element competes with the price (Ch 2: Visual Hierarchy)
- HSL colors replace raw hex — the system is transparent and the grey scale is predictable (Ch 5: Build a color system with HSL)
- `box-shadow` with two layered shadows replaces the flat `border: 1px solid #ccc` — the card lifts off the page with realistic depth (Ch 6: Depth and shadow elevation)
- `.plan-name` uses uppercase + letter-spacing as a tertiary-element technique — it occupies a clear role without competing with the price despite appearing first (Ch 2: De-emphasize labels, emphasize values)
- Consistent spacing from the scale (12, 20, 24, 28px) replaces arbitrary margins — related elements are visually grouped (Ch 3: Spacing and layout)
- CTA `padding: 14px` and `font-weight: 600` make the button unmistakably actionable, distinct from all other text on the card (Ch 8: Finishing touches)
