# LAUNCH-PLAN: ts-cli

**Product:** ts-cli — Zero-dependency CLI timestamp converter
**Slug:** ts-cli
**Date:** 2026-06-20
**QA Status:** PASS — 40/40 tests, 12/12 smoke tests

---

## Launch Channels (Priority Order)

### 1. PyPI (Primary Distribution)
- **What:** Publish `ts-cli` package to PyPI for `pip install ts-cli`
- **Why:** This is the primary install method Python developers expect
- **Status:** pyproject.toml ready, NOT yet published
- **Human action required:** Yes — PyPI publish (see escalation)

### 2. GitHub Repository
- **What:** Public repo with README, install instructions, and source
- **Why:** Source of truth, issue tracking, curl install source
- **Status:** Code exists locally, repo may not be public yet
- **Human action required:** Yes — verify/create GitHub repo (see escalation)

### 3. Reddit — r/Python, r/commandline, r/devops
- **What:** Show HN-style post: "I built a zero-dependency CLI for timestamp conversion"
- **Why:** High-traffic subreddits with exact target audience
- **Status:** Post not created
- **Human action required:** Yes — create Reddit accounts/posts (see escalation)

### 4. Hacker News — Show HN
- **What:** "Show HN: ts — A zero-dependency CLI timestamp converter"
- **Why:** Massive developer audience, potential for viral pickup
- **Status:** Post not created
- **Human action required:** Yes — HN account + post (see escalation)

### 5. Twitter/X
- **What:** Thread or single tweet announcing the tool with usage examples
- **Why:** Developer community on Twitter, good for discoverability
- **Status:** Not posted
- **Human action required:** Yes — Twitter account + post (see escalation)

### 6. Product Hunt
- **What:** Product Hunt listing for ts-cli
- **Why:** Launch-day visibility, early adopters
- **Status:** Not listed
- **Human action required:** Yes — PH account + listing (see escalation)

### 7. Dev.to / Hashnode
- **What:** Short blog post: "I built ts — a zero-dependency timestamp converter"
- **Why:** Long-form content, SEO, developer audience
- **Status:** Not written
- **Human action required:** Yes — write + publish post (see escalation)

---

## First-Week Launch Timeline

### Day 1 (Launch Day) — "Ship It"
1. **Publish to PyPI** — `twine upload dist/*` (human)
2. **Verify GitHub repo is public** with README, MIT license, install instructions (human)
3. **Post to Hacker News** — "Show HN: ts — zero-dependency CLI timestamp converter" (human)
4. **Post to Reddit** — r/Python, r/commandline (human)
5. **Tweet announcement** with usage examples (human)

### Day 2 — "Amplify"
1. **Post to r/devops** (human)
2. **Submit to Product Hunt** (human)
3. **Engage with comments** on HN, Reddit, Twitter (human)
4. **Monitor PyPI download stats** (human)

### Day 3 — "Content"
1. **Write Dev.to/Hashnode blog post** — "Why I built a timestamp converter CLI" (human)
2. **Cross-link** blog post from Reddit, Twitter (human)
3. **Monitor GitHub stars/issues** (human)

### Day 4-5 — "Community"
1. **Post in relevant Discord/Slack communities** (Python, DevOps) (human)
2. **Share in Indie Hackers** if applicable (human)
3. **Respond to all feedback** (human)

### Day 6-7 — "Measure & Iterate"
1. **Check PyPI download count** (human)
2. **Review GitHub stars, issues, PRs** (human)
3. **Note feature requests** for v2 roadmap (human)
4. **Decide on follow-up** — maintain, expand, or move to next product (human)

---

## Exact Human Actions Required

All publishing actions are gated behind human approval. See full escalation checklist at:
`~/hermes_ops/escalations/ts-cli.md`

### Summary of Human Actions:

| # | Action | Platform | Priority |
|---|--------|----------|----------|
| 1 | Create PyPI account (if needed) + publish `ts-cli` | PyPI | CRITICAL |
| 2 | Create/verify GitHub repo `ericjoye/ts-cli` is public | GitHub | CRITICAL |
| 3 | Build sdist/wheel: `python -m build` locally | Local | CRITICAL |
| 4 | Post "Show HN" on Hacker News | HN | HIGH |
| 5 | Post on r/Python and r/commandline | Reddit | HIGH |
| 6 | Tweet announcement with examples | Twitter/X | MEDIUM |
| 7 | Submit to Product Hunt | Product Hunt | MEDIUM |
| 8 | Write Dev.to/Hashnode blog post | Dev.to | MEDIUM |
| 9 | Share in Discord/Slack dev communities | Various | LOW |
| 10 | Monitor stats and respond to feedback | All | ONGOING |

---

## Success Metrics (First 30 Days)

- **PyPI downloads:** 500+ (good), 2000+ (great)
- **GitHub stars:** 50+ (good), 200+ (great)
- **Hacker News upvotes:** 20+ (good), 100+ (great)
- **Reddit upvotes:** 50+ combined (good)
- **Issues/PRs:** Any community contributions = success
- **Blog post views:** 1000+ (good)

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Low visibility on HN/Reddit | Post at peak hours (US morning), engage in comments |
| PyPI name `ts-cli` taken | Already verified available (pyproject.toml ready) |
| Negative feedback on simplicity | Emphasize "zero-dependency, single file" as feature |
| No traction | This is a portfolio piece — learn and move to next product |

---

## Notes

- ts-cli is **free and open source** — no paid tier at launch
- All launch channels are developer-focused (no consumer marketing)
- The goal is **portfolio credibility + user base**, not revenue
- Revisit monetization only at 10k+ downloads/month or clear pro-feature demand
