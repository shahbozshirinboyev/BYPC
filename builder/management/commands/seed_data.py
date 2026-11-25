"""
Namunaviy qismlarni bazaga yuklaydi (asl HTML jadvali asosida).
Idempotent: qayta ishga tushirilsa takroriy yozmaydi, balki yangilaydi.
"""
from django.core.management.base import BaseCommand

from products.models import (
    CPU, Motherboard, RAM, Cooler, AIO, GPU, SSD, HDD, PSU, Case,
    Monitor, Printer, KeyboardMouse, Headset,
)

ALL_SOCKETS = "LGA1700,AM4,AM5"

DATA = {
    CPU: [
        ("Intel Core i5-14400 OEM (LGA1700)", 164, {"brand": "Intel", "socket": "LGA1700", "cores": 10, "watt": 65}),
        ("AMD Ryzen 5 5600", 120, {"brand": "AMD", "socket": "AM4", "cores": 6, "watt": 65}),
        ("AMD Ryzen 5 7600", 200, {"brand": "AMD", "socket": "AM5", "cores": 6, "watt": 65}),
        ("AMD Ryzen 7 7800X3D", 400, {"brand": "AMD", "socket": "AM5", "cores": 8, "watt": 120}),
        ("Intel Core i5-13400F", 180, {"brand": "Intel", "socket": "LGA1700", "cores": 10, "watt": 65}),
        ("Intel Core i7-14700K", 390, {"brand": "Intel", "socket": "LGA1700", "cores": 20, "watt": 125}),
    ],
    Motherboard: [
        ("MSI PRO B760M-P (LGA1700, DDR4)", 85, {"brand": "MSI", "socket": "LGA1700", "ram_type": "DDR4", "form_factor": "Micro-ATX", "m2_slots": 1}),
        ("B550 (AM4, DDR4)", 105, {"brand": "ASUS", "socket": "AM4", "ram_type": "DDR4", "form_factor": "ATX", "m2_slots": 1}),
        ("A620 (AM5, DDR5)", 100, {"brand": "MSI", "socket": "AM5", "ram_type": "DDR5", "form_factor": "Micro-ATX", "m2_slots": 1}),
        ("B650 (AM5, DDR5)", 150, {"brand": "Gigabyte", "socket": "AM5", "ram_type": "DDR5", "form_factor": "ATX", "m2_slots": 2}),
        ("B760 (LGA1700, DDR4)", 110, {"brand": "ASUS", "socket": "LGA1700", "ram_type": "DDR4", "form_factor": "ATX", "m2_slots": 2}),
        ("Z790 (LGA1700, DDR5)", 230, {"brand": "MSI", "socket": "LGA1700", "ram_type": "DDR5", "form_factor": "ATX", "m2_slots": 3}),
    ],
    RAM: [
        ("Lexar 64 GB (2x32 GB) DDR4 3200", 164, {"brand": "Lexar", "ram_type": "DDR4", "capacity_gb": 64, "speed_mhz": 3200}),
        ("Lexar 32 GB (1x32 GB) DDR4 3200", 82, {"brand": "Lexar", "ram_type": "DDR4", "capacity_gb": 32, "speed_mhz": 3200}),
        ("16 GB (1x16 GB) DDR4 3200", 40, {"brand": "Lexar", "ram_type": "DDR4", "capacity_gb": 16, "speed_mhz": 3200}),
        ("32 GB (2x16 GB) DDR4 3200", 70, {"brand": "Lexar", "ram_type": "DDR4", "capacity_gb": 32, "speed_mhz": 3200}),
        ("16 GB (1x16 GB) DDR5 6000", 60, {"brand": "Corsair", "ram_type": "DDR5", "capacity_gb": 16, "speed_mhz": 6000}),
        ("32 GB (2x16 GB) DDR5 6000", 105, {"brand": "Corsair", "ram_type": "DDR5", "capacity_gb": 32, "speed_mhz": 6000}),
    ],
    Cooler: [
        ("CPU Cooler A50", 5, {"brand": "A50", "cooler_type": "Air", "sockets": ALL_SOCKETS, "cooling_watt": 65, "height_mm": 155}),
        ("Komplektdagi", 0, {"brand": "Stock", "cooler_type": "Air", "sockets": ALL_SOCKETS, "cooling_watt": 65, "height_mm": 50}),
        ("Minorali kuler", 35, {"brand": "Deepcool", "cooler_type": "Air", "sockets": ALL_SOCKETS, "cooling_watt": 120, "height_mm": 150}),
        ("240 mm suvli", 90, {"brand": "Corsair", "cooler_type": "Liquid", "sockets": ALL_SOCKETS, "cooling_watt": 250, "height_mm": 0}),
    ],
    AIO: [
        ('Xtech 24" IPS H61 Flat (Вебкамера WiFi) white', 125,
         {"brand": "Xtech", "screen_size": '24"', "panel": "IPS", "chipset": "H61"}),
        ('Xtech 24" IPS H81 Flat (Вебкамера WiFi) white', 129,
         {"brand": "Xtech", "screen_size": '24"', "panel": "IPS", "chipset": "H81"}),
        ('Xtech 24" IPS H410 Flat (Вебкамера WiFi) white', 139,
         {"brand": "Xtech", "screen_size": '24"', "panel": "IPS", "chipset": "H410"}),
        ('Xtech 24" IPS H510 Flat (Вебкамера WiFi M.2 nvme) white', 0,
         {"brand": "Xtech", "screen_size": '24"', "panel": "IPS", "chipset": "H510", "m2_nvme": True, "note": "Narx jadvalda ko‘rsatilmagan"}),
        ('Xtech 24" IPS H610 Flat (Вебкамера WiFi M.2 nvme) white', 136,
         {"brand": "Xtech", "screen_size": '24"', "panel": "IPS", "chipset": "H610", "m2_nvme": True}),
        ('Xtech 24" IPS H610 Model: S238 (Вебкамера WiFi M.2 nvme) white', 140,
         {"brand": "Xtech", "screen_size": '24"', "panel": "IPS", "chipset": "H610", "m2_nvme": True, "model_code": "S238"}),
        ('Xtech 27" IPS H61 Flat (Вебкамера WiFi) white', 150,
         {"brand": "Xtech", "screen_size": '27"', "panel": "IPS", "chipset": "H61"}),
        ('Xtech 27" IPS H510 Flat (Вебкамера WiFi M.2.nvme) white', 175,
         {"brand": "Xtech", "screen_size": '27"', "panel": "IPS", "chipset": "H510", "m2_nvme": True}),
        ('Xtech 27" IPS H610 Flat (Вебкамера WiFi M.2.nvme) white', 169,
         {"brand": "Xtech", "screen_size": '27"', "panel": "IPS", "chipset": "H610", "m2_nvme": True}),
        ('Xtech 27" IPS H610 DDR5 Flat (Вебкамера WiFi M.2.nvme) white', 0,
         {"brand": "Xtech", "screen_size": '27"', "panel": "IPS", "chipset": "H610", "m2_nvme": True, "ddr5": True, "note": "Narx jadvalda ko‘rsatilmagan"}),
        ('Xtech 32" IPS H61 Curved (WiFi M.2.nvme) white', 269,
         {"brand": "Xtech", "screen_size": '32"', "resolution": "2560x1440", "screen_type": "curved", "panel": "IPS", "chipset": "H61", "webcam": False, "m2_nvme": True}),
        ('Xtech 32" IPS H610 Curved (WiFi M.2.nvme) white', 275,
         {"brand": "Xtech", "screen_size": '32"', "resolution": "2560x1440", "screen_type": "curved", "panel": "IPS", "chipset": "H610", "webcam": False, "m2_nvme": True}),
        ('No Name 24" H610 New model', 136,
         {"brand": "No Name", "screen_size": '24"', "panel": "—", "chipset": "H610", "note": "New model"}),
    ],
    GPU: [
        ("Axle GeForce RTX 3060 12GB", 300, {"brand": "Axle", "chipset": "NVIDIA", "vram_gb": 12, "watt": 170, "length_mm": 240}),
        ("Alohida kartasiz", 0, {"brand": "—", "chipset": "None", "vram_gb": 0, "watt": 0, "length_mm": 0}),
        ("Radeon RX 7600 8GB", 270, {"brand": "AMD", "chipset": "AMD", "vram_gb": 8, "watt": 165, "length_mm": 240}),
        ("GeForce RTX 4060 8GB", 300, {"brand": "NVIDIA", "chipset": "NVIDIA", "vram_gb": 8, "watt": 115, "length_mm": 245}),
        ("Radeon RX 7800 XT 16GB", 500, {"brand": "AMD", "chipset": "AMD", "vram_gb": 16, "watt": 263, "length_mm": 320}),
        ("GeForce RTX 4070 Super 12GB", 600, {"brand": "NVIDIA", "chipset": "NVIDIA", "vram_gb": 12, "watt": 220, "length_mm": 300}),
    ],
    SSD: [
        ("MicroFrom NVMe 1 TB", 113, {"brand": "MicroFrom", "interface": "NVMe", "capacity_gb": 1024}),
        ("500 GB NVMe", 40, {"brand": "Samsung", "interface": "NVMe", "capacity_gb": 500}),
        ("1 TB NVMe", 70, {"brand": "Samsung", "interface": "NVMe", "capacity_gb": 1000}),
        ("2 TB NVMe", 130, {"brand": "WD", "interface": "NVMe", "capacity_gb": 2000}),
    ],
    HDD: [
        ("HDD 1 TB 7200 rpm", 45, {"brand": "Seagate", "form_factor": '3.5"', "capacity_gb": 1000, "rpm": 7200}),
        ("HDD 2 TB 7200 rpm", 65, {"brand": "Seagate", "form_factor": '3.5"', "capacity_gb": 2000, "rpm": 7200}),
        ("HDD 4 TB 5400 rpm", 100, {"brand": "WD", "form_factor": '3.5"', "capacity_gb": 4000, "rpm": 5400}),
    ],
    PSU: [
        ("X-Power 850 W 80+", 45, {"brand": "X-Power", "watt": 850, "efficiency": "80+ Bronze", "modular": False}),
        ("450 W", 45, {"brand": "Generic", "watt": 450, "efficiency": "None", "modular": False}),
        ("650 W 80+ Bronze", 70, {"brand": "Corsair", "watt": 650, "efficiency": "80+ Bronze", "modular": False}),
        ("750 W 80+ Gold", 95, {"brand": "Corsair", "watt": 750, "efficiency": "80+ Gold", "modular": True}),
        ("850 W 80+ Gold", 125, {"brand": "Corsair", "watt": 850, "efficiency": "80+ Gold", "modular": True}),
    ],
    Case: [
        ("Xtech R-25 oq, RGB", 26, {"brand": "Xtech", "case_type": "Mini", "form_factors": "Micro-ATX,Mini-ITX", "max_gpu_length": 300, "max_cooler_height": 155}),
        ("Oddiy korpus", 45, {"brand": "Generic", "case_type": "Mid", "form_factors": "ATX,Micro-ATX,Mini-ITX", "max_gpu_length": 350, "max_cooler_height": 160}),
        ("Mid-tower, shamollatgichli", 85, {"brand": "Deepcool", "case_type": "Mid", "form_factors": "ATX,Micro-ATX,Mini-ITX", "max_gpu_length": 400, "max_cooler_height": 165}),
        ("Premium shisha korpus", 140, {"brand": "Corsair", "case_type": "Full", "form_factors": "ATX,Micro-ATX,Mini-ITX", "max_gpu_length": 420, "max_cooler_height": 170}),
    ],
    Monitor: [
        ("Xtech 27 inch IPS 165 Hz egri (SG-GM270HL)", 105, {"brand": "Xtech", "panel": "IPS", "size_inch": 27, "refresh_hz": 165}),
    ],
    Printer: [
        ("HP LaserJet Pro M404dn", 220, {"brand": "HP", "printer_type": "Laser", "connection": "Wired", "paper_size": "A4", "color_print": False, "duplex": True, "speed_ppm": 38}),
        ("HP Color LaserJet Pro MFP M479fdw", 480, {"brand": "HP", "printer_type": "Laser", "connection": "Wireless", "paper_size": "A4", "color_print": True, "duplex": True, "speed_ppm": 28}),
        ("Canon PIXMA G3411", 210, {"brand": "Canon", "printer_type": "Inkjet", "connection": "Wired", "paper_size": "A4", "color_print": True, "duplex": False, "speed_ppm": 11}),
        ("Epson EcoTank L3250", 195, {"brand": "Epson", "printer_type": "Inkjet", "connection": "Wireless", "paper_size": "A4", "color_print": True, "duplex": False, "speed_ppm": 10}),
        ("Xerox B1025", 640, {"brand": "Xerox", "printer_type": "Laser", "connection": "Wired", "paper_size": "A4+A3", "color_print": False, "duplex": True, "speed_ppm": 45}),
        ("Brother DCP-L2540DW", 260, {"brand": "Brother", "printer_type": "LED", "connection": "Wireless", "paper_size": "A4", "color_print": False, "duplex": True, "speed_ppm": 30}),
    ],
    KeyboardMouse: [
        ("", 8, {"brand": "Metoo", "model_code": "C20", "bundle_type": "combo", "connection": "Wireless",
                "layout": "EN/RU", "lighting": "none", "switch_type": "membrane", "color": "white"}),
    ],
    Headset: [
        ("Genesis Radium 300 (3.5 mm)", 18, {"brand": "Genesis", "connection": "Wired", "surround": False}),
        ("Logitech G432 7.1", 45, {"brand": "Logitech", "connection": "Wired", "surround": True}),
        ("HyperX Cloud II", 60, {"brand": "HyperX", "connection": "Wired", "surround": True}),
    ],
}


class Command(BaseCommand):
    help = "Katalogga namunaviy qismlarni kiritadi/yangilaydi"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true",
                            help="Avval barcha qismlarni o'chirib, qayta kiritadi")

    def handle(self, *args, **options):
        total = 0
        for model, rows in DATA.items():
            if options["clear"]:
                model.objects.all().delete()
            for name, price, extra in rows:
                defaults = {"price": price, **extra}
                if model is AIO:
                    defaults["m2_slots"] = 1 if defaults.get("m2_nvme") else 0
                    defaults["ram_type"] = "DDR5" if defaults.get("ddr5") else "DDR4"
                model.objects.update_or_create(name=name, defaults=defaults)
                total += 1
            self.stdout.write(self.style.SUCCESS(
                f"  {model._meta.verbose_name_plural}: {len(rows)} ta"))
        self.stdout.write(self.style.SUCCESS(f"Jami {total} ta qism bazaga kiritildi."))
