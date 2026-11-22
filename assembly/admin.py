from django.contrib import admin

from bypc.admin_site import admin_site
from .models import (
    PCAssemblySettings, AIOAssemblySettings, PCCalculation, AIOCalculation,
)


@admin.register(PCAssemblySettings, site=admin_site)
class PCAssemblySettingsAdmin(admin.ModelAdmin):
    list_display = ("__str__", "markup_percent", "labor_cost_usd",
                    "warranty_months", "psu_headroom_percent", "updated_at")


@admin.register(AIOAssemblySettings, site=admin_site)
class AIOAssemblySettingsAdmin(admin.ModelAdmin):
    list_display = ("__str__", "markup_percent", "labor_cost_usd",
                    "warranty_months", "include_kbm", "updated_at")


class CalculationAdmin(admin.ModelAdmin):
    """Hisob tarixi faqat ko'rish uchun — yozuvlar kalkulyatordan qo'shiladi."""
    list_display = ("id", "user", "session_key", "subtotal_usd",
                    "markup_percent", "total_usd", "total_uzs", "created_at")
    list_filter = ("created_at",)
    search_fields = ("session_key", "user__username")
    readonly_fields = ("user", "session_key", "components", "subtotal_usd",
                       "markup_percent", "labor_cost_usd", "total_usd",
                       "total_uzs", "created_at")
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(PCCalculation, site=admin_site)
class PCCalculationAdmin(CalculationAdmin):
    pass


@admin.register(AIOCalculation, site=admin_site)
class AIOCalculationAdmin(CalculationAdmin):
    pass
