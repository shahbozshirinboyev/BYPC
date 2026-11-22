"""BYPC uchun yagona admin sayt va bo'limlar tartibi."""
from django.contrib.admin import AdminSite


APP_ORDER = ["products", "assembly", "builder", "auth"]

MODEL_ORDER = {
    "products": [
        "CPU", "AIO (Моноблоки)", "MB", "RAM", "COOLER", "GPU", "SSD", "HDD",
        "PSU", "CASE", "MONITOR", "PRINTER", "KB&M", "HEADSET",
    ],
    "assembly": [
        "PC ASSEMBLY SETTINGS", "PC CALCULATIONS",
        "AIO ASSEMBLY SETTINGS", "AIO CALCULATIONS",
    ],
    "builder": ["BUYURTMALAR", "PROFILLAR", "SAVED BUILDS", "SETTINGS"],
}


class BYPCAdminSite(AdminSite):
    site_header = "BYPC — boshqaruv paneli"
    site_title = "BYPC Admin"
    index_title = "Mahsulotlar va yig'ish sozlamalari"

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
            order = MODEL_ORDER.get(app["app_label"])
            if order:
                app["models"].sort(
                    key=lambda m: order.index(m["name"]) if m["name"] in order else 99
                )
        app_list.sort(
            key=lambda a: APP_ORDER.index(a["app_label"]) if a["app_label"] in APP_ORDER else 99
        )
        return app_list


admin_site = BYPCAdminSite(name="bypc_admin")
