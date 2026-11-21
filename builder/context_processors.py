from .views import role_of


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
    elif path.startswith("/seller"):
        active = "seller"

    return {
        "active_menu": active,
        "role": role_of(request.user),
    }
