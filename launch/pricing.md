# ts-cli — Pricing Strategy

## Model: Free (Open Source)

ts-cli is a **free, open-source** tool. This is the right call because:

1. **Market expectation**: CLI developer tools in this space are free. Charging for a timestamp converter would face massive resistance.
2. **Portfolio positioning**: ts-cli is a portfolio piece that demonstrates product-building capability, not a revenue driver.
3. **Low willingness to pay**: The target user (developers) expects this class of tool to be free. The value per use is too low to monetize directly.

## Revenue Path (Future)

While ts-cli itself stays free, potential monetization paths exist:

1. **Pro tier (ts-pro)**: A hypothetical paid version with additional features:
   - Duration math (`ts duration 1718901234 1718902000` → `12m 46s`)
   - Cron expression parsing (`ts cron "0 * * * *"` → next 5 runs)
   - Relative time (`ts "2 hours ago"` → epoch)
   - JSON output mode for scripting
   - Config file for default timezone/format
   - Price: $2-5 one-time or $1/mo

2. **Devtools bundle**: Bundle ts-cli with other micro-CLI tools (env-diff, etc.) into a paid "developer toolkit" collection.

3. **Sponsorship**: GitHub Sponsors / Open Collective for ongoing maintenance.

## Recommendation

**Launch as free.** Revisit monetization only if:
- User base grows to 10k+ PyPI downloads/month
- Clear demand for pro features emerges
- Bundle opportunity materializes with 3+ tools

For now: ship it free, collect users, build reputation.
