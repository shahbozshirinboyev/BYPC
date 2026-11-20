"""AGE Computers narxlar jadvalidan (Export varag'i) qismlarni bazaga yuklaydi."""
import json
from pathlib import Path

from django.core.management.base import BaseCommand

from builder.models import (
    CPU, Motherboard, RAM, Cooler, GPU, SSD, HDD, PSU, Case,
    Monitor, KeyboardMouse, Headset,
)

MODELS = {
    'cpu': CPU, 'mb': Motherboard, 'ram': RAM, 'cool': Cooler,
    'gpu': GPU, 'ssd': SSD, 'hdd': HDD, 'psu': PSU, 'case': Case,
    'mon': Monitor, 'kbm': KeyboardMouse, 'head': Headset,
}
DATA_FILE = Path(__file__).resolve().parents[2] / 'data' / 'age_products.json'


class Command(BaseCommand):
    help = "age_products.json dagi barcha qismlarni alohida jadvallarga yuklaydi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true',
                            help="Avval tegishli jadvallarni tozalaydi")

    def handle(self, *args, **options):
        payload = json.loads(DATA_FILE.read_text(encoding='utf-8'))
        total = 0
        for key, rows in payload.items():
            model = MODELS[key]
            allowed = {f.name for f in model._meta.fields}
            if options['clear']:
                model.objects.all().delete()
            for row in rows:
                defaults = {k: v for k, v in row.items()
                            if k != 'name' and k in allowed}
                model.objects.update_or_create(name=row['name'], defaults=defaults)
                total += 1
            self.stdout.write(self.style.SUCCESS(
                f"  {model._meta.verbose_name_plural}: {len(rows)} ta"))
        self.stdout.write(self.style.SUCCESS(f"Jami {total} ta qism yuklandi/yangilandi."))
