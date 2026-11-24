"""RAM xususiyatlarini ro'yxatdan to'ldirish va nomlarni qayta yig'ish."""
import re

from django.db import migrations


def _modules(name):
    m = re.search(r"(\d+)\s*[x×]\s*(\d+)", name, re.I) or re.search(
        r"(\d+)\s*(?:GB)?\s*\*\s*(\d+)", name, re.I)
    if not m:
        return 1
    a, b = int(m.group(1)), int(m.group(2))
    if 1 < b <= 4:
        return b
    if 1 < a <= 4:
        return a
    return 1


def _build(r):
    """Model build_name() bilan bir xil tartib."""
    per = r.capacity_gb // r.modules if r.modules and r.capacity_gb else r.capacity_gb
    kit = str(per) + 'x' + str(r.modules) if r.modules == 2 and per else ""
    parts = [
        r.brand,
        str(r.capacity_gb) + 'GB' if r.capacity_gb else "",
        r.ram_type,
        str(r.speed_mhz) + 'MHz' if r.speed_mhz else "",
        kit,
        'SODIMM' if r.form_factor == 'SODIMM' else "",
        'CL' + str(r.cl) if r.cl else "",
        r.heatsink,
        'LongDIMM' if r.long_dimm else "",
        'RGB' if r.rgb else "",
        r.note,
    ]
    return " ".join(p for p in parts if p).strip()[:200] or "RAM"


# Ro'yxatdagi, bazada yo'q modellar: brend, tur, hajm, tezlik, modullar,
# form-faktor, RGB, CL, radiator, long, izoh, narx.
EXTRA = [
    ("Adata", "DDR5", 16, 5600, 1, "SODIMM", False, None, "", False, "", 235),
    ("PNY", "DDR5", 16, 0, 1, "SODIMM", False, None, "", False, "", 205),
    ("NETAC", "DDR4", 16, 3200, 1, "SODIMM", False, None, "", False, "", 85),
    ("Lexar", "DDR4", 8, 3200, 1, "SODIMM", False, None, "", False, "", 50),
    ("Lexar", "DDR4", 16, 3200, 1, "SODIMM", False, None, "", False, "", 90),
    ("Lexar", "DDR4", 32, 3200, 1, "SODIMM", False, None, "", False, "", 270),
    ("Lexar", "DDR5", 8, 5600, 1, "SODIMM", False, None, "", False, "", 132),
    ("Lexar", "DDR5", 16, 0, 1, "SODIMM", False, None, "", False, "", 226),
    ("Lexar", "DDR5", 16, 5600, 1, "SODIMM", False, None, "", False, "", 244),
    ("Lexar", "DDR5", 16, 0, 2, "DIMM", True, None, "", False, "", 255),
    ("Lexar", "DDR5", 32, 5600, 1, "SODIMM", False, None, "", False, "", 368),
    ("Lexar", "DDR5", 32, 0, 2, "DIMM", True, None, "", False, "", 535),
    ("Crucial", "DDR4", 16, 3200, 1, "SODIMM", False, None, "", False, "", 121),
    ("Lexar", "DDR5", 32, 5600, 1, "DIMM", False, None, "", False, "", 495),
    ("Lexar", "DDR4", 32, 3200, 2, "DIMM", True, None, "", False, "", 70),
]


def forwards(apps, schema_editor):
    RAM = apps.get_model("products", "RAM")
    for r in RAM.objects.all():
        n = r.name or ""
        r.modules = _modules(n)
        r.form_factor = "SODIMM" if re.search(r"sodimm?|sodim", n, re.I) else "DIMM"
        r.rgb = bool(re.search(r"\brgb\b", n, re.I))
        cl = re.search(r"\bC(\d{2})\b", n, re.I)
        r.cl = int(cl.group(1)) if cl else None
        r.heatsink = "Silver" if "silver" in n.lower() else (
            "Black" if "black" in n.lower() or "radiator" in n.lower() else "")
        r.long_dimm = "longdimm" in n.lower()
        r.note = "Hynix A-die" if "hynix" in n.lower() else ""
        if r.brand.lower() == "gmoc" and r.ram_type == "DDR5":
            r.speed_mhz = 6000  # ro'yxatdagi "600MHz" — xato yozuv
        r.name = _build(r)
        r.save(update_fields=["name", "modules", "form_factor", "rgb", "cl",
                              "heatsink", "long_dimm", "note", "speed_mhz"])

    for brand, rtype, cap, speed, mods, form, rgb, cl, sink, long, note, price in EXTRA:
        defaults = dict(price=price, rgb=rgb, cl=cl, heatsink=sink,
                        long_dimm=long, note=note)
        r, _ = RAM.objects.update_or_create(
            brand=brand, ram_type=rtype, capacity_gb=cap, speed_mhz=speed,
            modules=mods, form_factor=form, defaults=defaults)
        r.name = _build(r)
        r.save(update_fields=["name"])


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0017_alter_ram_options_ram_cl_ram_form_factor_and_more"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
