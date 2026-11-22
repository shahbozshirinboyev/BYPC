from django.conf import settings
from django.db import models


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
