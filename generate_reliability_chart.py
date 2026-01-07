"""
Generate Power Platform Monitor Reliability Chart

This script creates a visualization of Power Platform Monitor alert reliability
based on collected data. The output is a 16:9 PNG image suitable for sharing
on social media platforms like LinkedIn and Twitter.

Usage: python generate_reliability_chart.py
Output: 142_days_monitor_reliability.png
"""

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.patches as patches

# --- 1. CONFIGURATION ---
start_date = "2025-08-19"
end_date = "2026-01-07"

# Dates when alerts were actually received
received_dates_str = [
    "2026-01-06", "2026-01-05", "2026-01-04", "2026-01-03", "2026-01-02", "2026-01-01",
    "2025-12-31", "2025-12-30", "2025-12-29", "2025-12-28", "2025-12-26", "2025-12-24",
    "2025-12-23", "2025-12-22", "2025-12-21", "2025-12-20", "2025-12-15", "2025-12-12",
    "2025-12-04", "2025-12-02", "2025-11-30", "2025-11-28", "2025-11-24", "2025-11-19",
    "2025-11-18", "2025-11-16", "2025-11-13", "2025-11-12", "2025-11-11", "2025-11-09",
    "2025-10-31", "2025-10-14", "2025-10-13", "2025-10-03", "2025-10-02", "2025-10-01",
    "2025-09-30", "2025-08-26", "2025-08-25", "2025-08-23", "2025-08-19"
]

# --- 2. DATA PREP ---
full_range = pd.date_range(start=start_date, end=end_date)
received_dates = pd.to_datetime(received_dates_str)
total_days = len(full_range)
actual_days = len(received_dates)
reliability = (actual_days / total_days) * 100
missed_days = total_days - actual_days

# --- 3. PLOT SETUP (16:9 Aspect Ratio) ---
fig, ax = plt.subplots(figsize=(12, 6.75), dpi=150)
fig.patch.set_facecolor('#f8f9fa')  # Light grey bg
ax.set_facecolor('#f8f9fa')

# --- 4. DRAWING ---
# Timeline base
ax.hlines(y=0, xmin=full_range[0], xmax=full_range[-1], color='#e9ecef', linewidth=25, zorder=1)
# Success Hits (Power Platform Purple)
ax.vlines(x=received_dates, ymin=-0.45, ymax=0.45, color='#742774', linewidth=2, label='Alert Received', zorder=2)

# Highlight: Silent Failure Gap (Sep)
gap_start = pd.Timestamp("2025-08-27")
gap_end = pd.Timestamp("2025-09-29")
rect = patches.Rectangle((mdates.date2num(gap_start), -0.6),
                         mdates.date2num(gap_end) - mdates.date2num(gap_start),
                         1.2, linewidth=0, facecolor='#dc3545', alpha=0.1, zorder=0)
ax.add_patch(rect)
ax.text(pd.Timestamp("2025-09-12"), 0.7, "Silent Failure\n(34 Days)", color='#dc3545', ha='center', fontsize=9, fontweight='bold')

# --- 5. TEXT LABELS ---
# Header
ax.text(0.0, 1.35, "Power Platform Monitor Reliability", transform=ax.transAxes, fontsize=22, fontweight='bold', color='#212529')
ax.text(0.0, 1.25, f"Daily Alert Check: Aug 19, 2025 - Jan 07, 2026 ({total_days} days)", transform=ax.transAxes, fontsize=12, color='#6c757d')

# Key Stats
ax.text(0.0, 1.05, f"{reliability:.1f}%", transform=ax.transAxes, fontsize=26, fontweight='bold', color='#742774')
ax.text(0.0, 0.96, "Success Rate", transform=ax.transAxes, fontsize=10, color='#6c757d')

ax.text(0.25, 1.05, f"{missed_days}", transform=ax.transAxes, fontsize=26, fontweight='bold', color='#dc3545')
ax.text(0.25, 0.96, "Missed Alerts", transform=ax.transAxes, fontsize=10, color='#6c757d')

ax.text(0.5, 1.05, "34 Days", transform=ax.transAxes, fontsize=26, fontweight='bold', color='#343a40')
ax.text(0.5, 0.96, "Longest Gap", transform=ax.transAxes, fontsize=10, color='#6c757d')

# --- 6. CLEANUP ---
ax.set_ylim(-1, 2)
ax.set_xlim(pd.Timestamp(start_date) - pd.Timedelta(days=5), pd.Timestamp(end_date) + pd.Timedelta(days=5))
ax.get_yaxis().set_visible(False)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color('#adb5bd')

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(fontsize=10, color='#495057')

plt.tight_layout()

# --- 7. SAVE OUTPUT ---
output_file = "142_days_monitor_reliability.png"
plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='#f8f9fa', edgecolor='none')
print(f"Chart saved to: {output_file}")
print(f"Stats: {reliability:.1f}% success rate, {missed_days} missed alerts out of {total_days} days")
