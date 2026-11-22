"""Eski `builder.*` mahsulot content-type'larini tozalaydi.

Mahsulotlar `products` ilovasiga ko'chgach, eski content-type va ularga
bog'langan ruxsatlar keraksiz bo'lib qoladi. Mahsulot ma'lumotlariga
tegmaydi — faqat Django ichki yozuvlari o'chiriladi.
"""
from django.db import migrations


OLD_MODELS = [
    "aio", "case", "cooler", "cpu", "gpu", "hdd", "headset",
    "keyboardmouse", "monitor", "motherboard", "printer", "psu", "ram", "ssd",
]


def remove_old_content_types(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    ContentType.objects.filter(app_label="builder", model__in=OLD_MODELS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(remove_old_content_types, migrations.RunPython.noop),
    ]
