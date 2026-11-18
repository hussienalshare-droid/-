"""نموذج ثلاثي الأبعاد للطابق الأرضي (قطعة 12.60 × 23.00 م) من المخطط المعدّل (الصورة 5).
الإحداثيات بالمتر، الجدران سمك 0.20 م وارتفاع 3.00 م. ليست فيه فتحات أبواب/شبابيك."""
import json, os

T, H = 0.20, 3.0
# (الاسم, x0, y0, x1, y1, اللون, النوع)  النوع: room | well | out
rooms = [
    ("غرفة نوم 1", 0.0, 0.0, 4.9, 4.5, "#f3ead9", "room"),
    ("ممر", 4.9, 0.0, 5.9, 4.5, "#f7f5f0", "room"),
    ("حمام", 5.9, 0.0, 7.3, 2.0, "#dbe9f2", "room"),
    ("منور 1", 5.9, 2.0, 7.3, 3.6, "#cfe3c2", "well"),
    ("ممر", 4.9, 3.6, 7.3, 4.5, "#f7f5f0", "room"),
    ("غرفة ملابس", 7.3, 0.0, 12.6, 1.7, "#ece4d6", "room"),
    ("غرفة نوم 2", 7.3, 1.7, 12.6, 5.9, "#f3ead9", "room"),
    ("درج", 0.0, 4.5, 4.5, 7.1, "#e8dcc8", "room"),
    ("موزع", 4.5, 4.5, 7.3, 7.1, "#f7f5f0", "room"),
    ("موزع", 7.3, 5.9, 12.6, 7.1, "#f7f5f0", "room"),
    ("صالة", 0.0, 7.1, 6.5, 11.3, "#f6efe2", "room"),
    ("حديقة داخلية", 6.5, 7.1, 9.5, 10.2, "#cfe3c2", "well"),
    ("لوندري", 9.5, 7.1, 11.1, 8.5, "#e6e9f2", "room"),
    ("WC", 11.1, 7.1, 12.6, 8.5, "#dbe9f2", "room"),
    ("حمام", 9.5, 8.5, 12.6, 10.2, "#dbe9f2", "room"),
    ("مطبخ بارد", 6.5, 10.2, 10.8, 15.4, "#e9efe3", "room"),
    ("مطبخ حار", 10.8, 10.2, 12.6, 15.4, "#e3ecd9", "room"),
    ("استقبال", 0.0, 11.3, 4.5, 17.1, "#f6efe2", "room"),
    ("مدخل", 4.5, 11.3, 6.5, 17.1, "#f7f5f0", "room"),
    ("حديقة أمامية", 0.0, 17.1, 8.2, 23.0, "#d6e8c8", "out"),
    ("كراج", 8.2, 15.4, 12.6, 23.0, "#e4e4e4", "out"),
    ("حمام خارجي", 0.0, 21.5, 1.5, 23.0, "#dbe9f2", "room"),
]

walls = set()
def add_wall(x0, y0, x1, y1):
    walls.add((round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3)))
for name, x0, y0, x1, y1, col, kind in rooms:
    if kind == "out":
        continue
    # جدران المحيط (على محاور الحدود، سمك T)
    add_wall(x0 - T / 2, y0 - T / 2, x1 + T / 2, y0 + T / 2)
    add_wall(x0 - T / 2, y1 - T / 2, x1 + T / 2, y1 + T / 2)
    add_wall(x0 - T / 2, y0 + T / 2, x0 + T / 2, y1 - T / 2)
    add_wall(x1 - T / 2, y0 + T / 2, x1 + T / 2, y1 - T / 2)
# السور الخارجي للحديقة والكراج (جدار قصير)
for seg in [(0, 17.1, 0.2, 23.0), (12.4, 15.4, 12.6, 23.0)]:
    add_wall(*seg)

data = {
    "H": H,
    "rooms": [dict(name=n, x0=a, y0=b, x1=c, y1=d, color=col, kind=k) for n, a, b, c, d, col, k in rooms],
    "walls": [dict(x0=a, y0=b, x1=c, y1=d) for a, b, c, d in sorted(walls)],
}
here = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(here, "template.html"), encoding="utf-8").read()
import base64
def durl(fn):
    raw = open(os.path.join(here, "vendor", fn), "rb").read()
    return "data:text/javascript;base64," + base64.b64encode(raw).decode("ascii")
imap = {"imports": {"three": durl("three.module.js"),
                    "three/addons/OrbitControls.js": durl("OrbitControls.js")}}
html = tpl.replace("/*__IMPORTMAP__*/{}", json.dumps(imap))
html = html.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
open(os.path.join(here, "floor-plan-3d.html"), "w", encoding="utf-8").write(html)
print("walls", len(walls), "rooms", len(rooms))
