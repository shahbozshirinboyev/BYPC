from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from bypc.admin_site import admin_site
from .models import SavedBuild, Settings, Profile, Order, OrderItem


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
