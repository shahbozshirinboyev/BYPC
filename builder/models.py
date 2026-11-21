from django.conf import settings
from django.db import models


SOCKET_CHOICES = [("LGA1700", "LGA1700"), ("AM4", "AM4"), ("AM5", "AM5")]
RAM_CHOICES = [("DDR3", "DDR3"), ("DDR4", "DDR4"), ("DDR5", "DDR5")]
MB_FORM_CHOICES = [("ATX", "ATX"), ("Micro-ATX", "Micro-ATX"), ("Mini-ITX", "Mini-ITX")]
SSD_INTERFACE_CHOICES = [("NVMe", "NVMe"), ("SATA", "SATA")]
HDD_FORM_CHOICES = [('3.5"', '3.5"'), ('2.5"', '2.5"')]
EFFICIENCY_CHOICES = [("None", "No certification"), ("80+ Bronze", "80+ Bronze"),
                      ("80+ Gold", "80+ Gold"), ("80+ Platinum", "80+ Platinum")]
COOLER_CHOICES = [("Air", "Havo"), ("Liquid", "Suvli")]
AIO_CHIPSET_CHOICES = [("H61", "H61"), ("H81", "H81"), ("H410", "H410"),
                       ("H510", "H510"), ("H610", "H610"), ("Other", "Boshqa")]
AIO_SIZE_CHOICES = [('24"', '24"'), ('27"', '27"'), ('32"', '32"')]
AIO_PANEL_CHOICES = [("IPS", "IPS"), ("VA", "VA"), ("TN", "TN"), ("—", "—")]
CASE_TYPE_CHOICES = [("Mini", "Mini-tower"), ("Mid", "Mid-tower"), ("Full", "Full-tower")]
PANEL_CHOICES = [("IPS", "IPS"), ("VA", "VA"), ("TN", "TN"), ("OLED", "OLED")]
CONNECTION_CHOICES = [("Wired", "Simli"), ("Wireless", "Simsiz")]
PRINTER_TYPE_CHOICES = [("Laser", "Laser"), ("Inkjet", "Siyohli"), ("LED", "LED")]
PAPER_SIZE_CHOICES = [("A4", "A4"), ("A3", "A3"), ("A4+A3", "A4 + A3")]
ROLE_CHOICES = [("admin", "Admin"), ("seller", "Sotuvchi"), ("guest", "Mehmon")]
ORDER_STATUS_CHOICES = [
    ("NEW", "Yangi"), ("AGREED", "Kelishuvda"), ("QUEUED", "Navbatda"),
    ("IN_PROGRESS", "Tayyorlanmoqda"), ("READY", "Tayyor"),
    ("SHIPPING", "Yo'lda"), ("DELIVERED", "Yetkazildi"),
    ("ON_HOLD", "To'xtatildi"), ("CANCELLED", "Bekor qilindi"),
]
# Yetkazish turiga qarab oqim farqlanadi: olib ketishda "Yo'lda" bosqichi yo'q.
ORDER_FLOW_DELIVERY = ["NEW", "AGREED", "QUEUED", "IN_PROGRESS", "READY", "SHIPPING", "DELIVERED"]
ORDER_FLOW_PICKUP = ["NEW", "AGREED", "QUEUED", "IN_PROGRESS", "READY", "DELIVERED"]
DELIVERY_STATUS_FLOWS = {
    "DELIVERY": ORDER_FLOW_DELIVERY,
    "POST": ORDER_FLOW_DELIVERY,
    "PICKUP": ORDER_FLOW_PICKUP,
}
ORDER_FLOW = ORDER_FLOW_DELIVERY  # eski kod uchun moslik
ORDER_EXTRA_STATUSES = ["ON_HOLD", "CANCELLED"]
DELIVERY_STATUS_LABELS = {
    "DELIVERY": {"SHIPPING": "Yo'lda", "DELIVERED": "Yetkazildi"},
    "POST": {"SHIPPING": "Jo'natildi", "DELIVERED": "Qabul qilib oldi"},
    "PICKUP": {"DELIVERED": "Olib ketildi"},
}
PAYMENT_STATUS_CHOICES = [
    ("UNPAID", "To'lanmagan"), ("ON_DELIVERY", "Yetkazilganda to'lanadi"),
    ("ON_PICKUP", "Olib ketishda to'lanadi"), ("PARTIAL", "Qisman to'langan"),
    ("PAID", "To'langan"),
]
PAYMENT_TYPE_CHOICES = [
    ("CASH", "Naqd"), ("CARD", "Karta"), ("TRANSFER", "Bank orqali"),
    ("CASH_CARD", "Aralash"),
]
DELIVERY_TYPE_CHOICES = [
    ("PICKUP", "Olib ketadi"), ("DELIVERY", "Olib borish"), ("POST", "Pochta orqali"),
]


class Profile(models.Model):
    """Foydalanuvchi turi va huquqlari."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="profile")
    role = models.CharField("Rol", max_length=10, choices=ROLE_CHOICES, default="guest")
    phone = models.CharField("Telefon", max_length=30, blank=True, default="")

    class Meta:
        verbose_name = "PROFIL"
        verbose_name_plural = "PROFILLAR"

    def __str__(self):
        return f"{self.user.username} — {self.get_role_display()}"

    @property
    def is_admin(self):
        return self.role == "admin" or self.user.is_superuser

    @property
    def is_seller(self):
        return self.role == "seller"


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


class AIO(Component):
    """All-in-one monoblock kompyuterlar."""
    screen_size = models.CharField("Ekran o'lchami", max_length=5, choices=AIO_SIZE_CHOICES, default='24"')
    panel = models.CharField("Matritsa", max_length=5, choices=AIO_PANEL_CHOICES, default="IPS")
    chipset = models.CharField("Chipset", max_length=10, choices=AIO_CHIPSET_CHOICES, default="H610")
    curved = models.BooleanField("Egri ekran", default=False)
    webcam = models.BooleanField("Veb-kamera", default=True)
    wifi = models.BooleanField("WiFi", default=True)
    m2_nvme = models.BooleanField("M.2 NVMe (eskisa)", default=False)
    m2_slots = models.PositiveIntegerField("M.2 NVMe slotlari", default=0)
    ram_type = models.CharField("RAM turi", max_length=10, choices=RAM_CHOICES, default="DDR4")
    ddr5 = models.BooleanField("DDR5 (eskisa)", default=False)
    color = models.CharField("Rang", max_length=20, default="white")
    model_code = models.CharField("Model kodi", max_length=30, blank=True, default="")
    note = models.CharField("Izoh", max_length=100, blank=True, default="")

    class Meta(Component.Meta):
        verbose_name = "AIO (monoblock)"
        verbose_name_plural = "AIO (Моноблоки)"


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
    """Foydalanuvchi saqlagan yig'malar (session yoki user orqali bog'lanadi)."""
    name = models.CharField("Nomi", max_length=120)
    owner = models.CharField("Egasi (session)", max_length=64, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             null=True, blank=True, related_name="builds")
    data = models.JSONField("Tanlov", default=dict)
    total = models.DecimalField("Jami (USD)", max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField("Vaqti", auto_now_add=True)

    class Meta:
        verbose_name = "SAVED BUILD"
        verbose_name_plural = "SAVED BUILDS"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — ${self.total}"


class Order(models.Model):
    """Sotuvchi tomonidan klient uchun yaratilgan buyurtma."""
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name="orders")
    order_number = models.CharField("Buyurtma raqami", max_length=24,
                                    blank=True, null=True, unique=True)
    client_name = models.CharField("Klient ismi", max_length=120)
    client_phone = models.CharField("Telefon", max_length=30, blank=True, default="")
    note = models.TextField("Izoh", blank=True, default="")
    items = models.JSONField("Qismlar (eski ko'rinish)", default=list)
    total = models.DecimalField("Jami (USD)", max_digits=12, decimal_places=2, default=0)
    total_uzs = models.DecimalField("Jami (so'm)", max_digits=16, decimal_places=0, default=0)
    partial_amount = models.DecimalField("Qisman to'lov (USD)", max_digits=12,
                                         decimal_places=2, default=0)
    status = models.CharField("Holat", max_length=12, choices=ORDER_STATUS_CHOICES,
                              default="NEW")
    payment_status = models.CharField("To'lov holati", max_length=12,
                                      choices=PAYMENT_STATUS_CHOICES, default="UNPAID")
    payment_type = models.CharField("To'lov turi", max_length=12,
                                    choices=PAYMENT_TYPE_CHOICES, default="CASH")
    delivery_type = models.CharField("Yetkazish", max_length=10,
                                     choices=DELIVERY_TYPE_CHOICES, default="PICKUP")
    delivery_date = models.DateField("Yetkazish sanasi", null=True, blank=True)
    delivery_time = models.CharField("Yetkazish vaqti", max_length=10, blank=True, default="")
    region = models.CharField("Viloyat", max_length=80, blank=True, default="")
    district = models.CharField("Tuman", max_length=80, blank=True, default="")
    city = models.CharField("Shahar", max_length=80, blank=True, default="")
    landmark = models.CharField("Mo'ljal", max_length=200, blank=True, default="")
    cash_amount = models.DecimalField("Naqd (USD)", max_digits=12, decimal_places=2, default=0)
    card_amount = models.DecimalField("Karta (USD)", max_digits=12, decimal_places=2, default=0)
    transfer_amount = models.DecimalField("Bank (USD)", max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField("Vaqti", auto_now_add=True)
    updated_at = models.DateTimeField("Yangilangan", auto_now=True)
    delivered_at = models.DateTimeField("Yetkazilgan vaqti", null=True, blank=True)

    class Meta:
        verbose_name = "BUYURTMA"
        verbose_name_plural = "BUYURTMALAR"
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.id} — {self.client_name} (${self.total})"

    @property
    def display_order_number(self):
        return self.order_number or f"ORDER#{self.pk}"

    @property
    def remaining_amount(self):
        """Qisman to'lov hisobga olingan qoldiq (USD)."""
        return max(0, float(self.total) - float(self.partial_amount))

    @property
    def is_completed(self):
        """Yakunlangan deb faqat yetkazilgan + to'langan buyurtma hisoblanadi."""
        return self.status == "DELIVERED" and self.payment_status == "PAID"

    @property
    def status_display(self):
        """Yetkazish turiga mos holat nomi (masalan, PICKUP uchun 'Olib ketildi')."""
        return self.status_label(self.status, self.delivery_type)

    @property
    def address(self):
        parts = [self.region, self.district, self.city, self.landmark]
        return ", ".join(p for p in parts if p)

    @property
    def mixed_total(self):
        return self.cash_amount + self.card_amount + self.transfer_amount

    @classmethod
    def status_flow(cls, delivery_type=None):
        return list(DELIVERY_STATUS_FLOWS.get(delivery_type, ORDER_FLOW_DELIVERY))

    @classmethod
    def status_label(cls, status, delivery_type=None):
        custom = DELIVERY_STATUS_LABELS.get(delivery_type, {})
        return custom.get(status, dict(ORDER_STATUS_CHOICES).get(status, status))

    @classmethod
    def status_choices_for_delivery(cls, delivery_type):
        """Oqim + umumiy holatlar, yetkazish turiga mos nomlar bilan."""
        statuses = cls.status_flow(delivery_type) + ORDER_EXTRA_STATUSES
        return [(s, cls.status_label(s, delivery_type)) for s in statuses]

    @classmethod
    def allowed_next_statuses(cls, current, delivery_type=None):
        """Joriy holatdan oldinga faqat ruxsat etilgan holatlar."""
        flow = cls.status_flow(delivery_type)
        if current in flow:
            return flow[flow.index(current) + 1:]
        return list(ORDER_EXTRA_STATUSES)


class OrderItem(models.Model):
    """Buyurtma qatori: miqdor va narx alohida saqlanadi."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lines")
    kind = models.CharField("Guruhi", max_length=20, blank=True, default="")
    name = models.CharField("Nomi", max_length=200)
    quantity = models.PositiveIntegerField("Soni", default=1)
    unit_price_usd = models.DecimalField("Narxi (USD)", max_digits=12,
                                         decimal_places=2, default=0)

    class Meta:
        verbose_name = "BUYURTMA QATORI"
        verbose_name_plural = "BUYURTMA QATORLARI"
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} × {self.quantity}"

    @property
    def line_total_usd(self):
        return float(self.unit_price_usd) * self.quantity
