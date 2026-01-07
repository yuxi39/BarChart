from PIL import Image, ImageDraw
im=Image.open('outputs/chart_sorted.png').convert('RGB')
w,h=im.size
px=im.load()
col_counts=[sum(1 for y in range(h) if px[x,y]==(0,0,0)) for x in range(w)]
row_counts=[sum(1 for x in range(w) if px[x,y]==(0,0,0)) for y in range(h)]
cols=[i for i,c in enumerate(col_counts) if c>h*0.01]
rows=[i for i,c in enumerate(row_counts) if c>w*0.01]
print('size',w,h)
print('cols exceeding 1% black:', cols[:20])
print('rows exceeding 1% black:', rows[:20])
mx=max(col_counts)
xs=[i for i,c in enumerate(col_counts) if c==mx]
print('max black count',mx,'at columns',xs[:10])
# Save image highlight
draw=ImageDraw.Draw(im)
for x in xs:
    draw.line([(x,0),(x,h)], fill=(255,0,0))
for x in cols[:50]:
    draw.line([(x,0),(x,10)], fill=(0,255,0))
im.save('outputs/chart_sorted_debug.png')
print('Wrote outputs/chart_sorted_debug.png')