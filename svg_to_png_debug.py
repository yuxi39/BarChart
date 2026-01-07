from pathlib import Path
OUT = Path('d:/moqt-project/outputs')
log = OUT / 'convert_log.txt'
with open(log, 'w', encoding='utf-8') as fh:
    fh.write('Start conversion debug\n')
    try:
        import cairosvg
        fh.write('cairosvg imported OK\n')
    except Exception as e:
        fh.write(f'ERROR importing cairosvg: {e}\n')
    files = [
        ('chart_given_large.svg', 'chart_given_large.png'),
        ('chart_sorted_large.svg', 'chart_sorted_large.png'),
    ]
    for svg_name, png_name in files:
        svg_path = OUT / svg_name
        png_path = OUT / png_name
        fh.write(f'Processing {svg_path} -> {png_path}\n')
        if not svg_path.exists():
            fh.write(f'Missing SVG: {svg_path}\n')
            continue
        try:
            cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), dpi=300)
            fh.write(f'Called svg2png for {svg_name}\n')
            fh.write(f'PNG exists after call: {png_path.exists()}\n')
        except Exception as e:
            fh.write(f'Conversion exception for {svg_name}: {e}\n')
    fh.write('Done\n')
print('Wrote debug log to:', log)
