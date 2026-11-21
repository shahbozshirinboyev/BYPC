from django.conf import settings
from django.db import migrations


def forwards(apps, schema_editor):
    Profile = apps.get_model("builder", "Profile")
    User = apps.get_model(settings.AUTH_USER_MODEL)
    AIO = apps.get_model("builder", "AIO")

    for user in User.objects.all():
        Profile.objects.get_or_create(
            user_id=user.pk,
            defaults={"role": "admin" if user.is_superuser else "guest"},
        )

    for aio in AIO.objects.all():
        changed = []
        if not aio.ram_type:
            aio.ram_type = "DDR5" if aio.ddr5 else "DDR4"
            changed.append("ram_type")
        if not aio.m2_slots and aio.m2_nvme:
            aio.m2_slots = 1
            changed.append("m2_slots")
        if changed:
            aio.save(update_fields=changed)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("builder", "0007_printer_aio_m2_slots_aio_ram_type_savedbuild_user_and_more"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
