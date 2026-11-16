"""مخطط الطابق الأرضي — قطعة 12.60 × 23.00 م، سمك الجدار 20 سم.

الإحداثيات بالمتر على محاور الجدران (منتصف الجدار). الجدار الخارجي محوره على 0.10 من حد القطعة.
المقاسات المكتوبة داخل الغرف صافية (بين وجهي الجدران).
"""
import math
import os

W, L = 12.6, 23.0
T = 0.20                   # سمك الجدار
S = 40                     # بكسل لكل متر
M = 90

def X(v): return M + v * S
def Y(v): return M + v * S
R = lambda x0, y0, x1, y1: [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

D2, D1 = 15.4, 17.1        # الحد الأمامي للبناء: يمين (المطبخ) / يسار (الاستقبال)
E2, E1 = D2 - 0.1, D1 - 0.1

# كيرف المدخل: ربع دائرة نصف قطرها 1.20 م على محور الجدار، من ركن المطبخ إلى واجهة الاستقبال
CR = 1.2
CX, CY = 6.5 - CR, E1 - CR
def arc(cx, cy, rad, t0, t1, n=24):
    return [(cx + rad * math.cos(math.radians(t0 + (t1 - t0) * i / n)),
             cy + rad * math.sin(math.radians(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]
entrance = [(4.5, 11.3), (6.5, 11.3)] + arc(CX, CY, CR, 0, 90) + [(4.5, E1)]

# (الاسم, مضلع على المحاور, اللون, النوع)
rooms = [
    ("غرفة نوم 1", R(0.1, 0.1, 4.9, 4.5), "#f3ead9", "room"),
    ("حمام", R(4.9, 0.1, 7.3, 2.1), "#dbe9f2", "wet"),
    ("منور", R(4.9, 2.1, 7.3, 4.5), "#cfe3c2", "void"),
    ("غرفة ملابس", R(7.3, 0.1, 12.5, 1.7), "#ece4d6", "room"),
    ("غرفة نوم 2", R(7.3, 1.7, 12.5, 5.9), "#f3ead9", "room"),
    ("درج", R(0.1, 4.5, 3.5, 7.1), "#e8dcc8", "stair"),
    ("موزع", [(3.5, 4.5), (7.3, 4.5), (7.3, 5.9), (12.5, 5.9), (12.5, 7.1), (3.5, 7.1)], "#f7f5f0", "circ"),
    ("صالة", R(0.1, 7.1, 7.0, 11.3), "#f6efe2", "room"),
    ("حديقة داخلية", R(7.0, 7.1, 10.0, 11.3), "#cfe3c2", "void"),
    ("لوندري", [(10.0, 7.1), (12.5, 7.1), (12.5, 8.0), (11.1, 8.0), (11.1, 9.4), (10.0, 9.4)], "#e6e9f2", "wet"),
    ("WC", R(11.1, 8.0, 12.5, 9.4), "#dbe9f2", "wet"),
    ("حمام", R(10.0, 9.4, 12.5, 11.3), "#dbe9f2", "wet"),
    ("استقبال", R(0.1, 11.3, 4.5, E1), "#f6efe2", "room"),
    ("مدخل", entrance, "#f7f5f0", "circ"),
    ("مطبخ", R(6.5, 11.3, 10.7, 16.5), "#e9efe3", "room"),   # المطبخ البارد 4.00 × 5.00 م
    ("مطبخ حار", R(10.7, 11.3, 12.5, E2), "#e3ecd9", "room"),
    ("حمام خارجي", R(0.1, 21.5, 1.5, 22.9), "#dbe9f2", "wet"),
]
OB = R(0, 21.4, 1.6, 23.0)   # الحد الخارجي للحمام الخارجي
garden = ([(0, D1)] + arc(CX, CY, CR + T / 2, 90, 0) +
          [(6.6, 16.6), (8.2, 16.6), (8.2, 23.0), (1.6, 23.0), (1.6, 21.4), (0, 21.4)])
outside = [
    ("كراج", [(10.8, D2), (12.6, D2), (12.6, 23.0), (8.2, 23.0), (8.2, 16.6), (10.8, 16.6)], "#e4e4e4"),
    ("حديقة", garden, "#d6e8c8"),
]
display = {"مطبخ حار": "حار", "حمام خارجي": "حمام", "مطبخ": "مطبخ بارد"}

# الأبواب: (h/v, محور الجدار, من, إلى, جهة الفتح[, "b" = المفصلة عند النهاية])
doors = [
    ("h", 4.5, 3.75, 4.65, -1),    # غرفة نوم 1 ← موزع
    ("v", 7.3, 4.75, 5.65, 1),     # غرفة نوم 2 ← موزع
    ("h", 1.7, 7.6, 8.5, 1),       # غرفة ملابس
    ("v", 7.3, 0.5, 1.3, -1),      # حمام ← غرفة ملابس
    ("h", 7.1, 10.2, 11.0, 1),     # لوندري ← موزع
    ("v", 11.1, 8.35, 9.05, 1),    # WC ← لوندري
    ("h", 9.4, 10.2, 10.9, 1),     # حمام ← لوندري
    ("v", 4.5, 15.4, 16.6, -1),    # استقبال ← مدخل
    ("v", 6.5, 12.0, 12.9, 1),     # مطبخ ← مدخل
    ("h", E2, 10.9, 11.7, 1),      # مطبخ حار ← كراج
    ("v", 1.5, 21.8, 22.5, 1),     # حمام خارجي ← حديقة
]
# فتحات بلا أبواب
openings = [("v", 3.5, 4.6, 7.0), ("h", 7.1, 4.3, 6.7), ("h", 11.3, 4.6, 6.4), ("v", 10.7, 12.4, 13.8)]
# الشبابيك
windows = [
    ("v", 4.9, 2.5, 4.1), ("v", 7.3, 2.5, 4.1), ("h", 2.1, 5.5, 6.7), ("h", 4.5, 5.3, 6.9),   # على المنور
    ("v", 7.0, 7.6, 10.8), ("h", 7.1, 7.6, 9.4), ("h", 11.3, 7.6, 9.4),                       # صالة وموزع ومطبخ ← حديقة داخلية
    ("v", 10.0, 7.5, 8.5), ("v", 10.0, 10.1, 10.9),                                           # لوندري وحمام ← حديقة داخلية
    ("h", E2, 11.85, 12.35), ("h", 16.5, 7.4, 8.4),                                                                  # مطبخ حار ← كراج
    ("h", E1, 1.0, 3.4), ("h", E1, 4.72, 5.15),                                               # استقبال ومدخل ← حديقة أمامية
]

def area(poly):
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                   for i in range(len(poly)))) / 2
def perim(poly):
    return sum(math.hypot(poly[i][0] - poly[(i + 1) % len(poly)][0], poly[i][1] - poly[(i + 1) % len(poly)][1])
               for i in range(len(poly)))
def clear_area(poly):
    """المساحة الصافية بعد إزاحة حدود المضلع للداخل بنصف سمك الجدار (تصلح للزوايا القائمة والمنحنيات)."""
    d = T / 2
    n = len(poly)
    signed = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    sgn = 1 if signed > 0 else -1
    tsum = 0.0
    for i in range(n):
        (ax, ay), (bx, by), (cx, cy) = poly[i - 1], poly[i], poly[(i + 1) % n]
        v1, v2 = (bx - ax, by - ay), (cx - bx, cy - by)
        ang = sgn * math.atan2(v1[0] * v2[1] - v1[1] * v2[0], v1[0] * v2[0] + v1[1] * v2[1])
        tsum += math.tan(ang / 2)
    return area(poly) - perim(poly) * d + tsum * d * d
def bbox(poly):
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)
def pts(poly): return " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in poly)

o = []
w_px, h_px = int(W * S + 2 * M), int(L * S + 2 * M)
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_px} {h_px}" width="{w_px}" height="{h_px}" '
         f'font-family="Tahoma, Arial, sans-serif">')
o.append('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path d="M0,0 L10,5 L0,10 z" fill="#7a6545"/></marker>'
         '<marker id="tk" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
         '<path d="M2,8 L8,2" stroke="#c0392b" stroke-width="1.5"/></marker></defs>')
o.append(f'<rect width="{w_px}" height="{h_px}" fill="#fff"/>')

for name, poly, col in outside:
    o.append(f'<polygon points="{pts(poly)}" fill="{col}"/>')
for name, poly, col, kind in rooms:
    o.append(f'<polygon points="{pts(poly)}" fill="{col}"/>')

def rect(x, y, w, h, fill, stroke="#8a7f70", rx=3, extra=""):
    o.append(f'<rect x="{X(x):.1f}" y="{Y(y):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" fill="{fill}" stroke="{stroke}" rx="{rx}" {extra}/>')
def plant(cx, cy, rad=0.3):
    o.append(f'<circle cx="{X(cx)}" cy="{Y(cy)}" r="{rad*S}" fill="#7fb069" stroke="#4f7d3f"/>')

# --- أثاث رمزي ---
def bed(x, y, w, h, head="left"):
    rect(x, y, w, h, "#fff")
    if head == "left": rect(x, y, 0.45, h, "#d9cfc0")
    else: rect(x + w - 0.45, y, 0.45, h, "#d9cfc0")
bed(0.5, 0.8, 2.1, 1.8, "left")                 # غرفة 1
bed(10.2, 2.8, 2.1, 1.8, "right")               # غرفة 2
rect(9.5, 0.3, 2.8, 0.6, "#d8c7a8")             # خزانة ملابس
rect(11.9, 6.2, 0.4, 0.6, "#fff", "#5b8fb5")    # مغسلة الممر
# صالة: كنب + طاولة طعام
rect(0.4, 7.5, 0.8, 3.4, "#e2d6c4", "#a8977d"); rect(1.3, 7.4, 2.6, 0.8, "#e2d6c4", "#a8977d")
rect(1.6, 8.6, 2.2, 1.6, "none", "#c4b49a", 0, 'stroke-dasharray="4 3"')
rect(5.0, 8.6, 1.0, 1.6, "#b08a5f", "#6e5333")
# استقبال: كنب على شكل U
rect(0.4, 11.7, 0.8, 4.9, "#e2d6c4", "#a8977d"); rect(3.4, 11.7, 0.8, 3.5, "#e2d6c4", "#a8977d")
rect(1.3, 11.6, 2.0, 0.8, "#e2d6c4", "#a8977d")
rect(1.4, 13.0, 1.8, 2.6, "none", "#c4b49a", 0, 'stroke-dasharray="4 3"')
# مطبخ: كاونتر
rect(6.7, 15.4, 3.0, 0.6, "#d0d0d0", "#888", 0); rect(9.9, 11.5, 0.6, 0.8, "#d0d0d0", "#888", 0)
rect(11.7, 11.5, 0.6, 3.6, "#d0d0d0", "#888", 0)
# لوندري: غسالة
rect(11.75, 7.25, 0.6, 0.6, "#fff", "#5b8fb5")
o.append(f'<circle cx="{X(12.05)}" cy="{Y(7.55)}" r="{0.2*S}" fill="none" stroke="#5b8fb5"/>')
# نباتات: حديقة داخلية + منور + حديقة أمامية
for cx, cy in [(7.7, 7.8), (9.3, 7.8), (7.7, 10.6), (9.3, 10.6), (5.4, 2.7), (6.8, 2.7), (5.4, 3.9), (6.8, 3.9)]:
    plant(cx, cy)
for cx, cy in [(0.9, 18.0), (7.4, 18.9), (3.0, 22.1), (7.4, 22.1)]:
    plant(cx, cy, 0.45)
for i in range(5):                                # ممر من بوابة المشاة إلى باب الكيرف
    rect(5.2 + 0.2 * i, 21.35 - 1.0 * i, 1.0, 0.7, "#eae6de", "#bbb", 0)
# سيارة
rect(9.45, 17.0, 1.9, 4.7, "#cfd4da", "#7d8790", 14); rect(9.7, 18.2, 1.4, 1.0, "#9aa5b0", "none", 6)
rect(9.7, 20.0, 1.4, 0.8, "#9aa5b0", "none", 6)
# الدرج (شكل U)
sx0, sy0, sx1, sy1 = 0.2, 4.6, 3.4, 7.0
mid = (sy0 + sy1) / 2
x = sx0 + 0.9
while x < sx1 - 0.01:
    o.append(f'<line x1="{X(x)}" y1="{Y(sy0)}" x2="{X(x)}" y2="{Y(mid-0.05)}" stroke="#a88f6a"/>')
    o.append(f'<line x1="{X(x)}" y1="{Y(mid+0.05)}" x2="{X(x)}" y2="{Y(sy1)}" stroke="#a88f6a"/>')
    x += 0.28
o.append(f'<line x1="{X(sx0+0.9)}" y1="{Y(mid)}" x2="{X(sx1)}" y2="{Y(mid)}" stroke="#7a6545" stroke-width="3"/>')
o.append(f'<path d="M{X(sx1-0.2)},{Y(sy1-0.6)} L{X(sx0+0.45)},{Y(sy1-0.6)} L{X(sx0+0.45)},{Y(sy0+0.6)} L{X(sx1-0.3)},{Y(sy0+0.6)}" '
         f'fill="none" stroke="#7a6545" stroke-width="1.2" marker-end="url(#arr)"/>')

# --- الجدران (سمك 20 سم على المحاور) ---
for name, poly, col, kind in rooms:
    o.append(f'<polygon points="{pts(poly)}" fill="none" stroke="#1d1d1d" stroke-width="{T*S:.1f}" stroke-linejoin="miter"/>')
# سور القطعة
fence = [[(0.1, D1), (0.1, 22.9), (4.6, 22.9)], [(6.6, 22.9), (8.2, 22.9)], [(12.5, D2), (12.5, 22.9)]]
for f in fence:
    o.append(f'<polyline points="{pts(f)}" stroke="#555" stroke-width="{T*S:.1f}" fill="none"/>')
o.append(f'<rect x="{X(0)}" y="{Y(0)}" width="{W*S}" height="{L*S}" fill="none" stroke="#c0392b" stroke-width="1.2" stroke-dasharray="8 5"/>')

# --- فتحات وأبواب وشبابيك ---
gap = T * S + 2
def seg(orient, c, a, b):
    return (X(a), Y(c), X(b), Y(c)) if orient == "h" else (X(c), Y(a), X(c), Y(b))
for orient, c, a, b in openings:
    x1, y1, x2, y2 = seg(orient, c, a, b)
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#f7f5f0" stroke-width="{gap}"/>')
for d in doors:
    orient, c, a, b, sd = d[:5]
    hb = len(d) > 5                      # المفصلة عند b بدل a
    w = b - a
    x1, y1, x2, y2 = seg(orient, c, a, b)
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-width="{gap}"/>')
    hx, hy, fx, fy = (x2, y2, x1, y1) if hb else (x1, y1, x2, y2)
    if orient == "h":
        ex, ey = hx, Y(c + sd * w); sweep = 1 if sd < 0 else 0
    else:
        ex, ey = X(c + sd * w), hy; sweep = 0 if sd < 0 else 1
    if hb: sweep = 1 - sweep
    o.append(f'<line x1="{hx}" y1="{hy}" x2="{ex}" y2="{ey}" stroke="#333" stroke-width="1.5"/>')
    o.append(f'<path d="M{ex},{ey} A{w*S},{w*S} 0 0 {sweep} {fx},{fy}" fill="none" stroke="#777" stroke-dasharray="3 2"/>')
for orient, c, a, b in windows:
    x1, y1, x2, y2 = seg(orient, c, a, b)
    dx, dy = (0, 2.5) if orient == "h" else (2.5, 0)
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-width="{gap-1}"/>')
    for k in (-1, 1):
        o.append(f'<line x1="{x1+k*dx}" y1="{y1+k*dy}" x2="{x2+k*dx}" y2="{y2+k*dy}" stroke="#3b82c4" stroke-width="1.5"/>')

# الباب الرئيسي على الكيرف: وتر 1.00 م في منتصف القوس، يفتح للداخل والمفصلة جهة المطبخ
DW = 1.0
half = math.degrees(math.asin(DW / 2 / CR))
ta, tb = 45 - half, 45 + half
pa = (CX + CR * math.cos(math.radians(ta)), CY + CR * math.sin(math.radians(ta)))
pb = (CX + CR * math.cos(math.radians(tb)), CY + CR * math.sin(math.radians(tb)))
leaf = (pa[0] - DW * math.cos(math.radians(45)), pa[1] - DW * math.sin(math.radians(45)))
o.append(f'<polyline points="{pts(arc(CX, CY, CR, ta, tb, 12))}" fill="none" stroke="#fff" stroke-width="{gap}"/>')
o.append(f'<line x1="{X(pa[0]):.1f}" y1="{Y(pa[1]):.1f}" x2="{X(leaf[0]):.1f}" y2="{Y(leaf[1]):.1f}" stroke="#333" stroke-width="1.5"/>')
a0 = math.atan2(leaf[1] - pa[1], leaf[0] - pa[0]); a1 = math.atan2(pb[1] - pa[1], pb[0] - pa[0])
delta = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
o.append(f'<path d="M{X(leaf[0]):.1f},{Y(leaf[1]):.1f} A{DW*S},{DW*S} 0 0 {1 if delta > 0 else 0} {X(pb[0]):.1f},{Y(pb[1]):.1f}" '
         f'fill="none" stroke="#777" stroke-dasharray="3 2"/>')
o.append(f'<text x="{X(7.4)}" y="{Y(17.6)}" text-anchor="middle" font-size="9" fill="#444">مدخل كيرف</text>')
o.append(f'<text x="{X(7.4)}" y="{Y(17.9)}" text-anchor="middle" font-size="9" fill="#444">نق 1.20 م</text>')

# --- التسميات ---
label_pos = {"موزع": (5.6, 5.9), "غرفة نوم 1": (2.5, 3.35), "غرفة نوم 2": (9.0, 3.4), "صالة": (2.8, 9.2),
             "استقبال": (2.3, 14.0), "مدخل": (5.5, 13.6), "درج": (2.2, 5.9), "غرفة ملابس": (8.5, 0.75),
             "مطبخ": (8.6, 13.6), "مطبخ حار": (11.25, 13.2), "كراج": (10.4, 22.2), "حديقة": (3.4, 19.9),
             "منور": (6.1, 3.2), "حديقة داخلية": (8.5, 9.2), "لوندري": (10.55, 8.3), "WC": (11.8, 8.6),
             ("حمام", 10.0): (11.25, 10.3), "حمام خارجي": (0.8, 22.05)}
def label(name, poly, show=True, clear=True):
    x0, y0, x1, y1 = bbox(poly)
    cx, cy = label_pos.get((name, x0), label_pos.get(name, ((x0 + x1) / 2, (y0 + y1) / 2 - 0.15)))
    bw, bh = (x1 - x0 - T, y1 - y0 - T) if clear else (x1 - x0, y1 - y0)
    fs = 10 if min(bw, bh) < 2.5 else 14
    if name in ("موزع", "مدخل"): fs = 14
    if not show:   # الدرج: خلفية بيضاء خلف الاسم
        o.append(f'<rect x="{X(cx)-22}" y="{Y(cy)-15}" width="44" height="20" rx="4" fill="#fff" opacity="0.9"/>')
    o.append(f'<text x="{X(cx)}" y="{Y(cy)}" text-anchor="middle" font-size="{fs}" font-weight="bold" fill="#222">{display.get(name, name)}</text>')
    if not show: return
    a = clear_area(poly) if clear else area(poly)
    if len(poly) == 4:
        o.append(f'<text x="{X(cx)}" y="{Y(cy)+fs+1}" text-anchor="middle" font-size="{fs-3}" fill="#555">{bw:.2f}×{bh:.2f} m</text>')
        o.append(f'<text x="{X(cx)}" y="{Y(cy)+2*fs}" text-anchor="middle" font-size="{fs-3}" fill="#8a5a2b">{a:.1f} m²</text>')
    else:
        o.append(f'<text x="{X(cx)}" y="{Y(cy)+fs+1}" text-anchor="middle" font-size="{fs-3}" fill="#8a5a2b">{a:.1f} m²</text>')
for name, poly, col, kind in rooms:
    label(name, poly, show=(kind != "stair"))
for name, poly, col in outside:
    label(name, poly, clear=False)

# --- الأبعاد ---
def hdim(y_px, a, b, text, col="#555"):
    o.append(f'<line x1="{X(a)}" y1="{y_px}" x2="{X(b)}" y2="{y_px}" stroke="{col}" marker-start="url(#tk)" marker-end="url(#tk)"/>')
    o.append(f'<text x="{(X(a)+X(b))/2}" y="{y_px-5}" text-anchor="middle" font-size="12" fill="{col}">{text}</text>')
def vdim(x_px, a, b, text, col="#555"):
    cy = (Y(a) + Y(b)) / 2
    o.append(f'<line x1="{x_px}" y1="{Y(a)}" x2="{x_px}" y2="{Y(b)}" stroke="{col}" marker-start="url(#tk)" marker-end="url(#tk)"/>')
    o.append(f'<text x="{x_px-6}" y="{cy}" text-anchor="middle" font-size="12" fill="{col}" transform="rotate(-90 {x_px-6} {cy})">{text}</text>')
def chain(vals): return [(vals[i], vals[i + 1]) for i in range(len(vals) - 1)]

hdim(M - 50, 0, W, "12.60 m", "#c0392b")
for a, b in chain([0, 4.9, 7.3, 12.6]): hdim(M - 22, a, b, f"{b-a:.2f}")
for a, b in chain([0, 4.5, 6.5, 8.2, 12.6]): hdim(Y(L) + 30, a, b, f"{b-a:.2f}")
vdim(M - 50, 0, L, "23.00 m", "#c0392b")
for a, b in chain([0, 4.5, 7.1, 11.3, D1, 23.0]): vdim(M - 22, a, b, f"{b-a:.2f}")
for a, b in chain([0, 5.9, 7.1, 9.4, 11.3, D2, 23.0]): vdim(X(W) + 34, a, b, f"{b-a:.2f}")

o.append(f'<text x="{w_px/2}" y="{h_px-14}" text-anchor="middle" font-size="16" font-weight="bold" fill="#444">⟵ الشارع ⟶</text>')
o.append(f'<text x="{X(11.3)}" y="{Y(6.65)}" text-anchor="middle" font-size="9" fill="#444">مغسلة</text>')
o.append(f'<text x="{X(5.6)}" y="{Y(22.65)}" text-anchor="middle" font-size="11" fill="#444">مدخل المشاة</text>')
o.append(f'<text x="{X(10.4)}" y="{Y(22.9)}" text-anchor="middle" font-size="11" fill="#444">بوابة السيارة</text>')
o.append('</svg>')
svg = "\n".join(o)

# --- الحسابات ---
outer = [(0, 0), (W, 0), (W, D2), (10.8, D2), (10.8, 16.6), (6.6, 16.6), (6.6, CY)] + arc(CX, CY, CR + T / 2, 0, 90) + [(0, D1)]
footprint = area(outer)
voids = sum(clear_area(p) for n, p, c, k in rooms if k == "void")
built_main = footprint - voids
built = built_main + area(OB)
net = sum(clear_area(p) for n, p, c, k in rooms if k != "void")

here = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(here, "floor-plan.svg"), "w", encoding="utf-8").write(svg)

def dims(p):
    x0, y0, x1, y1 = bbox(p)
    return f"{x1-x0-T:.2f} × {y1-y0-T:.2f}" if len(p) == 4 else "—"
rows = "".join(f"<tr><td>{n}</td><td dir='ltr'>{dims(p)}</td><td dir='ltr'>{clear_area(p):.2f}</td></tr>"
               for n, p, c, k in rooms)
html = f"""<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>مخطط الطابق الأرضي</title>
<style>
body{{font-family:Tahoma,Arial,sans-serif;background:#fafafa;color:#222;margin:0;padding:16px}}
h1{{font-size:22px;margin:0 0 4px}} p{{margin:4px 0 12px;color:#555}}
.wrap{{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start}}
svg{{max-width:100%;height:auto;background:#fff;border:1px solid #ddd;direction:ltr}}
table{{border-collapse:collapse;background:#fff;min-width:300px}}
td,th{{border:1px solid #ddd;padding:6px 10px;font-size:14px}} th{{background:#f0ebe3}}
tfoot td{{font-weight:bold;background:#f7f3ec}}
</style></head><body>
<h1>مخطط الطابق الأرضي — قطعة 12.60 م × 23.00 م</h1>
<p>مساحة الأرض: {W*L:.1f} م² · مسطح البناء: {built:.1f} م² · سمك الجدران: 20 سم · المقاسات داخل الغرف صافية · الأبعاد الخارجية إلى محاور الجدران · الشارع من الأسفل</p>
<div class="wrap">{svg}
<table><thead><tr><th>الفراغ</th><th>المقاس الصافي (م)</th><th>المساحة الصافية م²</th></tr></thead>
<tbody>{rows}</tbody>
<tfoot><tr><td colspan="2">مساحة الأرض</td><td dir='ltr'>{W*L:.2f}</td></tr>
<tr><td colspan="2">المنور + الحديقة الداخلية (مكشوفة)</td><td dir='ltr'>{voids:.2f}</td></tr>
<tr><td colspan="2">مسطح البناء الرئيسي (مع الجدران)</td><td dir='ltr'>{built_main:.2f}</td></tr>
<tr><td colspan="2">الحمام الخارجي (مع الجدران)</td><td dir='ltr'>{area(OB):.2f}</td></tr>
<tr><td colspan="2">مسطح البناء الكلي</td><td dir='ltr'>{built:.2f}</td></tr>
<tr><td colspan="2">مجموع المساحات الصافية للغرف</td><td dir='ltr'>{net:.2f}</td></tr></tfoot></table></div>
</body></html>"""
open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(html)
print(f"plot={W*L:.2f} footprint={footprint:.2f} voids={voids:.2f} built_main={built_main:.2f} built={built:.2f} net={net:.2f}")
for n, p, c, k in rooms: print(f"  {n}: {dims(p)}  {clear_area(p):.2f}")
print(f"  garden={area(garden):.1f}")
