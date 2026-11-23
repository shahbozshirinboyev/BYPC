from .views import role_of


def _cart_count(request):
    """Savatdagi mahsulotlar soni (miqdorlar yig'indisi)."""
    total = 0
    for line in request.session.get("cart", []) if hasattr(request, "session") else []:
        try:
            total += max(1, int(line.get("qty", 1) or 1))
        except (TypeError, ValueError, AttributeError):
            total += 1
    return total


def common(request):
    """Barcha templatlar uchun faol menyu va foydalanuvchi turi."""
    path = request.path
    active = "home"
    if path.startswith("/pc-assembly") or path.startswith("/pc_assembly"):
        active = "pc"
    elif path.startswith("/aio-assembly") or path.startswith("/aio_assembly"):
        active = "aio"
    elif path.startswith("/monitors"):
        active = "monitors"
    elif path.startswith("/printers"):
        active = "printers"
    elif path.startswith("/profile") or path.startswith("/login") or path.startswith("/register"):
        active = "profile"
    elif path.startswith("/cart"):
        active = "cart"
    elif path.startswith("/orders") or path.startswith("/seller"):
        active = "orders"

    return {
        "active_menu": active,
        "role": role_of(request.user),
        "cart_count": _cart_count(request),
    }
