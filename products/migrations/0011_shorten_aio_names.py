from django.db import migrations


def shorten_names(apps, schema_editor):
    """Mavjud AIO nomlarini qisqa ko'rinishga o'tkazish."""
    AIO = apps.get_model("products", "AIO")
    color_labels = {"white": "White", "black": "Black"}
    for aio in AIO.objects.all():
        panel = aio.panel if aio.panel and aio.panel != "—" else ""
        parts = [
            aio.brand,
            aio.screen_size,
            panel,
            "Curved" if aio.screen_type == "curved" else "Flat",
            aio.chipset,
            aio.ram_type,
            color_labels.get(aio.color, aio.color),
        ]
        aio.name = " ".join(p for p in parts if p).strip()[:200] or "AIO"
        aio.save(update_fields=["name"])


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0010_alter_aio_brand_alter_case_brand_alter_cooler_brand_and_more"),
    ]

    operations = [
        migrations.RunPython(shorten_names, migrations.RunPython.noop),
    ]
