# After

An MVP experiment document that identifies the riskiest assumption, defines the smallest test, specifies actionable metrics, and sets explicit pivot/persevere criteria before any code is written.

```markdown
## MVP Experiment: AI Expense Management — Concierge Test

### The Big Idea
SMB finance managers spend 3+ hours per week manually reconciling receipts.
We believe they will pay for a tool that eliminates that work — but we have
not yet validated that they will change their workflow to use it.

### Leap-of-Faith Assumptions to Test

**Value hypothesis (riskiest):**
> "Finance managers at 10–50 person companies will submit receipts through
> a new tool at least 3× per week if the categorisation is accurate."

**Growth hypothesis (secondary):**
> "Satisfied users will refer at least one colleague within 30 days."

### Why NOT build the full product yet
Building OCR + AI categorisation + ERP integrations takes 6 months and $400K.
If users don't form the habit of submitting receipts, none of those features
matter. We must validate the value hypothesis first.

### MVP Design: Concierge (Manual Behind the Scenes)

**What users experience:**
- Sign up form → they receive a dedicated WhatsApp number
- They photograph receipts and send to WhatsApp
- We manually categorise and respond with a structured summary within 2 hours
- Weekly: we email a formatted expense report (manually compiled in Google Sheets)

**What we actually build:**
- Landing page with sign-up form (1 day)
- WhatsApp Business number (1 hour)
- Google Sheets report template (2 hours)
- Total build time: ~2 days

**Participants:** 15 finance managers recruited from our network

**Duration:** 6 weeks

### Innovation Accounting — Metrics

| Metric | Baseline | Target (persevere) | Source |
|--------|----------|--------------------|--------|
| Weekly receipt submission rate | 0 | ≥ 3 receipts/user/week by week 4 | WhatsApp logs |
| Categorisation acceptance rate | — | ≥ 85% accepted without correction | User replies |
| User retention (still active week 6) | — | ≥ 70% of participants | WhatsApp logs |
| Referral rate | 0 | ≥ 1 referral per 5 users | Sign-up source field |
| Willingness to pay | 0 | ≥ 60% say "yes" at $29/mo | End-of-pilot survey |

**Vanity metrics we will NOT track:** total sign-ups, page views, social shares.

### Pivot/Persevere Decision — Week 6 Review

**Persevere** (move to automated MVP) if ALL of:
- Submission rate ≥ 3/week by week 4
- Retention ≥ 70% at week 6
- Willingness to pay ≥ 60%

**Pivot** (reconsider problem or segment) if ANY of:
- Submission rate < 1/week by week 3 (habit not forming)
- Retention < 40% at week 4 (users not finding value)

**Pivot options to consider:**
- Zoom-in: focus only on one vertical (e.g., restaurant industry) where receipt volume is higher
- Customer segment: target bookkeepers who file for multiple clients, not the SMB themselves
- Problem: pivot to approval workflows if users engage more with that step than receipt capture
```

Key improvements:
- Leap-of-faith assumptions are named explicitly before any engineering begins — value hypothesis and growth hypothesis are the riskiest bets, not product features (Ch 5: Leap-of-faith assumptions)
- Concierge MVP — two days of manual work — tests the core habit loop without six months of engineering (Ch 6: MVP is for learning, not launching)
- Innovation accounting table defines baseline, target, and data source for each metric before the experiment runs (Ch 7: Innovation accounting)
- All metrics are cohort-based and behavioural ("submission rate", "retention") — vanity metrics like total sign-ups are explicitly excluded (Ch 7: Actionable vs. vanity metrics)
- Explicit pivot/persevere decision criteria with a named decision date eliminate gut-feel delays (Ch 8: Pivot or persevere)
- Pivot catalog is pre-populated — the team has thought through options in advance rather than scrambling at the decision point (Ch 8: Pivot types)
