"""يولّد مخطط الدور الأرضي لقطعة أرض 12.60 م × 23.00 م (SVG + HTML)."""
import math, os

W, L = 12.6, 23.0          # عرض الواجهة × عمق القطعة (متر)
S = 40                     # بكسل لكل متر
M = 90                     # هامش للأبعاد
EXT, INT = 0.25, 0.15      # سماكة الجدران الخارجية / الداخلية

def X(v): return M + v * S
def Y(v): return M + v * S

# (الاسم, المضلع بالأمتار, اللون, نوع)
R = lambda x0, y0, x1, y1: [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
rooms = [
    ("غرفة نوم 1", R(0, 0, 4.6, 4.6), "#f3ead9", "room"),
    ("مصلى", R(4.6, 0, 6.2, 2.8), "#efe3cc", "room"),
    ("غرفة نوم رئيسية", R(6.2, 0, 10.2, 4.6), "#f3ead9", "room"),
    ("دريسنج", R(10.2, 0, 12.6, 2.4), "#ece4d6", "room"),
    ("حمام", R(10.2, 2.4, 12.6, 4.6), "#dbe9f2", "wet"),
    ("موزع", [(4.6, 2.8), (6.2, 2.8), (6.2, 4.6), (9.2, 4.6), (9.2, 9.0), (8.4, 9.0),
              (8.4, 6.6), (5.4, 6.6), (5.4, 4.6), (4.6, 4.6)], "#f7f5f0", "circ"),
    ("حمام", R(9.2, 4.6, 12.6, 6.6), "#dbe9f2", "wet"),
    ("مطبخ تحضيري", R(9.2, 6.6, 12.6, 9.0), "#e9efe3", "room"),
    ("صالة", R(0, 4.6, 5.4, 12.2), "#f6efe2", "room"),
    ("درج", R(5.4, 6.6, 8.4, 9.0), "#e8dcc8", "stair"),
    ("مطبخ وطعام", R(8.4, 9.0, 12.6, 15.0), "#e9efe3", "room"),
    ("مجلس (استقبال)", R(0, 12.2, 5.4, 18.0), "#f6efe2", "room"),
    ("مدخل", [(5.4, 9.0), (8.4, 9.0), (8.4, 16.4), (6.9, 16.4), (6.9, 18.0), (5.4, 18.0)],
     "#f7f5f0", "circ"),
    ("حمام ضيوف", R(6.9, 16.4, 8.4, 18.0), "#dbe9f2", "wet"),
    ("موقف سيارة", R(8.4, 15.0, 12.6, 23.0), "#e4e4e4", "out"),
    ("حديقة أمامية", R(0, 18.0, 8.4, 23.0), "#d6e8c8", "out"),
]

# الأبواب: (اتجاه الجدار h/v, الإحداثي الثابت, بداية, نهاية, جهة الفتح +1/-1)
doors = [
    ("v", 4.6, 3.5, 4.4, -1),     # غرفة نوم 1
    ("h", 2.8, 5.0, 5.8, -1),     # مصلى
    ("h", 4.6, 7.0, 7.9, -1),     # غرفة رئيسية
    ("v", 10.2, 0.8, 1.6, 1),     # دريسنج
    ("h", 2.4, 10.8, 11.5, 1),    # حمام رئيسي
    ("v", 9.2, 5.3, 6.1, 1),      # حمام 2
    ("v", 9.2, 7.6, 8.5, 1),      # مطبخ تحضيري
    ("h", 9.0, 8.4, 9.2, 1),      # موزع ← مطبخ
    ("v", 5.4, 11.25, 12.15, -1), # صالة ← مدخل
    ("v", 5.4, 13.6, 14.8, -1),   # مجلس ← مدخل
    ("v", 8.4, 12.0, 12.9, 1),    # مطبخ ← مدخل
    ("v", 6.9, 16.6, 17.3, 1),    # حمام ضيوف
    ("h", 18.0, 5.5, 6.8, -1),    # الباب الرئيسي
    ("h", 15.0, 10.6, 11.5, 1),   # مطبخ ← موقف
]
# فتحات بدون أبواب (ممرات مفتوحة)
openings = [("h", 4.6, 4.6, 5.4), ("h", 6.6, 5.5, 8.3)]

def area(poly):
    a = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % len(poly)]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2

def centroid(poly):
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2

def pts(poly): return " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in poly)

out = []
w_px, h_px = int(W * S + 2 * M), int(L * S + 2 * M)
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_px} {h_px}" '
           f'width="{w_px}" height="{h_px}" font-family="Tahoma, Arial, sans-serif" direction="rtl">')
out.append(f'<rect width="{w_px}" height="{h_px}" fill="#ffffff"/>')
# حدود القطعة
out.append(f'<rect x="{X(0)}" y="{Y(0)}" width="{W*S}" height="{L*S}" fill="none" '
           f'stroke="#c0392b" stroke-width="1.5" stroke-dasharray="8 5"/>')

# تعبئة الغرف
for name, poly, col, kind in rooms:
    out.append(f'<polygon points="{pts(poly)}" fill="{col}"/>')

# تفاصيل: درج
x0, y0, x1, y1 = 5.4, 6.6, 8.4, 9.0
mid = (y0 + y1) / 2
for i in range(1, 12):
    xx = x0 + 0.25 * i
    if xx >= x1: break
    out.append(f'<line x1="{X(xx)}" y1="{Y(y0)}" x2="{X(xx)}" y2="{Y(mid-0.05)}" stroke="#a88f6a" stroke-width="1"/>')
    out.append(f'<line x1="{X(xx)}" y1="{Y(mid+0.05)}" x2="{X(xx)}" y2="{Y(y1)}" stroke="#a88f6a" stroke-width="1"/>')
out.append(f'<line x1="{X(x0)}" y1="{Y(mid)}" x2="{X(x1-0.3)}" y2="{Y(mid)}" stroke="#7a6545" stroke-width="2"/>')
out.append(f'<path d="M{X(x1-0.5)},{Y(y0+0.6)} L{X(x0+0.4)},{Y(y0+0.6)} L{X(x0+0.4)},{Y(y1-0.6)} L{X(x1-0.5)},{Y(y1-0.6)}" '
           f'fill="none" stroke="#7a6545" stroke-width="1.2" marker-end="url(#arr)"/>')
# حديقة أمامية: نافورة + جلسة
out.append(f'<rect x="{X(1.0)}" y="{Y(19.4)}" width="{2.0*S}" height="{2.0*S}" fill="#7fb6dd" stroke="#4d8ab5" rx="4"/>')
out.append(f'<circle cx="{X(2.0)}" cy="{Y(20.4)}" r="{0.45*S}" fill="none" stroke="#fff" stroke-width="2"/>')
out.append(f'<rect x="{X(4.6)}" y="{Y(19.8)}" width="{2.2*S}" height="{1.0*S}" fill="#c9b79a" stroke="#8d7a5c" rx="3"/>')
# ممر حجري للمدخل
for i in range(4):
    out.append(f'<rect x="{X(5.6)}" y="{Y(18.4+i*1.1)}" width="{1.1*S}" height="{0.7*S}" fill="#eae6de" stroke="#bbb"/>')
# سيارة
out.append(f'<rect x="{X(9.55)}" y="{Y(16.4)}" width="{1.9*S}" height="{4.7*S}" rx="14" fill="#cfd4da" stroke="#7d8790" stroke-width="1.5"/>')
out.append(f'<rect x="{X(9.8)}" y="{Y(17.6)}" width="{1.4*S}" height="{1.0*S}" rx="6" fill="#9aa5b0"/>')
out.append(f'<rect x="{X(9.8)}" y="{Y(19.4)}" width="{1.4*S}" height="{0.8*S}" rx="6" fill="#9aa5b0"/>')
# أثاث رمزي: أسرّة
def bed(x, y, w, h):
    out.append(f'<rect x="{X(x)}" y="{Y(y)}" width="{w*S}" height="{h*S}" fill="#fff" stroke="#8a7f70" rx="3"/>')
    out.append(f'<rect x="{X(x)}" y="{Y(y)}" width="{w*S}" height="{0.45*S}" fill="#d9cfc0" stroke="#8a7f70" rx="3"/>')
bed(0.6, 0.6, 1.0, 2.0); bed(2.0, 0.6, 1.0, 2.0); bed(7.3, 0.5, 1.8, 2.1)
# مطبخ: كاونتر + طاولة طعام
out.append(f'<rect x="{X(12.0)}" y="{Y(9.2)}" width="{0.6*S}" height="{3.6*S}" fill="#d0d0d0" stroke="#888"/>')
out.append(f'<rect x="{X(9.6)}" y="{Y(12.6)}" width="{1.0*S}" height="{1.8*S}" fill="#b08a5f" stroke="#6e5333" rx="3"/>')
# جلسات المجلس والصالة
for (x, y, w, h) in [(0.4, 12.6, 4.6, 0.7), (0.4, 16.9, 4.6, 0.7), (0.4, 13.5, 0.7, 3.2),
                     (0.4, 5.3, 0.7, 6.2), (1.4, 5.0, 3.4, 0.7), (4.4, 7.0, 0.7, 4.0)]:
    out.append(f'<rect x="{X(x)}" y="{Y(y)}" width="{w*S}" height="{h*S}" fill="#e2d6c4" stroke="#a8977d" rx="4"/>')
out.append(f'<rect x="{X(1.8)}" y="{Y(14.0)}" width="{2.4*S}" height="{2.2*S}" fill="none" stroke="#c4b49a" stroke-dasharray="4 3"/>')
out.append(f'<rect x="{X(1.6)}" y="{Y(7.2)}" width="{2.2*S}" height="{2.6*S}" fill="none" stroke="#c4b49a" stroke-dasharray="4 3"/>')

# الجدران
for name, poly, col, kind in rooms:
    if kind == "out": continue
    out.append(f'<polygon points="{pts(poly)}" fill="none" stroke="#2b2b2b" stroke-width="{INT*S:.1f}" stroke-linejoin="miter"/>')
# الجدار الخارجي للمبنى
outline = [(0, 0), (12.6, 0), (12.6, 15.0), (8.4, 15.0), (8.4, 18.0), (0, 18.0)]
out.append(f'<polygon points="{pts(outline)}" fill="none" stroke="#111" stroke-width="{EXT*S:.1f}" stroke-linejoin="miter"/>')
# سور القطعة حول الموقف والحديقة
out.append(f'<polyline points="{pts([(0,18),(0,23)])}" stroke="#555" stroke-width="5" fill="none"/>')
out.append(f'<polyline points="{pts([(12.6,15),(12.6,23)])}" stroke="#555" stroke-width="5" fill="none"/>')
out.append(f'<polyline points="{pts([(0,23),(5.2,23)])}" stroke="#555" stroke-width="5" fill="none"/>')
out.append(f'<polyline points="{pts([(7.2,23),(8.4,23)])}" stroke="#555" stroke-width="5" fill="none"/>')

# الأبواب
for o, c, a, b, s in doors:
    w = b - a
    if o == "h":
        out.append(f'<line x1="{X(a)}" y1="{Y(c)}" x2="{X(b)}" y2="{Y(c)}" stroke="#fff" stroke-width="{EXT*S+2:.1f}"/>')
        hx, hy = X(a), Y(c); ex, ey = X(a), Y(c + s * w)
        out.append(f'<line x1="{hx}" y1="{hy}" x2="{ex}" y2="{ey}" stroke="#333" stroke-width="1.5"/>')
        sweep = 1 if s < 0 else 0
        out.append(f'<path d="M{ex},{ey} A{w*S},{w*S} 0 0 {sweep} {X(b)},{Y(c)}" fill="none" stroke="#777" stroke-width="1" stroke-dasharray="3 2"/>')
    else:
        out.append(f'<line x1="{X(c)}" y1="{Y(a)}" x2="{X(c)}" y2="{Y(b)}" stroke="#fff" stroke-width="{EXT*S+2:.1f}"/>')
        hx, hy = X(c), Y(a); ex, ey = X(c + s * w), Y(a)
        out.append(f'<line x1="{hx}" y1="{hy}" x2="{ex}" y2="{ey}" stroke="#333" stroke-width="1.5"/>')
        sweep = 0 if s < 0 else 1
        out.append(f'<path d="M{ex},{ey} A{w*S},{w*S} 0 0 {sweep} {X(c)},{Y(b)}" fill="none" stroke="#777" stroke-width="1" stroke-dasharray="3 2"/>')
for o, c, a, b in openings:
    if o == "h":
        out.append(f'<line x1="{X(a)}" y1="{Y(c)}" x2="{X(b)}" y2="{Y(c)}" stroke="#f7f5f0" stroke-width="{EXT*S+2:.1f}"/>')

# أسماء الغرف + المقاسات + المساحة
for name, poly, col, kind in rooms:
    cx, cy = centroid(poly)
    if name == "موزع": cx, cy = 7.3, 5.6
    if name == "مدخل": cx, cy = 6.9, 14.6
    if name == "صالة": cy = 10.3
    if name == "مطبخ وطعام": cx, cy = 10.5, 10.6
    if name == "موقف سيارة": cy = 21.6
    if name == "حديقة أمامية": cx, cy = 2.0, 22.0
    if name == "غرفة نوم 1": cy = 3.3
    if name == "غرفة نوم رئيسية": cy = 3.4
    if name == "مجلس (استقبال)": cy = 15.1
    if name == "درج": cy = 7.15
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    bw, bh = max(xs) - min(xs), max(ys) - min(ys)
    small = bw < 2.5 or bh < 2.5
    fs = 10 if small else 15
    out.append(f'<text x="{X(cx)}" y="{Y(cy)}" text-anchor="middle" font-size="{fs}" font-weight="bold" fill="#222">{name}</text>')
    if kind in ("stair", "circ", "garden"):
        continue
    dims = f"{bw:.2f}×{bh:.2f}" if len(poly) == 4 else ""
    sub = f"{dims} m" if dims else ""
    out.append(f'<text x="{X(cx)}" y="{Y(cy)+fs+2}" text-anchor="middle" font-size="{fs-3}" fill="#555" direction="ltr">{sub}</text>')
    out.append(f'<text x="{X(cx)}" y="{Y(cy)+2*fs+2}" text-anchor="middle" font-size="{fs-3}" fill="#8a5a2b" direction="ltr">{area(poly):.1f} m²</text>')

# خطوط الأبعاد
out.append('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           '<path d="M0,0 L10,5 L0,10 z" fill="#7a6545"/></marker>'
           '<marker id="tk" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
           '<path d="M2,8 L8,2" stroke="#c0392b" stroke-width="1.5"/></marker></defs>')
def hdim(y_px, a, b, label, col="#c0392b"):
    out.append(f'<line x1="{X(a)}" y1="{y_px}" x2="{X(b)}" y2="{y_px}" stroke="{col}" stroke-width="1" marker-start="url(#tk)" marker-end="url(#tk)"/>')
    out.append(f'<text x="{(X(a)+X(b))/2}" y="{y_px-5}" text-anchor="middle" font-size="12" fill="{col}" direction="ltr">{label}</text>')
def vdim(x_px, a, b, label, col="#c0392b"):
    out.append(f'<line x1="{x_px}" y1="{Y(a)}" x2="{x_px}" y2="{Y(b)}" stroke="{col}" stroke-width="1" marker-start="url(#tk)" marker-end="url(#tk)"/>')
    cy = (Y(a) + Y(b)) / 2
    out.append(f'<text x="{x_px-6}" y="{cy}" text-anchor="middle" font-size="12" fill="{col}" direction="ltr" transform="rotate(-90 {x_px-6} {cy})">{label}</text>')

hdim(M - 50, 0, W, "12.60 m")
for a, b in [(0, 4.6), (4.6, 6.2), (6.2, 10.2), (10.2, 12.6)]:
    hdim(M - 22, a, b, f"{b-a:.2f}", "#555")
for a, b in [(0, 5.4), (5.4, 8.4), (8.4, 12.6)]:
    hdim(Y(L) + 30, a, b, f"{b-a:.2f}", "#555")
vdim(M - 50, 0, L, "23.00 m")
for a, b in [(0, 4.6), (4.6, 12.2), (12.2, 18.0), (18.0, 23.0)]:
    vdim(M - 22, a, b, f"{b-a:.2f}", "#555")
for a, b in [(0, 4.6), (4.6, 6.6), (6.6, 9.0), (9.0, 15.0), (15.0, 23.0)]:
    vdim(X(W) + 34, a, b, f"{b-a:.2f}", "#555")

# الشارع والشمال
out.append(f'<text x="{w_px/2}" y="{h_px-14}" text-anchor="middle" font-size="16" font-weight="bold" fill="#444">⟵ الشارع ⟶</text>')
out.append(f'<text x="{X(6.2)}" y="{Y(23)-6}" text-anchor="middle" font-size="11" fill="#444">مدخل المشاة</text>')
out.append(f'<text x="{X(10.5)}" y="{Y(23)-6}" text-anchor="middle" font-size="11" fill="#444">بوابة السيارة</text>')
out.append('</svg>')
svg = "\n".join(out)

here = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(here, "floor-plan.svg"), "w", encoding="utf-8").write(svg)

# جدول المساحات
built = 12.6 * 18.0 - 4.2 * 3.0
rows = "".join(
    f"<tr><td>{n}</td><td dir='ltr'>{area(p):.2f}</td></tr>" for n, p, c, k in rooms)
html = f"""<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>مخطط الدور الأرضي</title>
<style>
body{{font-family:Tahoma,Arial,sans-serif;background:#fafafa;color:#222;margin:0;padding:16px}}
h1{{font-size:22px;margin:0 0 4px}} p{{margin:4px 0 12px;color:#555}}
.wrap{{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start}}
svg{{max-width:100%;height:auto;background:#fff;border:1px solid #ddd}}
table{{border-collapse:collapse;background:#fff;min-width:260px}}
td,th{{border:1px solid #ddd;padding:6px 10px;font-size:14px}} th{{background:#f0ebe3}}
tfoot td{{font-weight:bold;background:#f7f3ec}}
</style></head><body>
<h1>مخطط الدور الأرضي — قطعة 12.60 م × 23.00 م</h1>
<p>مساحة الأرض: {W*L:.1f} م² · مسطح البناء (الدور الأرضي): {built:.1f} م² · الواجهة على الشارع من الأسفل</p>
<div class="wrap">{svg}
<table><thead><tr><th>الفراغ</th><th>المساحة م²</th></tr></thead>
<tbody>{rows}</tbody>
<tfoot><tr><td>مساحة الأرض</td><td dir='ltr'>{W*L:.2f}</td></tr>
<tr><td>مسطح البناء</td><td dir='ltr'>{built:.2f}</td></tr></tfoot></table></div>
</body></html>"""
open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(html)
print("ok", W * L, built)
