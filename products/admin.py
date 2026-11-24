import json

from django.contrib import admin
from django.utils.html import format_html

from bypc.admin_site import admin_site
from .models import (
    CPU, Motherboard, RAM, Cooler, AIO, GPU, SSD, HDD, PSU, Case,
    Monitor, Printer, KeyboardMouse, Headset, AIO_SOCKET_BY_CHIPSET,
)


class BaseAdmin(admin.ModelAdmin):
    search_fields = ("name", "brand")
    list_display = ("name", "brand", "price")
    list_per_page = 200
    list_max_show_all = 1000

    class Media:
        css = {"all": ("products/css/admin_form.css",)}


@admin.register(CPU, site=admin_site)
class CPUAdmin(BaseAdmin):
    list_display = ("name_display", "socket", "cores", "threads", "max_turbo_ghz",
                    "base_power_w", "max_turbo_power_w", "price")
    list_filter = ("socket", "cores", "threads")
    search_fields = ("name",)
    exclude = ("watt", "brand")
    fieldsets = (
        ("Asosiy", {"fields": ("name", "price")}),
        ("CPU", {"fields": ("socket", "cores", "threads", "max_turbo_ghz", "cache",
                            "base_power_w", "max_turbo_power_w")}),
        ("Platforma", {"fields": ("memory_types", "memory_speed", "gpu_name")}),
    )

    @admin.display(description="Name", ordering="name")
    def name_display(self, obj):
        return obj.name

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "name":
            kwargs["label"] = "Name"
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Motherboard, site=admin_site)
class MotherboardAdmin(BaseAdmin):
    list_display = ("name", "brand", "socket", "ram_type", "form_factor", "m2_slots", "price")
    list_filter = ("brand", "socket", "ram_type", "form_factor", "m2_slots")


@admin.register(RAM, site=admin_site)
class RAMAdmin(BaseAdmin):
    # Nom xususiyatlardan avtomatik yig'iladi (AIO kabi).
    # CL, Long DIMM va Izoh formada ko'rsatilmaydi.
    exclude = ("name", "cl", "long_dimm", "note")
    list_display = ("name_display", "brand", "ram_type", "capacity_gb", "speed_mhz",
                    "modules", "form_factor", "price")
    list_filter = ("brand", "ram_type", "capacity_gb", "speed_mhz", "modules",
                   "form_factor", "rgb", "radiator")
    fieldsets = (
        ("Asosiy", {"fields": ("brand", "ram_type", "price")}),
        ("Xususiyatlar", {"fields": ("capacity_gb", "modules", "speed_mhz", "form_factor")}),
        ("Tashqi ko‘rinish", {"fields": ("radiator", "rgb")}),
    )

    @admin.display(description="Name", ordering="name")
    def name_display(self, obj):
        return obj.name


@admin.register(Cooler, site=admin_site)
class CoolerAdmin(BaseAdmin):
    list_display = ("name", "brand", "cooler_type", "cooling_watt", "height_mm", "price")
    list_filter = ("brand", "cooler_type", "cooling_watt", "sockets")


@admin.register(AIO, site=admin_site)
class AIOAdmin(BaseAdmin):
    list_display = ("name", "brand", "screen_size", "resolution", "panel", "screen_type",
                    "chipset", "ram_type", "m2_slots", "hdd_ports", "price")
    list_filter = ("brand", "screen_size", "resolution", "panel", "screen_type",
                   "chipset", "ram_type", "m2_slots", "hdd_ports")
    # Nom avtomatik yig'iladi; eski (eskisa) va kiritilmaydigan maydonlar formada ko'rsatilmaydi.
    exclude = ("name", "m2_nvme", "ddr5", "model_code", "note")
    readonly_fields = ("socket_display",)
    fieldsets = (
        ("Asosiy", {"fields": ("brand", "color", "price")}),
        ("Ekran", {"fields": ("screen_size", "resolution", "panel", "screen_type")}),
        ("Platforma", {"fields": ("chipset", "socket_display", "ram_type", "m2_slots", "hdd_ports")}),
        ("Qo'shimcha", {"fields": ("wifi", "bluetooth", "webcam")}),
    )

    @admin.display(description="CPU socket")
    def socket_display(self, obj):
        """Socket chipsetga qarab avtomatik ko'rsatiladi (tanlanishi bilan jonli yangilanadi)."""
        socket = (obj.cpu_socket if obj else "") or "—"
        return format_html(
            '<span class="aio-socket" data-map="{}">{}</span>',
            json.dumps(AIO_SOCKET_BY_CHIPSET),
            socket,
        )

    class Media:
        js = ("products/js/aio_socket.js",)


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
