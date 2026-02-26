# After

A line chart with direct labels, a single accent color highlighting the insight, and an action title that states the finding — replacing three unreadable 3D pie charts.

```
CHART SPECIFICATION: Support Ticket Trend (Revised)

Chart type: Line chart (2D, no markers except at Q3 for annotation)
Title (action headline): "Product Bug tickets doubled in Q3 — prioritise QA investment"

Data: Ticket counts by category, Q1–Q3 2024
  Shown as: Single line chart, all three quarters on the x-axis

Visual choices:
  - All category lines: hsl(0, 0%, 75%) [light grey, 1.5px stroke]
  - "Product Bugs" line: hsl(4, 90%, 58%) [red accent, 2.5px stroke]
    — only this line is coloured; all others recede into context
  - Direct labels at Q3 data points (right side of chart)
    — no legend required
  - Single annotation on Product Bugs at Q3:
      "↑ 2× vs Q1" in matching red, placed above the data point

Axes:
  - X: Q1 2024, Q2 2024, Q3 2024 (three points, labelled clearly)
  - Y: Ticket volume (0–1,200), light grey gridlines, no border
  - Y-axis title removed — units are obvious from context

Clutter removed:
  - No 3D effects
  - No pie wedges (angles cannot be compared accurately)
  - No rainbow palette (colour carries no meaning when everything is coloured)
  - No legend (direct labels replace it)
  - No percentage labels on invisible slices
  - Chart border removed

Narrative context (slide title above chart):
  "Our Q3 support data shows one outlier that demands attention."

Call to action (below chart, in body text):
  "Recommendation: allocate 2 additional QA engineers to the mobile team
   before the Q4 release to prevent further escalation."
```

Key improvements:
- Line chart replaces pie charts — change over three time periods is exactly what a line chart communicates; pie charts cannot show trends (Ch 2: Choose an effective visual)
- Grey-out-then-highlight strategy: all lines are grey, only "Product Bugs" is red — the viewer's eye goes directly to the story without instruction (Ch 4: Focus attention with preattentive attributes — color)
- Direct labels at Q3 replace the legend — eliminates the back-and-forth between legend and chart (Ch 3: Eliminate clutter)
- Action headline "Product Bug tickets doubled in Q3 — prioritise QA investment" states the takeaway instead of describing the chart (Ch 7: Tell a story — horizontal logic, action titles)
- Annotation "↑ 2×" with the matching accent color amplifies the key data point without adding clutter (Ch 7: Annotation is storytelling)
- Explicit call-to-action in body text completes the three-act structure: context → insight → recommendation (Ch 7: Three-act structure)
