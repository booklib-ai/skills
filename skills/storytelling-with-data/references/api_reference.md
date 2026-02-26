# Storytelling with Data — Frameworks & Visual Reference

Complete catalog of chart types, principles, frameworks, and techniques
from all 10 chapters of *Storytelling with Data* by Cole Nussbaumer Knaflic.

---

## Ch 1: The Importance of Context

### The Who/What/How Framework

Before creating any visualization:

| Question | Details |
|----------|---------|
| **Who** | Your audience — their knowledge level, relationship to you, motivations, potential resistance |
| **What** | The action you want them to take — be specific (approve budget, change process, investigate further) |
| **How** | The delivery mechanism — live presentation, printed report, email, interactive dashboard |

### Exploratory vs. Explanatory Analysis

| Type | Purpose | Audience | Analogy |
|------|---------|----------|---------|
| **Exploratory** | Find insights in data | Yourself/team | Hunting for pearls in oysters |
| **Explanatory** | Communicate a specific insight | Decision-makers | Presenting the pearl on a necklace |

Most data visualization effort should go to explanatory — you've already done the exploring.

### The 3-Minute Story
Distill your entire analysis into what someone would tell a colleague in 3 minutes at the coffee machine. If you can't do this, your message isn't focused enough.

### The Big Idea
A single sentence that:
1. Articulates your unique point of view
2. Conveys what's at stake (why should they care?)
3. Is a complete sentence (not a topic or category)

**Template**: "[Observation about the data] — [what the audience should do about it]"

**Example**: "Customer churn increased 15% in Q3 driven by pricing complaints — we should pilot a loyalty discount for at-risk segments before Q4."

### Storyboarding
- Use sticky notes or paper before opening any tool
- One idea per sticky note
- Arrange, rearrange, discard until the narrative flows
- This prevents wasted effort building the wrong charts

---

## Ch 2: Choosing an Effective Visual

### Chart Type Decision Guide

#### Simple Text
- **Use when**: 1–2 numbers are the entire message
- **How**: Display the number prominently with brief context
- **Example**: "25% increase" in large font with "vs. prior year" as subtitle
- **Avoid**: Putting a single number in a chart (pie chart showing 25% vs 75%)

#### Tables
- **Use when**: Audience needs to look up specific values; mixed units; precise comparison
- **How**: Light or no borders; left-align text, right-align numbers; use heatmap coloring for patterns
- **Enhance**: Heatmap shading (color intensity) to make tables visual
- **Avoid**: Using tables in live presentations (too slow to process)

#### Line Charts
- **Use when**: Showing change over continuous time (months, quarters, years)
- **How**: Time on x-axis; one or multiple series; label directly (not in legend)
- **Rules**: Don't have to start at zero; can use different scales for multiple charts (but NOT dual y-axis)
- **Avoid**: More than 4–5 series (gets cluttered); connecting categorical data with lines

#### Slopegraphs
- **Use when**: Comparing values or ranks at exactly 2 time points
- **How**: Two vertical axes; lines connecting each item's values; label at both ends
- **Shows**: Direction of change, magnitude, and rank shifts simultaneously
- **Avoid**: More than 2 time points; too many items (>10–15)

#### Bar Charts (Vertical)
- **Use when**: Categorical comparison; time series with discrete periods
- **How**: Categories on x-axis; values on y-axis
- **Rules**: MUST start at zero; consistent bar width; space ≈ half bar width
- **Avoid**: More than ~12 bars; long category labels (use horizontal instead)

#### Bar Charts (Horizontal)
- **Use when**: Long category labels; many categories; ranking
- **How**: Categories on y-axis; values on x-axis; order by value (descending, top to bottom)
- **Rules**: MUST start at zero; single color or strategic color highlighting
- **Best practice**: Default to horizontal bars — they're almost always more readable than vertical

#### Stacked Bar Charts
- **Use when**: Showing composition (parts of a whole) across categories
- **How**: Segments stacked; consistent ordering of segments
- **Limitation**: Only the bottom segment has a common baseline; other segments are hard to compare
- **Alternative**: Consider multiple small bar charts or a 100% stacked bar for proportions only

#### Waterfall Charts
- **Use when**: Showing how components add/subtract to reach a total
- **How**: Starting value → incremental additions/subtractions → final total
- **Example**: Revenue → costs → profit; beginning balance → changes → ending balance

#### Scatterplots
- **Use when**: Showing relationship between 2 quantitative variables
- **How**: One variable per axis; each data point is a dot
- **Enhance**: Add trend line, color-code by category, size by third variable (bubble chart)
- **Avoid**: Too many points without visual grouping; missing axis labels

### Charts to AVOID

| Chart Type | Problem | Better Alternative |
|------------|---------|-------------------|
| **Pie chart** | Humans can't accurately compare angles/areas | Horizontal bar chart |
| **Donut chart** | Same as pie, plus hollow center wastes space | Horizontal bar chart |
| **3D chart** | Distorts perception; adds no information | 2D version of the same chart |
| **Secondary y-axis** | Readers can't tell which axis applies to which data | Two separate charts |
| **Area chart** | Filled area rarely adds meaning; can obscure data | Line chart (unless volume matters) |

---

## Ch 3: Clutter is Your Enemy

### Cognitive Load
Every element on a chart consumes processing power. The goal is to minimize extraneous cognitive load so the audience can focus on the message.

### Gestalt Principles of Visual Perception

| Principle | Definition | Application in Data Viz |
|-----------|-----------|------------------------|
| **Proximity** | Items near each other appear grouped | Space related data points closer; separate unrelated groups |
| **Similarity** | Items that look alike appear related | Use same color for same category; same shape for same type |
| **Enclosure** | Items within a boundary appear grouped | Use light background shading to group related chart areas |
| **Closure** | Mind fills in gaps to complete shapes | You don't need full borders; partial borders/gridlines suffice |
| **Continuity** | Eyes follow smooth lines/paths | Align elements; use consistent axis progression |
| **Connection** | Physically connected items appear related | Lines connecting data points (line chart); connecting annotations |

### Elements to Eliminate or Reduce

| Element | Action |
|---------|--------|
| Chart border/outline | Remove entirely |
| Gridlines | Remove or make very light grey (e.g., `#E0E0E0`) |
| Data markers on lines | Remove (unless sparse data) |
| Axis tick marks | Remove or minimize |
| Axis lines | Keep only if needed; often gridlines or data placement suffices |
| Bold axis labels | Reduce to regular weight |
| Legend | Replace with direct labels on data |
| Redundant axis title | Remove if axis labels are self-explanatory |
| Background color | Use white or very light neutral |
| Decimal precision | Round to meaningful precision (2 decimals rarely needed) |

### Data-Ink Ratio
Coined by Edward Tufte: the proportion of a graphic's ink devoted to displaying data vs. non-data elements. Maximize this ratio by removing non-data ink.

### White Space
- Not "empty" — it's strategic
- Creates visual breathing room
- Signals grouping through proximity
- Resist the urge to fill every pixel

---

## Ch 4: Focus Your Audience's Attention

### Memory Types in Data Viz

| Type | Duration | Capacity | Relevance |
|------|----------|----------|-----------|
| **Iconic memory** | <1 second | Large | Preattentive attributes are processed here |
| **Short-term memory** | ~30 seconds | 3–7 items | Limit chart elements to what fits in working memory |
| **Long-term memory** | Indefinite | Huge | Leverage schemas/patterns audience already knows |

### Preattentive Attributes Catalog

Attributes processed by the visual system in <500 milliseconds, before conscious attention:

**For text emphasis**:
| Attribute | How to Apply |
|-----------|-------------|
| **Bold** | Key words, takeaway text, important labels |
| **Italic** | Secondary emphasis, annotations, source notes |
| **UPPERCASE** | Short labels only (hard to read in long strings) |
| **Size** | Larger for headlines/key numbers; smaller for supporting text |
| **Color** | Single accent color on key text against grey/black body |

**For data emphasis**:
| Attribute | How to Apply |
|-----------|-------------|
| **Color/hue** | Highlight 1 series/bar in color; grey out the rest |
| **Intensity/saturation** | Brighter = more attention; muted = background |
| **Size** | Larger data markers, thicker lines for emphasis |
| **Enclosure** | Box, circle, or shaded region around key area |
| **Position** | First position (top of bar chart, leftmost) gets most attention |
| **Line width** | Thicker line for key series; thinner for context series |
| **Added marks** | Arrows, reference lines, callout boxes |

### Color Strategy

**The Grey-First Approach**:
1. Start with everything in grey
2. Identify the ONE thing you want the audience to see
3. Apply color ONLY to that element
4. Use a single accent color (or at most 2)

**Color rules**:
- Grey is your default — not a boring choice, a strategic one
- Brand colors: use sparingly as accents, not for every data series
- Warm colors (red, orange) advance; cool colors (blue, green) recede
- Never use color as the only means of conveying information
- Consistent meaning: once blue = "our product", keep it blue everywhere

### The "Where Are Your Eyes Drawn?" Test
After creating any visual:
1. Step back (or squint)
2. Where do your eyes go first?
3. Is that the most important element?
4. If not, adjust color, size, or position until it is

---

## Ch 5: Think Like a Designer

### Core Design Principles for Data Viz

| Principle | Application |
|-----------|------------|
| **Affordances** | Clickable things should look clickable; readable things should look readable |
| **Accessibility** | Don't rely on color alone; use labels, patterns, shapes as backup |
| **Aesthetics** | Well-designed visuals are perceived as easier to use and more credible |
| **Form follows function** | Choose design that serves the data; never sacrifice clarity for beauty |

### Text Alignment
- **Left-align** all text by default (including chart titles, axis labels, annotations)
- Center alignment is harder to read for anything beyond 1–2 lines
- Right-align numbers in columns so decimal points line up

### White Space / Negative Space
- Margin around charts: don't let elements touch edges
- Breathing room between chart title and chart body
- Space between legend/annotations and data area
- White space is NOT wasted — it improves comprehension

### Visual Hierarchy in Data Viz
1. **Title/takeaway** — Most prominent (bold, larger, top of chart)
2. **Data** — The actual bars/lines/points (the substance)
3. **Annotations** — Call-outs explaining what to see
4. **Axis labels** — Necessary but quiet
5. **Source/footnotes** — Smallest, least prominent

### Consistency Across a Presentation
- Same color = same meaning on every slide
- Same chart style/formatting throughout
- Same font, same font sizes
- Same axis formatting (if showing similar metrics)
- Consistency reduces cognitive load

---

## Ch 6: Model Visuals — Integration Examples

### Before/After Transformation Process
The book provides detailed worked examples showing the full transformation:

1. **Start with default chart** (Excel/Tableau output with all defaults)
2. **Identify the message** (What is the Big Idea?)
3. **Choose the right chart type** (Is the default appropriate?)
4. **Declutter** (Remove borders, gridlines, markers, legends)
5. **Focus attention** (Grey everything, add color to the story)
6. **Add annotations** (Tell the audience what to see)
7. **Add action title** (Replace generic title with takeaway statement)

### Common Transformations

| From | To | Why |
|------|----|-----|
| Pie chart | Horizontal bar chart | Easier to compare values |
| Cluttered line chart | Clean line chart with 1 highlighted series | Focuses attention on the story |
| Rainbow bar chart | Grey bars with 1 highlighted in color | Draws eye to what matters |
| Generic title ("Sales by Region") | Action title ("Northeast sales declined 18% in Q3") | Tells the audience what to see |
| Legend in corner | Direct labels on data series | Reduces eye travel; faster comprehension |
| Dark/busy background | White/clean background | Reduces clutter; focuses on data |

---

## Ch 7: Lessons in Storytelling

### Three-Act Narrative Structure for Data

| Act | Content | Data Viz Role |
|-----|---------|--------------|
| **Act 1: Setup** | Shared context; what the audience already knows | Background data; baseline metrics; "here's where we are" |
| **Act 2: Conflict** | What changed; the problem or opportunity; tension | Your key charts; the data that reveals the insight |
| **Act 3: Resolution** | What to do about it; the call to action | Recommendation; projected impact; next steps |

### Horizontal Logic
- Read ONLY the slide titles in sequence
- They should tell a complete, compelling story without seeing any chart
- Each title should be an **action statement** (verb + insight), not a **label** (noun phrase)

| Bad Title (Label) | Good Title (Action) |
|-------------------|-------------------|
| "Q3 Revenue" | "Q3 revenue fell 12% as enterprise deals slipped" |
| "Customer Satisfaction" | "Satisfaction scores improved after the June product update" |
| "Regional Breakdown" | "Western region now accounts for 40% of new business" |

### Vertical Logic
Within each slide/page:
- The title states the takeaway
- The chart/data supports that takeaway
- Annotations point to the evidence
- Nothing on the slide contradicts or distracts from the title

### Reverse Storyboarding
After completing a presentation:
1. Extract all slide titles into a list
2. Read them in order
3. Do they tell a coherent, compelling story?
4. If not, restructure

### The "So What?" Test
After presenting any data point or chart, ask: "So what?" The answer should be:
- Stated as an annotation on the chart
- Reflected in the slide title
- Connected to the call to action

### Repetition in Data Storytelling
- State the Big Idea early
- Support it with data in the middle
- Restate it at the end
- Don't be afraid to repeat — audiences need it more than you think

---

## Ch 8: Pulling It All Together

### Complete Workflow Checklist

1. **Context** — Who is my audience? What action do I want? How will I deliver?
2. **Big Idea** — Can I state my message in one sentence?
3. **Storyboard** — Have I planned the narrative flow before building?
4. **Chart type** — Is this the right visual for this data?
5. **Declutter** — Have I removed everything non-essential?
6. **Focus** — Is color used sparingly and strategically?
7. **Design** — Is it aligned, consistent, accessible?
8. **Annotate** — Have I told the audience what to see?
9. **Title** — Does each title state a takeaway, not a label?
10. **Story** — Does the horizontal logic tell a complete narrative?

---

## Ch 9: Case Studies — Key Patterns

### Transformation Patterns Observed

| Pattern | Technique |
|---------|-----------|
| **Dark to light** | Replace dark/colored backgrounds with white |
| **Rainbow to grey+accent** | Replace multi-color palettes with grey + 1 highlight color |
| **Legend to direct labels** | Remove legend box; label series directly on the chart |
| **Default to decluttered** | Remove borders, gridlines, markers, unnecessary text |
| **Label title to action title** | Replace "Sales by Quarter" with "Sales declined 15% in Q4" |
| **Chart dump to narrative** | Arrange charts in story order with connecting text |
| **Table to visual** | Convert data tables into bar charts or line charts for presentations |

### Annotation Strategies
- **Callout boxes**: Semi-transparent background with text near the relevant data point
- **Arrows**: Point from annotation text to specific data point
- **Reference lines**: Horizontal/vertical lines showing targets, averages, or thresholds
- **Color + text**: Highlighted data point + nearby text explaining significance
- **Progressive reveal**: In presentations, show the chart first, then add annotations (builds)

---

## Ch 10: Final Thoughts

### Practice Framework
- **Practice constantly** — Apply these lessons to every chart you make, even internal ones
- **Seek feedback** — Ask others "where are your eyes drawn?" and "what's the message?"
- **Study great examples** — Collect data visualizations that work and analyze why
- **Iterate** — First drafts are never final; refine through multiple passes
- **Be brave** — Simplifying feels risky ("What if they want more data?") but almost always improves communication
