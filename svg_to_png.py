"""Convert SVG files in outputs/ to PNG at 300 DPI."""
from pathlib import Path
import sys

try:
    import cairosvg
except Exception as e:
    print("cairosvg not available:", e)
    sys.exit(2)

ROOT = Path('d:/moqt-project')
OUT = ROOT / 'outputs'
files = [
    ('chart_given_large.svg', 'chart_given_large.png'),
    ('chart_sorted_large.svg', 'chart_sorted_large.png'),
]

for svg_name, png_name in files:
    svg_path = OUT / svg_name
    png_path = OUT / png_name
    if not svg_path.exists():
        print(f"Missing: {svg_path}")
        continue
    print(f"Converting {svg_path} -> {png_path} (300 DPI)")
    try:
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), dpi=300)
        if png_path.exists():
            print(f"Wrote: {png_path}")
        else:
            print(f"Conversion reported OK but output missing: {png_path}")
    except Exception as e:
        print(f"Error converting {svg_path}: {e}")

print('Done')
