# -*- coding: utf-8 -*-
"""
Recreate the horizontal bar chart sorted descending (largest at top) and export PNG + PPTX.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys, os, logging
import numpy as np
import argparse
import json
import textwrap
from typing import List, Tuple, Dict

print('DEBUG: script started, cwd=', os.getcwd())
sys.stdout.flush()
logging.basicConfig(level=logging.INFO)
logging.debug('debug logging enabled')
# Save outputs into repository root outputs folder (use cwd to avoid PATH oddities)
OUTPUT_DIR = Path.cwd() / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
print(f"Using OUTPUT_DIR: {OUTPUT_DIR}")

# Default data (used if no config is provided)
default_data = {
    "项目A": 1234.5,
    "项目B": 987.3,
    "项目C": 756.2,
    "项目D": 543.1,
    "项目E": 321.0,
}

# We'll determine data and headers via CLI/config below; for now set placeholders
# Data loading and sorting happens after parsing arguments and optional config file

# Dynamic layout and axes will be created later after we know the data size
# (created after sorting so sizing can adapt to number of rows)


# Use Agg backend for headless environments and configure fonts
mpl.use('Agg')
mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial"]
mpl.rcParams["axes.unicode_minus"] = False


# ------------------------
# CLI / Config parsing
# ------------------------
parser = argparse.ArgumentParser(description='Generate a sorted horizontal bar chart from JSON/config.')
parser.add_argument('--config', type=str, help='Path to JSON config file that contains title, tag, unit, left_summary, data')
parser.add_argument('--data-file', type=str, help='Path to a JSON file containing just the data list [[name, value], ...]')
parser.add_argument('--title', type=str, help='Chart title (overrides config)')
parser.add_argument('--tag', type=str, help='Right header tag (e.g., 回款金额)')
parser.add_argument('--unit', type=str, help='Unit string (e.g., 万元)')
parser.add_argument('--left-summary', dest='left_summary', type=str, default=None, help='Left summary label')
parser.add_argument('--output-dir', type=str, help='Output directory (overrides default)')
parser.add_argument('--overwrite-pptx', action='store_true', help='Allow overwriting existing PPTX')
args = parser.parse_args()

# allow override of output dir
if args.output_dir:
    OUTPUT_DIR = Path(args.output_dir)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

config = {}
# load config if provided
if args.config:
    try:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Could not read config file {args.config}: {e}")
        config = {}

# load minimal data file if provided
if args.data_file:
    try:
        with open(args.data_file, 'r', encoding='utf-8') as f:
            dfile = json.load(f)
            # expect list of [name,value]
            if isinstance(dfile, dict):
                config.setdefault('data', list(dfile.items()))
            else:
                config.setdefault('data', dfile)
    except Exception as e:
        print(f"Could not read data file {args.data_file}: {e}")

# merge CLI simple overrides
if args.title:
    config['title'] = args.title
if args.tag:
    config['tag'] = args.tag
if args.unit:
    config['unit'] = args.unit
if args.left_summary:
    config['left_summary'] = args.left_summary

# Finalize data: prefer config['data'] -> default_data
if 'data' in config and config['data']:
    # support either dict or list of pairs
    if isinstance(config['data'], dict):
        data = {str(k): float(v) for k, v in config['data'].items()}
    else:
        # expect list like [[name, value], ...]
        try:
            data = {str(k): float(v) for k, v in config['data']}
        except Exception:
            # fallback: try to coerce
            data = {str(item[0]): float(item[1]) for item in config['data']}
else:
    data = default_data.copy()

# headers and labels
title = config.get('title', '示例数据对比分析')
tag = config.get('tag', '数据值')
unit = config.get('unit', '单位')
left_summary = config.get('left_summary', '总计')

print(f"Using chart title: {title}; tag: {tag}; unit: {unit}; left_summary: {left_summary}")

# ------------------------
# End CLI/config parsing
# ------------------------

# Sort descending by value and create dynamic layout based on row count
items = sorted(data.items(), key=lambda x: x[1], reverse=False)
names = [n for n, v in items]
values = [v for n, v in items]

# Dynamic layout sizing based on number of rows
n_rows = len(names)
base_height = 5.5
row_height = 0.5  # inches per row
fig_height = max(base_height, 1.2 + n_rows * row_height)
fig = plt.figure(figsize=(16, fig_height))  # width, height in inches
fig.patch.set_facecolor('white')

# adaptive bar height and font sizes
bar_height = min(0.6, max(0.25, 0.6 * (8.0 / max(8, n_rows))))
label_fontsize = 16 if n_rows <= 8 else max(10, int(16 - (n_rows - 8) // 2))
value_fontsize = 14 if n_rows <= 8 else max(9, int(14 - (n_rows - 8) // 2))
title_fontsize = 26 if n_rows <= 8 else max(16, int(26 - (n_rows - 8) // 2))
header_fontsize = max(11, int(title_fontsize * 0.45))

# axes: keep the same relative margins but the figure height now scales
ax = fig.add_axes([0.07, 0.06, 0.88, 0.76])  # left, bottom, width, height (lowered and slightly shorter)


# Colors matching the manual chart palette
colors = ["#89c0ff", "#ffb3e6", "#ffd88a", "#c7e9d7", "#78cfe0", "#7fe6d0"]


def strip_trailing_zero(v: float) -> str:
    s = f"{v:.1f}"
    if s.endswith('.0'):
        return s[:-2]
    return s

# Note: figure/axes were created dynamically above based on data; do not close them here

# Grid/style will be applied on the created axes


# Header background (drawn by figure rectangle)
# (we already set figure background above)

# New axes for chart area — expanded to match the larger blue-frame layout
# Make the plotting area a bit lower so the top bar has space from the header background
# Axes created dynamically below based on number of data rows

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
    ax.text(label_text_x, y, name, ha='right', va='center', fontsize=label_fontsize, fontfamily='Microsoft YaHei', clip_on=False)
    # value label: place outside on the right, bold, no unit (show original value)
    val_str = strip_trailing_zero(v)
    val_x = bar_start + bar_w + max_val*0.02
    ax.text(val_x, y, val_str, ha='left', va='center', fontsize=value_fontsize, color='#222', fontweight='bold', clip_on=False)

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
# left: total box (rounded) — use left_summary and unit
fig.text(0.03, header_y, f"{left_summary}：{total:.1f}{unit}", fontsize=header_fontsize, color='white', bbox=dict(boxstyle="round,pad=0.35", facecolor='#1f3b4d', edgecolor='#1f3b4d'), ha='left', va='center')
# center: title
fig.text(0.5, header_y, title, ha='center', va='center', fontsize=title_fontsize, color='white', fontweight='bold')
# right: tag and unit
fig.text(0.965, header_y, f"{tag}（{unit}）", ha='right', va='center', fontsize=header_fontsize, color='white', bbox=dict(boxstyle='round,pad=0.22', facecolor='#1f3b4d', edgecolor='#1f3b4d'))

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
