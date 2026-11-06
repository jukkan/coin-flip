"""
Generate Power Platform Monitor Reliability Chart

Reads the days on which a Monitor alert email arrived (alert_days.csv) and draws a
16:9 timeline suitable for sharing on LinkedIn and similar platforms.

Each date in alert_days.csv is the evaluated day printed in the alert email body
("Timestamp"), not the day the email was received.

Usage: python generate_reliability_chart.py
Output: <N>_days_monitor_reliability.png

The earlier 142-day chart (Aug 19, 2025 - Jan 7, 2026) is kept as
generate_reliability_chart_142_days.py.
"""

import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.patches as patches

# --- 1. CONFIGURATION ---
# The flow was created on Sep 29, 2025; earlier results are historical only.
start_date = "2025-09-29"
end_date = "2026-11-05"

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "alert_days.csv"), newline="") as f:
    received_dates_str = [row["alert_day"] for row in csv.DictReader(f)]

# --- 2. DATA PREP ---
full_range = pd.date_range(start=start_date, end=end_date)
received_dates = pd.to_datetime(received_dates_str)
received_dates = received_dates[(received_dates >= full_range[0]) & (received_dates <= full_range[-1])]
total_days = len(full_range)
actual_days = len(received_dates)
reliability = (actual_days / total_days) * 100
missed_days = total_days - actual_days

# Longest run of days without an alert
received_set = set(received_dates)
longest = (0, None, None)
run_start, run_len = None, 0
for day in full_range:
    if day in received_set:
        run_start, run_len = None, 0
    else:
        if run_start is None:
            run_start = day
        run_len += 1
        if run_len > longest[0]:
            longest = (run_len, run_start, day)
gap_len, gap_start, gap_end = longest

# Success rate in the latest calendar year of data
latest_year = full_range[-1].year
year_range = full_range[full_range.year == latest_year]
year_hits = sum(1 for d in year_range if d in received_set)
year_rate = year_hits / len(year_range) * 100

# --- 3. PLOT SETUP (16:9 Aspect Ratio) ---
fig, ax = plt.subplots(figsize=(12, 6.75), dpi=150)
fig.patch.set_facecolor('#f8f9fa')
ax.set_facecolor('#f8f9fa')

# --- 4. DRAWING ---
ax.hlines(y=0, xmin=full_range[0], xmax=full_range[-1], color='#e9ecef', linewidth=25, zorder=1)
ax.vlines(x=received_dates, ymin=-0.45, ymax=0.45, color='#742774', linewidth=1.2, label='Alert Received', zorder=2)

# Highlight the longest silent gap
rect = patches.Rectangle((mdates.date2num(gap_start), -0.6),
                         mdates.date2num(gap_end) - mdates.date2num(gap_start) + 1,
                         1.2, linewidth=0, facecolor='#dc3545', alpha=0.1, zorder=0)
ax.add_patch(rect)
gap_mid = gap_start + (gap_end - gap_start) / 2
ax.text(gap_mid, 0.7, f"Longest gap\n({gap_len} days)", color='#dc3545', ha='center', fontsize=9, fontweight='bold')

# --- 5. TEXT LABELS ---
first_label = full_range[0].strftime('%b %d, %Y').replace(' 0', ' ')
last_label = full_range[-1].strftime('%b %d, %Y').replace(' 0', ' ')
ax.text(0.0, 1.35, "Power Platform Monitor Reliability", transform=ax.transAxes, fontsize=22, fontweight='bold', color='#212529')
ax.text(0.0, 1.25, f"Daily Alert Check: {first_label} - {last_label} ({total_days} days)", transform=ax.transAxes, fontsize=12, color='#6c757d')

ax.text(0.0, 1.05, f"{reliability:.1f}%", transform=ax.transAxes, fontsize=26, fontweight='bold', color='#742774')
ax.text(0.0, 0.96, "Days with an alert", transform=ax.transAxes, fontsize=10, color='#6c757d')

ax.text(0.25, 1.05, f"{missed_days}", transform=ax.transAxes, fontsize=26, fontweight='bold', color='#dc3545')
ax.text(0.25, 0.96, "Days without an alert", transform=ax.transAxes, fontsize=10, color='#6c757d')

ax.text(0.5, 1.05, f"{gap_len} Days", transform=ax.transAxes, fontsize=26, fontweight='bold', color='#343a40')
ax.text(0.5, 0.96, "Longest gap", transform=ax.transAxes, fontsize=10, color='#6c757d')

ax.text(0.75, 1.05, f"{year_rate:.0f}%", transform=ax.transAxes, fontsize=26, fontweight='bold', color='#2b8a3e')
ax.text(0.75, 0.96, f"Days with an alert in {latest_year}", transform=ax.transAxes, fontsize=10, color='#6c757d')

# --- 6. CLEANUP ---
ax.set_ylim(-1, 2)
ax.set_xlim(pd.Timestamp(start_date) - pd.Timedelta(days=5), pd.Timestamp(end_date) + pd.Timedelta(days=5))
ax.get_yaxis().set_visible(False)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color('#adb5bd')

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(fontsize=10, color='#495057')

plt.tight_layout()

# --- 7. SAVE OUTPUT ---
output_file = os.path.join(HERE, f"{total_days}_days_monitor_reliability.png")
plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='#f8f9fa', edgecolor='none')
print(f"Chart saved to: {output_file}")
print(f"Stats: {reliability:.1f}% of days with an alert, {missed_days} days without, longest gap {gap_len} days "
      f"({gap_start.date()} to {gap_end.date()}), {latest_year}: {year_rate:.1f}%")
