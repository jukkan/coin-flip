# Power Platform Monitor Coin Flip (Power Automate)

A tiny, connector-free cloud flow that fails ~50% of runs to test **Power Platform Monitor** dashboards and **Monitor Alerts** in PPAC.

## Quick start (2 minutes)
1. Download `CoinFlip_unmanaged.zip` from this repo.
2. In a suitable Power Platform environment, go to **Solutions** → **Import** → pick the zip → **Publish all customizations**.
3. Open flow **Coin Flip – PPAC Monitor test** → **Turn on** (adjust schedule if you want, default is every 3h).
4. In **PPAC → Monitor → Create alert**  
   - Product: **Power Automate**  
   - Product type: **Cloud flow**  
   - Metric: **Success rate**  
   - Operator: **Is Under**  
   - Value: **98** (or lower if you want excitement)

**Expected**: The flow fails ~50% of runs. Monitor charts/alerts are daily-aggregated and can be late or flaky—this flow helps you observe that behavior.

## Change failure rate
Edit the Condition expression threshold (last hex digit of `guid()`):
- 50% (default): even parity check
- 75%: `less(indexOf('0123456789abcdef', substring(toLower(guid()),35,1)), 12)`
- 25%: same but threshold `4`

## But why?
Because the Power Platform Monitor features that Microsoft has rolled out in 2025 don't seem to be reliable enough to "just work". In fact, some of them are less reliable than a coin flip that would give you 50% chances of being right.

Read my article [Who monitors the Power Platform Monitor](https://www.perspectives.plus/p/who-monitors-the-power-platform-monitor) for more details. I've also been sharing updates about [missing telemetry data](https://www.linkedin.com/feed/update/urn:li:activity:7374337699186544640/) and [lack of alerts](https://www.linkedin.com/feed/update/urn:li:activity:7381217782463537152/) on LinkedIn.

---

**Made by Jukka Niiranen / Niiranen Advisory Oy.**  
If these kind of things are interesting to you:
- Subscribe to my newsletter **Perspectives on Power Platform** → [perspectives.plus](https://www.perspectives.plus/)
- Hire me for your **Power Platform advisory** needs → [niiranenadvisory.com](https://niiranenadvisory.com/)
