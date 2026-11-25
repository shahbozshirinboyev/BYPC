"""Mahsulot modellari.

Bu ilovada faqat katalog mahsulotlari saqlanadi:
CPU, AIO, MB, RAM, COOLER, GPU, SSD, HDD, PSU, CASE, MONITOR,
PRINTER, KB&M, HEADSET.

Jadvallar nomi (`db_table`) eski `builder_*` nomlarida qoldirilgan —
shu tufayli mavjud mahsulotlar va ularning ID'lari saqlanib qoladi.
"""
from django.db import models


SOCKET_CHOICES = [
    ("LGA1155", "LGA1155"), ("LGA1150", "LGA1150"), ("LGA1151", "LGA1151"),
    ("LGA1200", "LGA1200"), ("LGA1700", "LGA1700"), ("LGA1851", "LGA1851"),
    ("AM4", "AM4"), ("AM5", "AM5"),
]
RAM_CHOICES = [("DDR3", "DDR3"), ("DDR4", "DDR4"), ("DDR5", "DDR5")]
RAM_FORM_CHOICES = [("DIMM", "DIMM"), ("SODIMM", "SODIMM")]
RAM_MODULE_CHOICES = [(1, "1 ta"), (2, "2 ta")]
CPU_MEMORY_TYPE_CHOICES = [
    ("", "—"),
    ("DDR3", "DDR3"), ("DDR4", "DDR4"), ("DDR5", "DDR5"),
    ("DDR4/DDR5", "DDR4 / DDR5"),
]
CPU_GPU_CHOICES = [
    ("", "None"),
    ("Intel HD Graphics 2000", "Intel HD Graphics 2000"),
    ("Intel HD Graphics 2500", "Intel HD Graphics 2500"),
    ("Intel HD Graphics 3000", "Intel HD Graphics 3000"),
    ("Intel HD Graphics 4000", "Intel HD Graphics 4000"),
    ("Intel HD Graphics 4600", "Intel HD Graphics 4600"),
    ("Intel HD Graphics 530", "Intel HD Graphics 530"),
    ("Intel UHD Graphics 630", "Intel UHD Graphics 630"),
    ("Intel UHD Graphics 730", "Intel UHD Graphics 730"),
    ("Intel UHD Graphics 750", "Intel UHD Graphics 750"),
    ("Intel UHD Graphics 770", "Intel UHD Graphics 770"),
    ("Intel Graphics (Xe-LPG)", "Intel Graphics (Xe-LPG)"),
    ("AMD Radeon Vega 3", "AMD Radeon Vega 3"),
    ("AMD Radeon Vega 8", "AMD Radeon Vega 8"),
    ("AMD Radeon Vega 11", "AMD Radeon Vega 11"),
    ("AMD Radeon Graphics (RDNA 2)", "AMD Radeon Graphics (RDNA 2)"),
    ("AMD Radeon 760M", "AMD Radeon 760M"),
    ("AMD Radeon 780M", "AMD Radeon 780M"),
]
MB_FORM_CHOICES = [("ATX", "ATX"), ("Micro-ATX", "Micro-ATX"), ("Mini-ITX", "Mini-ITX")]
SSD_INTERFACE_CHOICES = [("NVMe", "NVMe"), ("SATA", "SATA")]
SSD_FORM_CHOICES = [('M.2', 'M.2'), ('2.5"', '2.5"')]
SSD_PCIE_CHOICES = [("", "—"), ("Gen3", "Gen3"), ("Gen4", "Gen4"), ("Gen5", "Gen5")]
HDD_FORM_CHOICES = [('3.5"', '3.5"'), ('2.5"', '2.5"')]
EFFICIENCY_CHOICES = [("None", "No certification"), ("80+ Bronze", "80+ Bronze"),
                      ("80+ Gold", "80+ Gold"), ("80+ Platinum", "80+ Platinum")]
COOLER_CHOICES = [("Air", "Havo"), ("Liquid", "Suvli")]
AIO_CHIPSET_CHOICES = [("H61", "H61"), ("H81", "H81"), ("H410", "H410"),
                       ("H510", "H510"), ("H610", "H610")]
AIO_SIZE_CHOICES = [('24"', '24"'), ('27"', '27"'), ('32"', '32"')]
AIO_PANEL_CHOICES = [("IPS", "IPS"), ("VA", "VA"), ("TN", "TN"), ("LED", "LED"), ("OLED", "OLED")]
AIO_COLOR_CHOICES = [("white", "White"), ("black", "Black")]
AIO_SOCKET_BY_CHIPSET = {
    "H61": "LGA1155",
    "H81": "LGA1150",
    "H410": "LGA1200",
    "H510": "LGA1200",
    "H610": "LGA1700",
}
AIO_SCREEN_TYPE_CHOICES = [("flat", "Flat"), ("curved", "Curved")]
AIO_RESOLUTION_CHOICES = [
    ("1366x768", "HD (1366x768)"),
    ("1920x1080", "Full HD (1920x1080)"),
    ("2560x1440", "QHD (2560x1440)"),
    ("3840x2160", "4K UHD (3840x2160)"),
]
AIO_SLOT_CHOICES = [(0, "0"), (1, "1"), (2, "2")]
CASE_TYPE_CHOICES = [("Mini", "Mini-tower"), ("Mid", "Mid-tower"), ("Full", "Full-tower")]
PANEL_CHOICES = [("IPS", "IPS"), ("VA", "VA"), ("TN", "TN"), ("LED", "LED"), ("OLED", "OLED")]
CONNECTION_CHOICES = [("Wired", "Simli"), ("Wireless", "Simsiz")]
KBM_CONNECTION_CHOICES = [("Wired", "Wired"), ("Wireless", "Wireless")]
KBM_LAYOUT_CHOICES = [("EN", "EN"), ("RU", "RU"), ("EN-RU", "EN-RU")]
KBM_LIGHTING_CHOICES = [("none", "None"), ("single", "Single Color"), ("rgb", "RGB")]
KBM_SWITCH_CHOICES = [
    ("membrane", "Membrane"),
    ("scissor", "Scissor"),
    ("semi-mechanical", "Semi-mechanical"),
    ("mechanical", "Mechanical"),
]
KBM_COLOR_CHOICES = [("white", "White"), ("black", "Black"), ("gray", "Gray")]
PRINTER_TYPE_CHOICES = [("Laser", "Laser"), ("Inkjet", "Siyohli"), ("LED", "LED")]
PAPER_SIZE_CHOICES = [("A4", "A4"), ("A3", "A3"), ("A4+A3", "A4 + A3")]


class Component(models.Model):
    """Barcha qismlar uchun umumiy asos."""
    name = models.CharField("Nomi", max_length=200)
    price = models.DecimalField("Narxi (USD)", max_digits=10, decimal_places=2, default=0)
    brand = models.CharField("Brend", max_length=30, blank=True, default="")

    class Meta:
        abstract = True
        ordering = ["id"]

    def __str__(self):
        return self.name


class CPU(Component):
    socket = models.CharField("Soket", max_length=20, choices=SOCKET_CHOICES, blank=True)
    cores = models.PositiveIntegerField("Total Cores", default=0)
    threads = models.PositiveIntegerField("Total Threads", default=0)
    max_turbo_ghz = models.DecimalField("Max Turbo Frequency (GHz)", max_digits=4,
                                        decimal_places=2, null=True, blank=True)
    cache = models.CharField("Cache", max_length=60, blank=True, default="")
    base_power_w = models.PositiveIntegerField("Processor Base Power (W)", default=0)
    max_turbo_power_w = models.PositiveIntegerField("Maximum Turbo Power (W)", null=True, blank=True)
    memory_types = models.CharField("Memory Types", max_length=120, choices=CPU_MEMORY_TYPE_CHOICES,
                                     blank=True, default="")
    memory_speed = models.CharField("Memory Speed", max_length=60, blank=True, default="")
    gpu_name = models.CharField("GPU Name", max_length=120, choices=CPU_GPU_CHOICES,
                                blank=True, default="")
    watt = models.PositiveIntegerField("Quvvat (W, eskisa)", default=0)

    class Meta(Component.Meta):
        verbose_name = "CPUs"
        verbose_name_plural = "CPUs"
        db_table = "builder_cpu"


class Motherboard(Component):
    socket = models.CharField("Soket", max_length=20, choices=SOCKET_CHOICES, blank=True)
    ram_type = models.CharField("RAM turi", max_length=10, choices=RAM_CHOICES, blank=True)
    form_factor = models.CharField("Form-faktor", max_length=20, choices=MB_FORM_CHOICES, blank=True)
    m2_slots = models.PositiveIntegerField("M.2 slotlari", default=1)

    class Meta(Component.Meta):
        verbose_name = "MB"
        verbose_name_plural = "MB"
        db_table = "builder_motherboard"


class RAM(Component):
    ram_type = models.CharField("RAM turi", max_length=10, choices=RAM_CHOICES, blank=True)
    capacity_gb = models.PositiveIntegerField("Umumiy hajmi (GB)", default=0)
    speed_mhz = models.PositiveIntegerField("Tezligi (MHz)", default=0)
    modules = models.PositiveSmallIntegerField("Modullar soni", choices=RAM_MODULE_CHOICES, default=1)
    form_factor = models.CharField("Form-faktor", max_length=8, choices=RAM_FORM_CHOICES, default="DIMM")
    cl = models.PositiveSmallIntegerField("CL (kechikish)", null=True, blank=True)
    radiator = models.BooleanField("Radiator", default=False)
    long_dimm = models.BooleanField("Long DIMM", default=False)
    rgb = models.BooleanField("RGB", default=False)
    note = models.CharField("Izoh", max_length=80, blank=True, default="")

    def build_name(self):
        """Nom xususiyatlardan yig'iladi: brend + hajm + tur + tezlik + ..."""
        per = self.capacity_gb // self.modules if self.modules and self.capacity_gb else self.capacity_gb
        kit = str(per) + 'x' + str(self.modules) if self.modules == 2 and per else ""
        parts = [
            self.brand,
            str(self.capacity_gb) + 'GB' if self.capacity_gb else "",
            self.ram_type,
            str(self.speed_mhz) + 'MHz' if self.speed_mhz else "",
            kit,
            'SODIMM' if self.form_factor == 'SODIMM' else "",
            'CL' + str(self.cl) if self.cl else "",
            'Radiator' if self.radiator else "",
            'LongDIMM' if self.long_dimm else "",
            'RGB' if self.rgb else "",
            self.note,
        ]
        return " ".join(p for p in parts if p).strip()[:200] or "RAM"

    def save(self, *args, **kwargs):
        self.name = self.build_name()
        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            kwargs["update_fields"] = list(set(update_fields) | {"name"})
        super().save(*args, **kwargs)

    class Meta(Component.Meta):
        verbose_name = "RAM"
        verbose_name_plural = "RAMs"
        db_table = "builder_ram"


class Cooler(Component):
    cooler_type = models.CharField("Turi", max_length=10, choices=COOLER_CHOICES, default="Air")
    sockets = models.CharField("Qo'llab-quvvatlagan soketlar", max_length=100,
                               help_text="Vergul bilan: LGA1700,AM4,AM5", default="")
    cooling_watt = models.PositiveIntegerField("Sovutish quvvati (W)", default=0)
    height_mm = models.PositiveIntegerField("Balandligi (mm)", default=0)

    class Meta(Component.Meta):
        verbose_name = "COOLER"
        verbose_name_plural = "COOLER"
        db_table = "builder_cooler"


class AIO(Component):
    """All-in-one (AIO) kompyuterlar."""
    screen_size = models.CharField("Ekran o'lchami", max_length=5, choices=AIO_SIZE_CHOICES, default='24"')
    resolution = models.CharField("Ekran razmeri", max_length=12,
                                  choices=AIO_RESOLUTION_CHOICES, default="1920x1080")
    screen_type = models.CharField("Ekran turi", max_length=10,
                                   choices=AIO_SCREEN_TYPE_CHOICES, default="flat")
    panel = models.CharField("Matritsa", max_length=5, choices=AIO_PANEL_CHOICES, default="IPS")
    chipset = models.CharField("Chipset", max_length=10, choices=AIO_CHIPSET_CHOICES, default="H610")
    webcam = models.BooleanField("Veb-kamera", default=True)
    wifi = models.BooleanField("WiFi", default=True)
    bluetooth = models.BooleanField("Bluetooth", default=False)
    m2_nvme = models.BooleanField("M.2 NVMe (eskisa)", default=False)
    m2_slots = models.PositiveIntegerField("NVME M.2 Slot soni",
                                           choices=AIO_SLOT_CHOICES, default=0)
    hdd_ports = models.PositiveIntegerField("HDD port soni",
                                            choices=AIO_SLOT_CHOICES, default=1)
    ram_type = models.CharField("RAM turi", max_length=10, choices=RAM_CHOICES, default="DDR4")
    ddr5 = models.BooleanField("DDR5 (eskisa)", default=False)
    color = models.CharField("Color", max_length=20, choices=AIO_COLOR_CHOICES, default="white")
    model_code = models.CharField("Model kodi", max_length=30, blank=True, default="")
    note = models.CharField("Izoh", max_length=100, blank=True, default="")

    @property
    def cpu_socket(self):
        """CPU soketi chipsetdan avtomatik aniqlanadi (yagona manba — chipset)."""
        return AIO_SOCKET_BY_CHIPSET.get(self.chipset, "")

    def build_name(self):
        """Qisqa nom: brend, ekran, chipset, RAM va rang (qolgani kartochkada pastda)."""
        panel = self.panel if self.panel and self.panel != "—" else ""
        parts = [
            self.brand,
            self.screen_size,
            panel,
            self.get_screen_type_display() if self.screen_type else "",
            self.chipset,
            self.ram_type,
            self.get_color_display() if self.color else "",
        ]
        return " ".join(p for p in parts if p).strip()[:200] or "AIO"

    def save(self, *args, **kwargs):
        self.name = self.build_name()
        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            kwargs["update_fields"] = list(set(update_fields) | {"name"})
        super().save(*args, **kwargs)

    class Meta(Component.Meta):
        verbose_name = "AIOs"
        verbose_name_plural = "AIOs"
        db_table = "builder_aio"


class GPU(Component):
    chipset = models.CharField("Chipset", max_length=20, default="NVIDIA")
    vram_gb = models.PositiveIntegerField("Videoxotira (GB)", default=0)
    watt = models.PositiveIntegerField("Quvvat (W)", default=0)
    length_mm = models.PositiveIntegerField("Uzunligi (mm)", default=0)

    class Meta(Component.Meta):
        verbose_name = "GPU"
        verbose_name_plural = "GPU"
        db_table = "builder_gpu"


class SSD(Component):
    interface = models.CharField("Interfeys", max_length=10,
                                 choices=SSD_INTERFACE_CHOICES, default="NVMe")
    capacity_gb = models.PositiveIntegerField("Hajmi (GB)", default=0)
    form_factor = models.CharField("Form-faktor", max_length=8, choices=SSD_FORM_CHOICES, default="M.2")
    speed_mbs = models.PositiveIntegerField("Tezligi (MB/s)", default=0)
    pcie_gen = models.CharField("PCIe avlodi", max_length=5, choices=SSD_PCIE_CHOICES,
                                blank=True, default="")
    model = models.CharField("Model", max_length=60, blank=True, default="")

    def build_name(self):
        """Nom xususiyatlardan yig'iladi (RAM/AIO kabi)."""
        cap = self.capacity_gb
        size = (str(cap // 1000) + 'TB') if cap and cap % 1000 == 0 and cap >= 1000 else (
            str(cap) + 'GB' if cap else "")
        form = dict(SSD_FORM_CHOICES).get(self.form_factor, self.form_factor)
        parts = [
            self.brand,
            self.model,
            size,
            self.interface,
            form,
        ]
        return " ".join(p for p in parts if p).strip()[:200] or "SSD"

    def save(self, *args, **kwargs):
        self.name = self.build_name()
        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            kwargs["update_fields"] = list(set(update_fields) | {"name"})
        super().save(*args, **kwargs)

    class Meta(Component.Meta):
        verbose_name = "SSD"
        verbose_name_plural = "SSDs"
        db_table = "builder_ssd"


class HDD(Component):
    form_factor = models.CharField("Form-faktor", max_length=10, choices=HDD_FORM_CHOICES, default='3.5"')
    capacity_gb = models.PositiveIntegerField("Hajmi (GB)", default=0)
    rpm = models.PositiveIntegerField("Aylanish tezligi (rpm)", default=0)

    class Meta(Component.Meta):
        verbose_name = "HDD"
        verbose_name_plural = "HDD"
        db_table = "builder_hdd"


class PSU(Component):
    watt = models.PositiveIntegerField("Quvvat (W)", default=0)
    efficiency = models.CharField("Sertifikat", max_length=20, choices=EFFICIENCY_CHOICES, default="None")
    modular = models.BooleanField("Modulli", default=False)

    class Meta(Component.Meta):
        verbose_name = "PSU"
        verbose_name_plural = "PSU"
        db_table = "builder_psu"


class Case(Component):
    case_type = models.CharField("Korpus turi", max_length=10, choices=CASE_TYPE_CHOICES, default="Mid")
    form_factors = models.CharField("Mos platalar", max_length=100,
                                    help_text="Vergul bilan: ATX,Micro-ATX,Mini-ITX", default="ATX")
    max_gpu_length = models.PositiveIntegerField("Maks. GPU uzunligi (mm)", default=0)
    max_cooler_height = models.PositiveIntegerField("Maks. sovutgich balandligi (mm)", default=0)

    class Meta(Component.Meta):
        verbose_name = "CASE"
        verbose_name_plural = "CASE"
        db_table = "builder_case"


class Monitor(Component):
    panel = models.CharField("Matritsa", max_length=10, choices=PANEL_CHOICES, blank=True)
    size_inch = models.PositiveIntegerField("Diagonali (dyuym)", default=0)
    refresh_hz = models.PositiveIntegerField("Yangilanish (Hz)", default=0)

    class Meta(Component.Meta):
        verbose_name = "MONITOR"
        verbose_name_plural = "MONITOR"
        db_table = "builder_monitor"


class Printer(Component):
    printer_type = models.CharField("Turi", max_length=10, choices=PRINTER_TYPE_CHOICES, default="Laser")
    connection = models.CharField("Ulanish", max_length=10, choices=CONNECTION_CHOICES, default="Wired")
    paper_size = models.CharField("Qog'oz o'lchami", max_length=10, choices=PAPER_SIZE_CHOICES, default="A4")
    color_print = models.BooleanField("Rangli chop etish", default=True)
    duplex = models.BooleanField("Ikki tomonlama", default=False)
    speed_ppm = models.PositiveIntegerField("Tezligi (ppm)", default=0)

    class Meta(Component.Meta):
        verbose_name = "PRINTER"
        verbose_name_plural = "PRINTER"
        db_table = "builder_printer"


class KeyboardMouse(Component):
    # legacy fields kept for DB compatibility
    model_code = models.CharField("Model", max_length=60, blank=True, default="")
    bundle_type = models.CharField("Turi/To'plam", max_length=20, blank=True, default="combo")

    connection = models.CharField("Ulanish", max_length=10, choices=KBM_CONNECTION_CHOICES, default="Wired")
    layout = models.CharField("Layout", max_length=10, choices=KBM_LAYOUT_CHOICES, default="EN-RU")
    lighting = models.CharField("Yoritish", max_length=15, choices=KBM_LIGHTING_CHOICES, default="none")
    switch_type = models.CharField("Switch turi", max_length=20, choices=KBM_SWITCH_CHOICES, default="membrane")
    color = models.CharField("Rangi", max_length=20, choices=KBM_COLOR_CHOICES, blank=True, default="")

    def build_name(self):
        parts = [
            (self.brand or "").strip(),
            (self.model_code or "").strip(),
            self.get_connection_display(),
            self.get_color_display(),
        ]
        out = []
        for p in parts:
            if p and p not in out:
                out.append(p)
        return " ".join(out).strip()[:200] or "KB&Ms"

    def save(self, *args, **kwargs):
        self.name = self.build_name()
        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            kwargs["update_fields"] = list(set(update_fields) | {"name"})
        super().save(*args, **kwargs)

    class Meta(Component.Meta):
        verbose_name = "KB&Ms"
        verbose_name_plural = "KB&Ms"
        db_table = "builder_keyboardmouse"


class Headset(Component):
    """Quloqchin / headset — ixtiyoriy aksessuar."""
    connection = models.CharField("Ulanish", max_length=10, choices=CONNECTION_CHOICES, default="Wired")
    surround = models.BooleanField("Ovoz atrofida (surround)", default=False)

    class Meta(Component.Meta):
        verbose_name = "HEADSET"
        verbose_name_plural = "HEADSET"
        db_table = "builder_headset"
