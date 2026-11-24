from django.db import migrations, models


def forwards(apps, schema_editor):
    AIO = apps.get_model("products", "AIO")
    color_labels = {"white": "Oq", "black": "Qora", "gray": "Kulrang"}
    for aio in AIO.objects.all():
        aio.screen_type = "curved" if aio.curved else "flat"
        panel = aio.panel if aio.panel and aio.panel != "—" else ""
        parts = [
            aio.brand,
            aio.screen_size,
            aio.resolution,
            panel,
            "Curved" if aio.curved else "Flat",
            "AIO",
            aio.chipset,
            aio.ram_type,
            f"M.2 x{aio.m2_slots}" if aio.m2_slots else "",
            color_labels.get(aio.color, aio.color),
        ]
        aio.name = " ".join(p for p in parts if p).strip()[:200] or "AIO"
        aio.save(update_fields=["screen_type", "name"])


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0005_alter_aio_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="aio",
            name="resolution",
            field=models.CharField(
                choices=[
                    ("1366x768", "HD (1366x768)"),
                    ("1920x1080", "Full HD (1920x1080)"),
                    ("2560x1440", "QHD (2560x1440)"),
                    ("3840x2160", "4K UHD (3840x2160)"),
                ],
                default="1920x1080",
                max_length=12,
                verbose_name="Ekran razmeri",
            ),
        ),
        migrations.AddField(
            model_name="aio",
            name="screen_type",
            field=models.CharField(
                choices=[("flat", "Flat"), ("curved", "Curved")],
                default="flat",
                max_length=10,
                verbose_name="Ekran turi",
            ),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="aio",
            name="curved",
        ),
    ]
