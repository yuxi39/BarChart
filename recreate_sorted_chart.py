# -*- coding: utf-8 -*-
"""
Recreate the horizontal bar chart sorted descending (largest at top) and export PNG + PPTX.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys, os, logging
import numpy as np

print('DEBUG: script started, cwd=', os.getcwd())
sys.stdout.flush()
logging.basicConfig(level=logging.DEBUG)
logging.debug('debug logging enabled')
# Save outputs into repository root outputs folder (use cwd to avoid PATH oddities)
OUTPUT_DIR = Path.cwd() / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
print(f"Using OUTPUT_DIR: {OUTPUT_DIR}")

# Data extracted from the provided image (values in 万元)
data = {
    "李艳华": 8638.0,
    "郑群": 2418.3,
    "胡军可": 2397.3,
    "谷大鹏": 1163.2,
    "梁晨+靳宗齐": 504.8,
    "钟征华": 35.1,
}

# Sort descending by value
items = sorted(data.items(), key=lambda x: x[1], reverse=False)
names = [n for n, v in items]
values = [v for n, v in items]

# Use Agg backend for headless environments and configure fonts
mpl.use('Agg')
mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial"]
mpl.rcParams["axes.unicode_minus"] = False

# Ensure outputs directory is explicit absolute path to repo root
OUTPUT_DIR = Path('d:/moqt-project/outputs')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
print(f"Using OUTPUT_DIR: {OUTPUT_DIR}")

# Colors matching the manual chart palette
colors = ["#89c0ff", "#ffb3e6", "#ffd88a", "#c7e9d7", "#78cfe0", "#7fe6d0"]


def strip_trailing_zero(v: float) -> str:
    s = f"{v:.1f}"
    if s.endswith('.0'):
        return s[:-2]
    return s

# Start fresh figure and avoid leftover axes (which can show 0-1 normalized axes)
plt.close('all')
fig = plt.figure(figsize=(16, 5.5))  # width, height in inches
fig.patch.set_facecolor('white')
# use a wider plotting area to match the green-frame layout in outputs/chart_given_large.svg

# we'll create and use our own axes below (so there's no stray 0-1 axes)

# Grid/style will be applied on the created axes


# Header background (drawn by figure rectangle)
# (we already set figure background above)

# New axes for chart area — expanded to match the larger blue-frame layout
# Make the plotting area a bit lower so the top bar has space from the header background
ax = fig.add_axes([0.07, 0.06, 0.88, 0.76])  # left, bottom, width, height (lowered and slightly shorter)

# Vertical grid lines (linear axis)
max_val = max(values)
# Choose a 'nice' integer tick base by rounding DOWN to the nearest power-of-ten multiple
# e.g., 8400 -> 8000, 432 -> 400
mag = 10 ** int(np.floor(np.log10(max_val))) if max_val > 0 else 1
tick_base = int((max_val // mag) * mag)
if tick_base == 0:
    tick_base = int(mag)
# original x ticks (in original units) — evenly spaced between 0 and tick_base (integers)
x_ticks_orig = [int(round(t)) for t in np.linspace(0, tick_base, 5)]
# Ensure ticks are unique and sorted (in case of small values)
x_ticks_orig = sorted(list(dict.fromkeys(x_ticks_orig)))
# We'll draw gridlines after bar_start_base is known so they align with the bars
# Note: removed the thin vertical separator between labels and bars per request (the "yellow" line)
# We'll draw a custom bottom axis line after setting y-limits so its y coordinate is correct
bottom_axis_y = None

# Draw rounded bars using patches
import matplotlib.patches as patches
bar_height = 0.6
ys = list(range(len(names)))
# use linear units for positioning label column and bars so axis is linear
# move the labels and bars to the right to leave a clean left margin (increase left whitespace)
label_col_x = -max_val*0.15  # shifted right slightly to increase left margin
# base bar start (a little gap from the label column so bars don't touch the text)
bar_start_base = label_col_x + max_val*0.06
for i, (name, v) in enumerate(items):
    y = ys[i]
    # use linear width (original units)
    bar_w = v
    color = colors[i % len(colors)]
    bar_start = bar_start_base
    # rectangle with rounded corners
    rect = patches.FancyBboxPatch((bar_start, y - bar_height/2), bar_w, bar_height,
                                  boxstyle="round,pad=0.02,rounding_size=6",
                                  linewidth=0, facecolor=color, edgecolor=color)
    ax.add_patch(rect)
    # label column: placed on the left, right-aligned so labels hug the left edge
    # shift the name labels slightly right without moving the bars
    label_text_x = label_col_x + max_val*0.03
    ax.text(label_text_x, y, name, ha='right', va='center', fontsize=16, fontfamily='Microsoft YaHei', clip_on=False)
    # value label: place outside on the right, bold, no unit (show original value)
    val_str = strip_trailing_zero(v)
    val_x = bar_start + bar_w + max_val*0.02
    ax.text(val_x, y, val_str, ha='left', va='center', fontsize=14, color='#222', fontweight='bold', clip_on=False)

# now that bar_start_base is known, shift tick/grid positions so the axis starts at the bar start
tick_positions_shifted = [bar_start_base + t for t in x_ticks_orig]
for xtp in tick_positions_shifted:
    ax.axvline(xtp, color='#e6e6e6', linestyle='--', linewidth=1)

# Adjust axes limits and ticks
# header y position (used to align axis end with header label)
header_y = 0.94
# compute axis start so it includes the label column and compute axis end so bars fit
# start from label_col_x with a small left padding so text labels are fully visible
start_data = label_col_x - max_val*0.02
right_fig_x = 0.965
try:
    disp = fig.transFigure.transform((right_fig_x - 0.02, header_y))
    mapped_end = ax.transData.inverted().transform(disp)[0]
    # ensure the axis end allows the largest bar (max_val) to be fully visible
    desired_end = max(mapped_end, bar_start_base + max_val * 1.03)
    end_data = desired_end
except Exception:
    end_data = bar_start_base + max_val * 1.12

# set x limits to include start and end comfortably (linear units)
ax.set_xlim(start_data, max(end_data, max_val) + max_val*0.03)
# lower the top plotted limit so the top bar moves down a bit, leaving space from header
ax.set_ylim(-0.5, len(names)-0.8)
ax.set_yticks([])
# show numeric x ticks (display labels in original units positioned at shifted coordinates)
ax.set_xticks(tick_positions_shifted)
ax.set_xticklabels([f"{int(t):,}" for t in x_ticks_orig], fontsize=14, color='#555')
ax.tick_params(axis='x', which='major', labelsize=14, colors='#555')
# removed the small left-column header label (user requested to delete it)
# draw a prominent bottom horizontal axis line from the label-left to the right header position
bottom_axis_y = ax.get_ylim()[0] - 0.06
ax.hlines(bottom_axis_y, start_data, end_data, colors='#666', linewidth=2, zorder=3)
# make bottom spine invisible since we draw our custom axis
ax.spines['bottom'].set_visible(False)
try:
    # and keep the appearance of a rounded end if available
    ax.spines['bottom'].set_solid_capstyle('round')
except Exception:
    pass

# Total box and standardized header placement
total = sum(values)
header_y = 0.94
# dark header background
fig.patches.extend([patches.Rectangle((0, header_y - 0.06), 1, 0.12, transform=fig.transFigure, facecolor='#1f3b4d', zorder=0)])
# left: total box (rounded) — use the same dark header style as the right header and increase visibility
fig.text(0.03, header_y, f"总回款金额：{total:.1f}万元", fontsize=13, color='white', bbox=dict(boxstyle="round,pad=0.35", facecolor='#1f3b4d', edgecolor='#1f3b4d'), ha='left', va='center')
# center: title
fig.text(0.5, header_y, '各业务员回款金额对比分析', ha='center', va='center', fontsize=26, color='white', fontweight='bold')
# right: small right-aligned label, visually consistent with left total box
fig.text(0.965, header_y, '回款金额（万元）', ha='right', va='center', fontsize=14, color='white', bbox=dict(boxstyle='round,pad=0.22', facecolor='#1f3b4d', edgecolor='#1f3b4d'))

# remove top/right/left spines but keep bottom for numeric ticks
for spine in ['top','right','left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#666')

# Set tight layout (tighten margins to match the larger blue-frame feel)
plt.subplots_adjust(left=0.11, right=0.99, top=0.94, bottom=0.04)
# Styling improvements to match manual design
plt.tight_layout(rect=(0,0,1,0.96))

# Save high-resolution PNG
png_path = OUTPUT_DIR / "chart_sorted.png"
plt.savefig(png_path, dpi=300)
print(f"Wrote PNG: {png_path}")

# Also save an SVG for lossless vector output
svg_path = OUTPUT_DIR / "chart_sorted.svg"
plt.savefig(svg_path, format='svg')
print(f"Wrote SVG: {svg_path}")

plt.close(fig)

# Try convert provided manual SVG to PNG (if present) for PPTX embed
given_svg = OUTPUT_DIR / 'chart_given_large.svg'
converted_given_png = OUTPUT_DIR / 'chart_given_large.png'
try:
    import cairosvg
    if given_svg.exists():
        cairosvg.svg2png(url=str(given_svg), write_to=str(converted_given_png), dpi=300)
        print(f"Converted existing SVG to PNG: {converted_given_png}")
    else:
        print(f"No manual SVG found at {given_svg}, skipping conversion.")
except Exception as e:
    print(f"Could not convert manual SVG to PNG (cairosvg missing or error): {e}")

# Create PPTX with generated images
try:
    from pptx import Presentation
    from pptx.util import Inches
    prs = Presentation()
    blank = prs.slide_layouts[6]

    # Slide with sorted chart
    slide = prs.slides.add_slide(blank)
    left = Inches(0.5)
    top = Inches(0.8)
    width = Inches(9)
    slide.shapes.add_picture(str(png_path), left, top, width=width)

    # If we converted given chart, add it as second slide; else, add the SVG as a note slide
    if converted_given_png.exists():
        slide = prs.slides.add_slide(blank)
        slide.shapes.add_picture(str(converted_given_png), left, top, width=width)
    else:
        slide = prs.slides.add_slide(blank)
        tx = slide.shapes.add_textbox(left, top, width, Inches(1))
        tx.text = f'Original manual SVG available at: {given_svg}'

    pptx_path = OUTPUT_DIR / "charts_presentation.pptx"
    try:
        prs.save(pptx_path)
        print(f"Wrote PPTX: {pptx_path}")
    except PermissionError as e_save:
        alt_path = OUTPUT_DIR / "charts_presentation_v2.pptx"
        try:
            prs.save(alt_path)
            print(f"Could not overwrite existing PPTX (permission denied); wrote alternate PPTX: {alt_path}")
        except Exception as e2:
            print(f"Could not create PPTX: {e_save}; alternate save also failed: {e2}")
except Exception as e:
    print(f"Could not create PPTX: {e}")
