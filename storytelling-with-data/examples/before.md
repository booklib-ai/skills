# Before

A pie chart specification used to compare customer support ticket volume across seven categories over three time periods — a chart type that cannot support this data relationship.

```
CHART SPECIFICATION: Support Ticket Distribution

Chart type: Pie chart (3D, with exploded slices)
Title: "Support Ticket Breakdown"

Data: Ticket counts by category for Q1, Q2, Q3 2024
  Shown as: Three separate 3D pie charts side by side

Categories (7 slices per pie):
  - Billing Issues
  - Login / Account Access
  - Product Bugs
  - Feature Requests
  - Shipping & Delivery
  - Refunds & Returns
  - Other

Visual choices:
  - Each category gets a distinct color from a rainbow palette
  - All 7 slices are shown even when <2% share
  - Percentages shown inside each slice (8px font)
  - Legend placed below each chart
  - 3D perspective tilt applied for "visual interest"
  - No annotations or callouts

Goal: Show the trend in which ticket types are growing and which are shrinking
      across Q1 → Q2 → Q3, and highlight that Product Bugs doubled in Q3.
```
