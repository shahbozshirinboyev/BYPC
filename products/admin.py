from django.contrib import admin

from bypc.admin_site import admin_site
from .models import (
    CPU, Motherboard, RAM, Cooler, AIO, GPU, SSD, HDD, PSU, Case,
    Monitor, Printer, KeyboardMouse, Headset,
)


class BaseAdmin(admin.ModelAdmin):
    search_fields = ("name", "brand")
    list_display = ("name", "brand", "price")
    list_per_page = 200
    list_max_show_all = 1000


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
