from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from .models import (
    CPU, Motherboard, RAM, Cooler, AIO, GPU, SSD, HDD, PSU, Case,
    Monitor, Printer, KeyboardMouse, Headset, SavedBuild, Settings,
    Profile, Order, OrderItem,
)

ORDER = ["CPU", "AIO (Моноблоки)", "MB", "RAM", "COOLER", "GPU", "SSD", "HDD", "PSU",
         "CASE", "MONITOR", "PRINTER", "KB&M", "HEADSET", "BUYURTMALAR",
         "PROFIL", "SAVED BUILDS", "SETTINGS"]


class BYPCAdminSite(AdminSite):
    site_header = "BYPC — boshqaruv paneli"
    site_title = "BYPC Admin"
    index_title = "Qismlar katalogi"

    def has_permission(self, request):
        """Faqat Admin roli admin paneliga kira oladi."""
        if not request.user.is_active:
            return False
        if request.user.is_superuser:
            return True
        profile = getattr(request.user, "profile", None)
        return bool(profile and profile.role == "admin")

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        for app in app_list:
            if app["app_label"] == "builder":
                app["models"].sort(
                    key=lambda m: ORDER.index(m["name"]) if m["name"] in ORDER else 99
                )
        app_list.sort(key=lambda a: 0 if a['app_label'] == 'builder'
                      else (1 if a['app_label'] == 'auth' else 2))
        return app_list


admin_site = BYPCAdminSite(name="bypc_admin")


class BaseAdmin(admin.ModelAdmin):
    search_fields = ("name", "brand")
    list_display = ("name", "brand", "price")
    list_per_page = 25


@admin.register(CPU, site=admin_site)
class CPUAdmin(BaseAdmin):
    list_display = ("name", "brand", "socket", "cores", "watt", "price")
    list_filter = ("brand", "socket", "cores")


@admin.register(Motherboard, site=admin_site)
class MotherboardAdmin(BaseAdmin):
    list_display = ("name", "brand", "socket", "ram_type", "form_factor", "m2_slots", "price")
    list_filter = ("brand", "socket", "ram_type", "form_factor", "m2_slots")


@admin.register(RAM, site=admin_site)
class RAMAdmin(BaseAdmin):
    list_display = ("name", "brand", "ram_type", "capacity_gb", "speed_mhz", "price")
    list_filter = ("brand", "ram_type", "capacity_gb", "speed_mhz")


@admin.register(Cooler, site=admin_site)
class CoolerAdmin(BaseAdmin):
    list_display = ("name", "brand", "cooler_type", "cooling_watt", "height_mm", "price")
    list_filter = ("brand", "cooler_type", "cooling_watt", "sockets")


@admin.register(AIO, site=admin_site)
class AIOAdmin(BaseAdmin):
    list_display = ("name", "brand", "screen_size", "chipset", "panel", "ram_type", "m2_slots", "price")
    list_filter = ("brand", "screen_size", "chipset", "panel", "ram_type", "m2_slots", "curved")


@admin.register(GPU, site=admin_site)
class GPUAdmin(BaseAdmin):
    list_display = ("name", "brand", "chipset", "vram_gb", "watt", "length_mm", "price")
    list_filter = ("brand", "chipset", "vram_gb")


@admin.register(SSD, site=admin_site)
class SSDAdmin(BaseAdmin):
    list_display = ("name", "brand", "interface", "capacity_gb", "price")
    list_filter = ("brand", "interface", "capacity_gb")


@admin.register(HDD, site=admin_site)
class HDDAdmin(BaseAdmin):
    list_display = ("name", "brand", "form_factor", "capacity_gb", "rpm", "price")
    list_filter = ("brand", "form_factor", "capacity_gb", "rpm")


@admin.register(PSU, site=admin_site)
class PSUAdmin(BaseAdmin):
    list_display = ("name", "brand", "watt", "efficiency", "modular", "price")
    list_filter = ("brand", "efficiency", "watt", "modular")


@admin.register(Case, site=admin_site)
class CaseAdmin(BaseAdmin):
    list_display = ("name", "brand", "case_type", "form_factors", "max_gpu_length", "price")
    list_filter = ("brand", "case_type", "form_factors")


@admin.register(Monitor, site=admin_site)
class MonitorAdmin(BaseAdmin):
    list_display = ("name", "brand", "panel", "size_inch", "refresh_hz", "price")
    list_filter = ("brand", "panel", "size_inch", "refresh_hz")


@admin.register(KeyboardMouse, site=admin_site)
class KeyboardMouseAdmin(BaseAdmin):
    list_display = ("name", "brand", "connection", "layout", "price")
    list_filter = ("brand", "connection", "layout")


@admin.register(Headset, site=admin_site)
class HeadsetAdmin(BaseAdmin):
    list_display = ("name", "brand", "connection", "surround", "price")
    list_filter = ("brand", "connection", "surround")


@admin.register(Printer, site=admin_site)
class PrinterAdmin(BaseAdmin):
    list_display = ("name", "brand", "printer_type", "connection", "paper_size", "color_print", "price")
    list_filter = ("brand", "printer_type", "connection", "paper_size", "color_print", "duplex")


@admin.register(Profile, site=admin_site)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email", "phone")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("kind", "name", "quantity", "unit_price_usd", "line_total_display")
    readonly_fields = ("line_total_display",)

    @admin.display(description="Qator jami (USD)")
    def line_total_display(self, obj):
        return f"${obj.line_total_usd:.2f}"


@admin.register(Order, site=admin_site)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("display_order_number", "client_name", "client_phone", "seller",
                    "total", "status", "payment_status", "payment_type", "created_at")
    list_filter = ("status", "payment_status", "payment_type", "delivery_type",
                   "created_at", "seller")
    search_fields = ("order_number", "client_name", "client_phone", "note")
    readonly_fields = ("order_number", "created_at", "updated_at", "delivered_at")
    inlines = [OrderItemInline]
    ordering = ("-created_at",)


admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)


@admin.register(Settings, site=admin_site)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("markup_percent", "usd_to_uzs")


@admin.register(SavedBuild, site=admin_site)
class SavedBuildAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "total", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "owner")
    readonly_fields = ("created_at",)
