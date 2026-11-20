from django.db import models


SOCKET_CHOICES = [("LGA1700", "LGA1700"), ("AM4", "AM4"), ("AM5", "AM5")]
RAM_CHOICES = [("DDR4", "DDR4"), ("DDR5", "DDR5")]
MB_FORM_CHOICES = [("ATX", "ATX"), ("Micro-ATX", "Micro-ATX"), ("Mini-ITX", "Mini-ITX")]
SSD_INTERFACE_CHOICES = [("NVMe", "NVMe"), ("SATA", "SATA")]
HDD_FORM_CHOICES = [('3.5"', '3.5"'), ('2.5"', '2.5"')]
EFFICIENCY_CHOICES = [("None", "No certification"), ("80+ Bronze", "80+ Bronze"),
                      ("80+ Gold", "80+ Gold"), ("80+ Platinum", "80+ Platinum")]
COOLER_CHOICES = [("Air", "Havo"), ("Liquid", "Suvli")]
CASE_TYPE_CHOICES = [("Mini", "Mini-tower"), ("Mid", "Mid-tower"), ("Full", "Full-tower")]
PANEL_CHOICES = [("IPS", "IPS"), ("VA", "VA"), ("TN", "TN"), ("OLED", "OLED")]
CONNECTION_CHOICES = [("Wired", "Simli"), ("Wireless", "Simsiz")]


class Component(models.Model):
    """Barcha qismlar uchun umumiy asos."""
    name = models.CharField("Nomi", max_length=200)
    price = models.DecimalField("Narxi (USD)", max_digits=10, decimal_places=2, default=0)
    brand = models.CharField("Brend", max_length=50, blank=True, default="")

    class Meta:
        abstract = True
        ordering = ["id"]

    def __str__(self):
        return self.name


class CPU(Component):
    socket = models.CharField("Soket", max_length=20, choices=SOCKET_CHOICES, blank=True)
    cores = models.PositiveIntegerField("Yadrolar soni", default=4)
    watt = models.PositiveIntegerField("Quvvat (W)", default=0)

    class Meta(Component.Meta):
        verbose_name = "CPU"
        verbose_name_plural = "CPU"


class Motherboard(Component):
    socket = models.CharField("Soket", max_length=20, choices=SOCKET_CHOICES, blank=True)
    ram_type = models.CharField("RAM turi", max_length=10, choices=RAM_CHOICES, blank=True)
    form_factor = models.CharField("Form-faktor", max_length=20, choices=MB_FORM_CHOICES, blank=True)
    m2_slots = models.PositiveIntegerField("M.2 slotlari", default=1)

    class Meta(Component.Meta):
        verbose_name = "MB"
        verbose_name_plural = "MB"


class RAM(Component):
    ram_type = models.CharField("RAM turi", max_length=10, choices=RAM_CHOICES, blank=True)
    capacity_gb = models.PositiveIntegerField("Hajmi (GB)", default=0)
    speed_mhz = models.PositiveIntegerField("Tezligi (MHz)", default=0)

    class Meta(Component.Meta):
        verbose_name = "RAM"
        verbose_name_plural = "RAM"


class Cooler(Component):
    cooler_type = models.CharField("Turi", max_length=10, choices=COOLER_CHOICES, default="Air")
    sockets = models.CharField("Qo'llab-quvvatlagan soketlar", max_length=100,
                               help_text="Vergul bilan: LGA1700,AM4,AM5", default="")
    cooling_watt = models.PositiveIntegerField("Sovutish quvvati (W)", default=0)
    height_mm = models.PositiveIntegerField("Balandligi (mm)", default=0)

    class Meta(Component.Meta):
        verbose_name = "COOLER"
        verbose_name_plural = "COOLER"


class GPU(Component):
    chipset = models.CharField("Chipset", max_length=20, default="NVIDIA")
    vram_gb = models.PositiveIntegerField("Videoxotira (GB)", default=0)
    watt = models.PositiveIntegerField("Quvvat (W)", default=0)
    length_mm = models.PositiveIntegerField("Uzunligi (mm)", default=0)

    class Meta(Component.Meta):
        verbose_name = "GPU"
        verbose_name_plural = "GPU"


class SSD(Component):
    interface = models.CharField("Interfeys", max_length=10, choices=SSD_INTERFACE_CHOICES, default="NVMe")
    capacity_gb = models.PositiveIntegerField("Hajmi (GB)", default=0)

    class Meta(Component.Meta):
        verbose_name = "SSD"
        verbose_name_plural = "SSD"


class HDD(Component):
    form_factor = models.CharField("Form-faktor", max_length=10, choices=HDD_FORM_CHOICES, default='3.5"')
    capacity_gb = models.PositiveIntegerField("Hajmi (GB)", default=0)
    rpm = models.PositiveIntegerField("Aylanish tezligi (rpm)", default=0)

    class Meta(Component.Meta):
        verbose_name = "HDD"
        verbose_name_plural = "HDD"


class PSU(Component):
    watt = models.PositiveIntegerField("Quvvat (W)", default=0)
    efficiency = models.CharField("Sertifikat", max_length=20, choices=EFFICIENCY_CHOICES, default="None")
    modular = models.BooleanField("Modulli", default=False)

    class Meta(Component.Meta):
        verbose_name = "PSU"
        verbose_name_plural = "PSU"


class Case(Component):
    case_type = models.CharField("Korpus turi", max_length=10, choices=CASE_TYPE_CHOICES, default="Mid")
    form_factors = models.CharField("Mos platalar", max_length=100,
                                    help_text="Vergul bilan: ATX,Micro-ATX,Mini-ITX", default="ATX")
    max_gpu_length = models.PositiveIntegerField("Maks. GPU uzunligi (mm)", default=0)
    max_cooler_height = models.PositiveIntegerField("Maks. sovutgich balandligi (mm)", default=0)

    class Meta(Component.Meta):
        verbose_name = "CASE"
        verbose_name_plural = "CASE"


class Monitor(Component):
    panel = models.CharField("Matritsa", max_length=10, choices=PANEL_CHOICES, blank=True)
    size_inch = models.PositiveIntegerField("Diagonali (dyuym)", default=0)
    refresh_hz = models.PositiveIntegerField("Yangiilanish (Hz)", default=0)

    class Meta(Component.Meta):
        verbose_name = "MONITOR"
        verbose_name_plural = "MONITOR"


class KeyboardMouse(Component):
    connection = models.CharField("Ulanish", max_length=10, choices=CONNECTION_CHOICES, default="Wired")
    layout = models.CharField("Tartib", max_length=20, default="UZ/RU/EN")

    class Meta(Component.Meta):
        verbose_name = "KB&M"
        verbose_name_plural = "KB&M"


class Headset(Component):
    """Quloqchin / headset — ixtiyoriy aksessuar."""
    connection = models.CharField("Ulanish", max_length=10, choices=CONNECTION_CHOICES, default="Wired")
    surround = models.BooleanField("Ovoz atrofida (surround)", default=False)

    class Meta(Component.Meta):
        verbose_name = "HEADSET"
        verbose_name_plural = "HEADSET"


class Settings(models.Model):
    """Admin paneldan sozlanadigan umumiy parametrlar."""
    markup_percent = models.DecimalField("Ustama, %", max_digits=5, decimal_places=2, default=10)
    usd_to_uzs = models.DecimalField("1 USD = so'm", max_digits=10, decimal_places=2, default=12700)

    class Meta:
        verbose_name = "SETTINGS"
        verbose_name_plural = "SETTINGS"

    def __str__(self):
        return "BYPC sozlamalari"


class SavedBuild(models.Model):
    """Foydalanuvchi saqlagan yig'malar (session orqali bog'lanadi)."""
    name = models.CharField("Nomi", max_length=120)
    owner = models.CharField("Egasi (session)", max_length=64, db_index=True)
    data = models.JSONField("Tanlov", default=dict)
    total = models.DecimalField("Jami (USD)", max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField("Vaqti", auto_now_add=True)

    class Meta:
        verbose_name = "SAVED BUILD"
        verbose_name_plural = "SAVED BUILDS"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — ${self.total}"
