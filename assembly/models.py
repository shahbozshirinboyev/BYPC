"""Yig'ish (assembly) sozlamalari va hisob-kitob tarixi.

PC va AIO uchun alohida sozlama hamda hisob tarixi modellari.
"""
from django.conf import settings
from django.db import models


class AssemblySettings(models.Model):
    """Bitta rejim uchun umumiy yig'ish sozlamalari (abstract)."""

    markup_percent = models.DecimalField("Ustama, %", max_digits=5, decimal_places=2, default=10)
    labor_cost_usd = models.DecimalField("Ish haqi (USD)", max_digits=10, decimal_places=2, default=0)
    warranty_months = models.PositiveIntegerField("Kafolat (oy)", default=12)
    note = models.CharField("Izoh", max_length=200, blank=True, default="")
    updated_at = models.DateTimeField("Yangilangan", auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Singleton: har bir rejim uchun faqat bitta sozlama yozuvi bo'ladi.
        existing = self.__class__.objects.values_list("pk", flat=True).first()
        if existing:
            self.pk = existing
            kwargs.pop("force_insert", None)
        super().save(*args, **kwargs)


class PCAssemblySettings(AssemblySettings):
    psu_headroom_percent = models.PositiveIntegerField("PSU zaxirasi, %", default=30)
    include_windows = models.BooleanField("Windows narxga qo'shilsin", default=False)

    class Meta(AssemblySettings.Meta):
        verbose_name = "PC ASSEMBLY SETTINGS"
        verbose_name_plural = "PC ASSEMBLY SETTINGS"

    def __str__(self):
        return "PC yig'ish sozlamalari"


class AIOAssemblySettings(AssemblySettings):
    include_kbm = models.BooleanField("KB&M narxga qo'shilsin", default=True)
    default_ssd_gb = models.PositiveIntegerField("Standart SSD (GB)", default=512)

    class Meta(AssemblySettings.Meta):
        verbose_name = "AIO ASSEMBLY SETTINGS"
        verbose_name_plural = "AIO ASSEMBLY SETTINGS"

    def __str__(self):
        return "AIO yig'ish sozlamalari"


class CalculationBase(models.Model):
    """Bajarilgan hisob-kitob yozuvi (abstract)."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name="+")
    session_key = models.CharField("Sessiya", max_length=64, blank=True, default="", db_index=True)
    components = models.JSONField("Tanlangan qismlar", default=dict)
    subtotal_usd = models.DecimalField("Qismlar summasi (USD)", max_digits=12,
                                       decimal_places=2, default=0)
    markup_percent = models.DecimalField("Ustama, %", max_digits=5, decimal_places=2, default=0)
    labor_cost_usd = models.DecimalField("Ish haqi (USD)", max_digits=10, decimal_places=2, default=0)
    total_usd = models.DecimalField("Jami (USD)", max_digits=12, decimal_places=2, default=0)
    total_uzs = models.DecimalField("Jami (so'm)", max_digits=16, decimal_places=0, default=0)
    created_at = models.DateTimeField("Vaqti", auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class PCCalculation(CalculationBase):
    class Meta(CalculationBase.Meta):
        verbose_name = "PC CALCULATION"
        verbose_name_plural = "PC CALCULATIONS"

    def __str__(self):
        return f"PC hisob #{self.pk} — ${self.total_usd}"


class AIOCalculation(CalculationBase):
    class Meta(CalculationBase.Meta):
        verbose_name = "AIO CALCULATION"
        verbose_name_plural = "AIO CALCULATIONS"

    def __str__(self):
        return f"AIO hisob #{self.pk} — ${self.total_usd}"
