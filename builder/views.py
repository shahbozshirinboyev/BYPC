import csv
import json
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from products.models import (
    CPU, Motherboard, RAM, Cooler, AIO, GPU, SSD, HDD, PSU, Case,
    Monitor, Printer, KeyboardMouse, Headset,
)
from assembly.models import (
    PCAssemblySettings, AIOAssemblySettings, PCCalculation, AIOCalculation,
)
from .models import (
    SavedBuild, Settings, Profile, Order, OrderItem, ROLE_CHOICES, ORDER_FLOW,
)
from .templatetags.bypc_tags import phone_format

FIELDS = {
    "cpu": (CPU, "id name price brand socket cores threads max_turbo_ghz cache base_power_w max_turbo_power_w memory_types memory_speed gpu_name watt"),
    "mb": (Motherboard, "id name price brand socket ram_type form_factor m2_slots"),
    "ram": (RAM, "id name price brand ram_type capacity_gb speed_mhz modules form_factor cl radiator long_dimm rgb note"),
    "cool": (Cooler, "id name price brand cooler_type sockets cooling_watt height_mm"),
    "aio": (AIO, "id name price brand screen_size resolution screen_type panel chipset ram_type m2_slots hdd_ports webcam wifi bluetooth color model_code note"),
    "gpu": (GPU, "id name price brand chipset vram_gb watt length_mm"),
    "ssd": (SSD, "id name price brand interface capacity_gb form_factor speed_mbs pcie_gen model"),
    "hdd": (HDD, "id name price brand form_factor capacity_gb rpm"),
    "psu": (PSU, "id name price brand watt efficiency modular"),
    "case": (Case, "id name price brand case_type form_factors max_gpu_length max_cooler_height"),
    "mon": (Monitor, "id name price brand panel size_inch refresh_hz"),
    "printer": (Printer, "id name price brand printer_type connection paper_size color_print duplex speed_ppm"),
    "kbm": (KeyboardMouse, "id name price brand connection layout lighting switch_type color"),
    "head": (Headset, "id name price brand connection surround"),
}




def role_of(user):
    """Foydalanuvchi turi: admin / sotuvchi / mehmon."""
    if not user or not user.is_authenticated:
        return "guest"
    if user.is_superuser:
        return "admin"
    profile = getattr(user, "profile", None)
    if profile and profile.role == "admin":
        return "admin"
    if profile and profile.role == "seller":
        return "seller"
    return "guest"


def _settings():
    conf = Settings.objects.first()
    return conf or Settings.objects.create()


def _assembly_conf(mode):
    """PC yoki AIO uchun yig'ish sozlamalarini qaytaradi (yo'q bo'lsa yaratadi)."""
    model = AIOAssemblySettings if mode == "aio" else PCAssemblySettings
    conf = model.objects.first()
    return conf or model.objects.create()


def _selected_components(data):
    """Kalkulyator tanlovini (kind -> id) bazadagi mahsulotlarga aylantiradi."""
    selected = (data or {}).get("s", {}) if isinstance(data, dict) else {}
    items, subtotal = [], Decimal("0")
    for kind, item_id in selected.items():
        model = FIELDS.get(kind, (None,))[0]
        if not model or item_id is None:
            continue
        obj = model.objects.filter(pk=item_id).first()
        if not obj:
            continue
        price = Decimal(str(obj.price))
        items.append({"kind": kind, "id": obj.pk, "name": obj.name,
                      "price": float(price)})
        subtotal += price
    return items, subtotal


def _record_calculation(request, mode, data):
    """Bajarilgan hisob-kitobni PC yoki AIO tarixiga yozadi."""
    mode = "aio" if mode == "aio" else "pc"
    items, subtotal = _selected_components(data)
    if not items:
        return None
    conf = _assembly_conf(mode)
    markup = Decimal(str(conf.markup_percent or 0))
    labor = Decimal(str(conf.labor_cost_usd or 0))
    total = (subtotal * (1 + markup / 100) + labor).quantize(Decimal("0.01"))
    rate = Decimal(str(_settings().usd_to_uzs or 0))
    total_uzs = int((total * rate).quantize(Decimal("1"))) if rate > 0 else 0
    model = AIOCalculation if mode == "aio" else PCCalculation
    return model.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=_owner(request),
        components={"items": items},
        subtotal_usd=subtotal,
        markup_percent=markup,
        labor_cost_usd=labor,
        total_usd=total,
        total_uzs=total_uzs,
    )


def _serialize(model, fields):
    items = list(model.objects.values(*fields.split()))
    for item in items:
        item["price"] = float(item["price"])
    return items


def _render_builder(request, mode):
    """Kalkulyatorni tanlangan rejimda ko'rsatadi (pc / aio)."""
    conf = _settings()
    assembly_conf = _assembly_conf(mode)
    catalog = {key: _serialize(model, fields) for key, (model, fields) in FIELDS.items()}
    return render(request, "builder/index.html", {
        "catalog": catalog,
        "rate": str(conf.usd_to_uzs),
        "markup": str(assembly_conf.markup_percent),
        "labor": str(assembly_conf.labor_cost_usd or 0),
        "mode": mode,
        "mode_label": "AIO assembly" if mode == "aio" else "PC assembly",
        "role": role_of(request.user),
    })


def home(request):
    """Kirish (landing) sahifasi."""
    models = (CPU, Motherboard, RAM, Cooler, AIO, GPU, SSD, HDD, PSU, Case,
              Monitor, Printer, KeyboardMouse, Headset)
    return render(request, "builder/home.html", {
        "role": role_of(request.user),
        "total_parts": sum(model.objects.count() for model in models),
        "aio_count": AIO.objects.count(),
    })


def pc_assembly(request):
    return _render_builder(request, "pc")


def aio_assembly(request):
    return _render_builder(request, "aio")


def monitors(request):
    return render(request, "builder/catalog.html", {
        "title": "Monitorlar",
        "subtitle": "Monitor katalogi — matritsa, diagonal va yangilanish tezligi bo'yicha tanlang",
        "items": _serialize(Monitor, FIELDS["mon"][1]),
        "key": "mon",
        "role": role_of(request.user),
    })


def printers(request):
    return render(request, "builder/catalog.html", {
        "title": "Printerlar",
        "subtitle": "Printer katalogi — turi, ulanish va qog'oz o'lchami bo'yicha tanlang",
        "items": _serialize(Printer, FIELDS["printer"][1]),
        "key": "printer",
        "role": role_of(request.user),
    })


# --- Autentifikatsiya va profil ------------------------------------------------

def register(request):
    if request.user.is_authenticated:
        return redirect("profile")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user, defaults={"role": "guest"})
            login(request, user)
            messages.success(request, "Ro'yxatdan o'tdingiz. Xush kelibsiz!")
            return redirect("profile")
    else:
        form = UserCreationForm()
    return render(request, "builder/auth.html", {
        "form": form, "kind": "register", "title": "Ro'yxatdan o'tish",
        "role": role_of(request.user),
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect("profile")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("profile")
        messages.error(request, "Login yoki parol noto'g'ri.")
    else:
        form = AuthenticationForm()
    return render(request, "builder/auth.html", {
        "form": form, "kind": "login", "title": "Kirish",
        "role": role_of(request.user),
    })


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Siz chiqdingiz.")
    return redirect("home")


def _saved_qs(request):
    if request.user.is_authenticated:
        return SavedBuild.objects.filter(user=request.user)
    return SavedBuild.objects.filter(owner=_owner(request), user__isnull=True)


@login_required
def profile(request):
    role = role_of(request.user)
    return render(request, "builder/profile.html", {
        "role": role,
        "role_label": dict(ROLE_CHOICES).get(
            getattr(getattr(request.user, "profile", None), "role", "guest"), "Mehmon"),
        "builds": list(_saved_qs(request).values("id", "name", "total", "created_at")),
        "orders": list(Order.objects.filter(seller=request.user).values(
            "id", "order_number", "client_name", "client_phone", "total", "status",
            "payment_status", "created_at")) if role in ("seller", "admin") else [],
    })


# --- Sotuvchi: savat va buyurtmalar --------------------------------------------

def _money(value, default=Decimal("0")):
    """'1 250,5' kabi qiymatni Decimal ga o'tkazadi."""
    try:
        return Decimal(str(value).replace(",", ".").replace(" ", "").strip())
    except (InvalidOperation, AttributeError, ValueError):
        return default


def _orders_for_user(request):
    """Admin hamma buyurtmalarni, sotuvchi faqat o'zinikini ko'radi."""
    qs = Order.objects.select_related("seller").prefetch_related("lines")
    if role_of(request.user) == "admin":
        return qs
    return qs.filter(seller=request.user)


def _validate_status_transition(order, target):
    """Holat oqimi yetkazish turiga bog'liq; to'lanmagan buyurtma navbatga kirmaydi."""
    valid = dict(Order._meta.get_field("status").choices)
    if target not in valid:
        return False, "Noto'g'ri holat."
    if target == "CANCELLED":
        return True, None
    if target == "QUEUED" and order.status == "AGREED" and order.payment_status == "UNPAID":
        return False, "To'lov holati 'To'lanmagan' bo'lsa, navbatga o'tkazib bo'lmaydi."
    flow = Order.status_flow(order.delivery_type)
    if order.status in flow and target in flow:
        if flow.index(target) < flow.index(order.status):
            return False, "Holatni orqaga qaytarib bo'lmaydi."
    return True, None


def _can_set_status(role, user, order, target):
    """Sotuvchi faqat kelishuv/navbat va bekor qilishni belgilay oladi."""
    if role == "admin":
        return True
    if order.seller_id != user.id:
        return False
    return target in {order.status, "NEW", "AGREED", "QUEUED", "CANCELLED"}


def _cart_line_spec(kind, item):
    if kind == "kbm":
        parts = [
            (getattr(item, "layout", "") or "").replace("/", "-"),
            ("Switch: " + item.get_switch_type_display()) if getattr(item, "switch_type", "") else "",
            ("Light: " + item.get_lighting_display()) if getattr(item, "lighting", "") else "",
        ]
        return " · ".join(p for p in parts if p)
    return ""


def _cart_with_live_prices(cart):
    """Savat narxlarini sessionga emas, bazaga qarab qayta hisoblaydi."""
    result, errors = [], []
    for line in cart:
        key = line.get("kind", "")
        model = FIELDS[key][0] if key in FIELDS else None
        item = model.objects.filter(pk=line.get("id")).first() if model else None
        if not item:
            errors.append(f"{line.get('name', 'Qism')} katalogda topilmadi.")
            continue
        try:
            qty = max(1, min(99, int(line.get("qty", 1) or 1)))
        except (TypeError, ValueError):
            qty = 1
        price = Decimal(str(item.price))
        result.append({"kind": key, "id": item.id, "name": item.name,
                       "price": float(price), "qty": qty,
                       "line_total": float(price * qty),
                       "spec": _cart_line_spec(key, item)})
    return result, errors


@transaction.atomic
def _create_order(request, cart, post):
    """Buyurtmani yaratadi: jami miqdorlar serverda qayta hisoblanadi."""
    client = post.get("client", "").strip()
    if not client:
        raise ValueError("Klient ismini kiriting.")
    priced, errors = _cart_with_live_prices(cart)
    if errors:
        raise ValueError(" | ".join(errors))
    if not priced:
        raise ValueError("Savat bo'sh.")

    total = sum(Decimal(str(i["price"])) * i["qty"] for i in priced)
    conf = _settings()
    rate = Decimal(str(conf.usd_to_uzs or 0))
    total_uzs = int((total * rate).quantize(Decimal("1"))) if rate > 0 else 0

    payment = post.get("payment_status", "UNPAID")
    if payment not in dict(Order._meta.get_field("payment_status").choices):
        payment = "UNPAID"
    partial = _money(post.get("partial_amount"), Decimal("0")) if payment == "PARTIAL" else Decimal("0")
    partial = max(Decimal("0"), min(partial, total))

    payment_type = post.get("payment_type", "CASH")
    if payment_type not in dict(Order._meta.get_field("payment_type").choices):
        payment_type = "CASH"
    mixed = [Decimal("0")] * 3
    if payment_type == "CASH_CARD" and payment in ("PAID", "PARTIAL"):
        mixed = [_money(post.get("cash_amount"), Decimal("0")),
                 _money(post.get("card_amount"), Decimal("0")),
                 _money(post.get("transfer_amount"), Decimal("0"))]
        expected = total if payment == "PAID" else partial
        if abs(sum(mixed) - expected) > Decimal("0.01"):
            raise ValueError(f"Aralash to'lov yig'indisi ${expected} bo'lishi kerak.")

    delivery = post.get("delivery_type", "PICKUP")
    if delivery not in dict(Order._meta.get_field("delivery_type").choices):
        delivery = "PICKUP"
    raw_date = post.get("delivery_date", "").strip()
    delivery_date = None
    if raw_date:
        try:
            delivery_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
        except ValueError:
            delivery_date = None

    order = Order.objects.create(
        seller=request.user,
        client_name=client[:120],
        client_phone=post.get("phone", "")[:30],
        note=post.get("note", "")[:2000],
        items=[{k: i[k] for k in ("kind", "id", "name", "price", "qty")} for i in priced],
        total=total, total_uzs=total_uzs, partial_amount=partial,
        payment_status=payment, payment_type=payment_type,
        cash_amount=mixed[0], card_amount=mixed[1], transfer_amount=mixed[2],
        delivery_type=delivery, delivery_date=delivery_date,
        delivery_time=post.get("time", "")[:5],
        region=post.get("region", "")[:80], district=post.get("district", "")[:80],
        city=post.get("city", "")[:80], landmark=post.get("landmark", "")[:200],
    )
    order.order_number = f"ORDER#{order.pk}"
    order.save(update_fields=["order_number"])
    OrderItem.objects.bulk_create([
        OrderItem(order=order, kind=i["kind"], name=i["name"],
                  quantity=i["qty"], unit_price_usd=Decimal(str(i["price"])))
        for i in priced
    ])
    return order


def _cart_redirect(request, fallback="cart"):
    nxt = request.POST.get("next", "")
    if nxt.startswith("/") and not nxt.startswith("//"):
        return redirect(nxt)
    return redirect(fallback)


@login_required
def seller_redirect(request):
    return redirect("orders_list")


@login_required
def cart_view(request):
    role = role_of(request.user)
    if role not in ("seller", "admin"):
        messages.error(request, "Bu bo'lim faqat sotuvchi uchun.")
        return redirect("profile")

    if request.method == "POST":
        action = request.POST.get("action")
        cart = request.session.get("cart", [])
        if action == "add":
            kind = request.POST.get("kind", "")
            model = FIELDS[kind][0] if kind in FIELDS else None
            item = model.objects.filter(pk=request.POST.get("id")).first() if model else None
            if item:
                qty = max(1, min(99, int(request.POST.get("qty", 1) or 1)))
                cart.append({"kind": kind, "id": item.id, "name": item.name,
                             "price": float(item.price), "qty": qty})
                messages.success(request, f"{item.name} savatga qo'shildi.")
        elif action == "add_build":
            try:
                items = json.loads(request.POST.get("items", "[]"))
            except (TypeError, ValueError):
                items = []
            added = 0
            for row in items if isinstance(items, list) else []:
                kind = (row or {}).get("kind", "")
                model = FIELDS[kind][0] if kind in FIELDS else None
                item = model.objects.filter(pk=(row or {}).get("id")).first() if model else None
                if not item:
                    continue
                qty = max(1, min(99, int((row or {}).get("qty", 1) or 1)))
                cart.append({"kind": kind, "id": item.id, "name": item.name,
                             "price": float(item.price), "qty": qty})
                added += 1
            if added:
                messages.success(request, f"Yig'ma savatga qo'shildi ({added} ta qism).")
            else:
                messages.error(request, "Savatga qo'shish uchun mos qism topilmadi.")
        elif action == "remove":
            try:
                cart.pop(int(request.POST.get("index", -1)))
            except (ValueError, IndexError):
                pass
        elif action == "clear":
            cart = []
        elif action == "order":
            try:
                order = _create_order(request, cart, request.POST)
            except ValueError as exc:
                messages.error(request, str(exc))
            else:
                request.session["cart"] = []
                messages.success(request, f"{order.display_order_number} buyurtma yaratildi (${order.total}).")
                return redirect("order_detail", pk=order.pk)
        request.session["cart"] = cart
        return _cart_redirect(request)

    cart, _ = _cart_with_live_prices(request.session.get("cart", []))
    return render(request, "builder/cart.html", {
        "role": role,
        "cart": cart,
        "cart_total": sum(Decimal(str(i["price"])) * i["qty"] for i in cart),
        "payment_choices": Order._meta.get_field("payment_status").choices,
        "payment_type_choices": Order._meta.get_field("payment_type").choices,
        "delivery_choices": Order._meta.get_field("delivery_type").choices,
    })


@login_required
def orders_list(request):
    role = role_of(request.user)
    if role not in ("seller", "admin"):
        messages.error(request, "Bu bo'lim faqat sotuvchi uchun.")
        return redirect("profile")

    qs = _orders_for_user(request)
    phone = request.GET.get("phone", "").strip()
    digits = "".join(ch for ch in phone if ch.isdigit())
    if digits:
        if len(digits) > 3 and digits.startswith("998"):
            qs = qs.filter(Q(client_phone__contains=digits) |
                           Q(client_phone__contains=digits[3:]))
        else:
            qs = qs.filter(client_phone__contains=digits)
    date_from, date_to = request.GET.get("date_from", ""), request.GET.get("date_to", "")
    if date_from:
        qs = qs.filter(created_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(created_at__date__lte=date_to)
    seller_id = request.GET.get("seller", "")
    if role == "admin" and seller_id.isdigit():
        qs = qs.filter(seller_id=int(seller_id))

    base_qs = qs
    tab = request.GET.get("tab", "all")
    completed_qs = base_qs.filter(status="DELIVERED", payment_status="PAID")
    if tab == "completed":
        qs = completed_qs
    elif tab == "DELIVERED":
        qs = base_qs.filter(status="DELIVERED").exclude(payment_status="PAID")
    elif tab != "all" and tab in dict(Order._meta.get_field("status").choices):
        qs = qs.filter(status=tab)
    counts = {"all": base_qs.count(), "completed": completed_qs.count()}
    counts["DELIVERED"] = base_qs.filter(status="DELIVERED").exclude(
        payment_status="PAID").count()
    for status in dict(Order._meta.get_field("status").choices):
        if status != "DELIVERED":
            counts[status] = base_qs.filter(status=status).count()

    page = Paginator(qs, 20).get_page(request.GET.get("page"))
    pager_params = request.GET.copy()
    pager_params.pop("page", None)
    pager_base = pager_params.urlencode()
    tab_params = pager_params.copy()
    tab_params.pop("tab", None)
    tab_base = tab_params.urlencode()
    order_groups = []
    for order in page:
        day = order.created_at.date()
        if order_groups and order_groups[-1]["date"] == day:
            order_groups[-1]["orders"].append(order)
        else:
            order_groups.append({"date": day, "orders": [order]})

    return render(request, "builder/orders.html", {
        "role": role,
        "orders": page,
        "order_groups": order_groups,
        "counts": counts,
        "tab": tab,
        "status_choices": Order._meta.get_field("status").choices,
        "sellers": get_user_model().objects.filter(is_superuser=False).order_by("username") if role == "admin" else [],
        "pager_base": pager_base,
        "tab_base": tab_base,
        "filters": {"phone": phone, "date_from": date_from, "date_to": date_to,
                    "seller": seller_id},
    })


@login_required
def order_detail(request, pk):
    role = role_of(request.user)
    if role not in ("seller", "admin"):
        return redirect("profile")
    order = get_object_or_404(_orders_for_user(request), pk=pk)
    flow = order.status_flow(order.delivery_type)
    own = order.seller_id == request.user.id
    allowed = [s for s, _ in Order.status_choices_for_delivery(order.delivery_type)]
    if role != "admin":
        allowed = [s for s in allowed if s in ("NEW", "AGREED", "QUEUED", "CANCELLED")]
        if order.status not in allowed:
            allowed.insert(0, order.status)
    return render(request, "builder/order_detail.html", {
        "role": role,
        "order": order,
        "lines": order.lines.all(),
        "flow": flow,
        "flow_labels": {s: Order.status_label(s, order.delivery_type) for s in flow},
        "can_manage": role == "admin" or own,
        "can_edit": role == "admin" or own,
        "can_delete": role == "admin",
        "allowed_statuses": [(s, Order.status_label(s, order.delivery_type)) for s in allowed],
        "current_index": flow.index(order.status) + 1 if order.status in flow else 0,
        "payment_statuses": Order._meta.get_field("payment_status").choices,
        "payment_type_labels": dict(Order._meta.get_field("payment_type").choices),
    })


@require_POST
@login_required
def order_status(request, pk):
    order = get_object_or_404(_orders_for_user(request), pk=pk)
    role = role_of(request.user)
    target = request.POST.get("status", "").strip()
    if not _can_set_status(role, request.user, order, target):
        return JsonResponse({"error": "Siz bu holatni o'zgartira olmaysiz."}, status=403)
    payment = request.POST.get("payment_status", "").strip()
    if payment not in dict(Order._meta.get_field("payment_status").choices):
        payment = order.payment_status
    # To'lov holati shu so'rovda o'zgarishi mumkin, shuning uchun tekshiruv shuni hisobga oladi.
    probe = Order(status=order.status, delivery_type=order.delivery_type, payment_status=payment)
    ok, error = _validate_status_transition(probe, target)
    if not ok:
        return JsonResponse({"error": error}, status=400)

    order.status = target
    order.payment_status = payment
    if target == "DELIVERED" and not order.delivered_at:
        order.delivered_at = timezone.now()
    order.save(update_fields=["status", "payment_status", "delivered_at", "updated_at"])

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "status": order.status_display,
                             "number": order.display_order_number})
    messages.success(request, f"Holat yangilandi: {order.status_display}")
    return redirect("order_detail", pk=order.pk)


@login_required
def order_edit(request, pk):
    """Buyurtma ma'lumotlarini tahrirlash (qatorlar o'zgarmaydi, jami qayta hisoblanadi)."""
    role = role_of(request.user)
    order = get_object_or_404(_orders_for_user(request), pk=pk)
    if role != "admin" and order.seller_id != request.user.id:
        messages.error(request, "Bu buyurtmani tahrirlash huquqi yo'q.")
        return redirect("order_detail", pk=pk)

    if request.method == "POST":
        post = request.POST
        client = post.get("client", "").strip()
        if not client:
            messages.error(request, "Klient ismini kiriting.")
            return redirect("order_edit", pk=pk)
        payment = post.get("payment_status", "UNPAID")
        if payment not in dict(Order._meta.get_field("payment_status").choices):
            payment = "UNPAID"
        payment_type = post.get("payment_type", "CASH")
        if payment_type not in dict(Order._meta.get_field("payment_type").choices):
            payment_type = "CASH"
        delivery = post.get("delivery_type", "PICKUP")
        if delivery not in dict(Order._meta.get_field("delivery_type").choices):
            delivery = "PICKUP"
        partial = _money(post.get("partial_amount"), Decimal("0")) if payment == "PARTIAL" else Decimal("0")
        total = sum(Decimal(str(l.unit_price_usd)) * l.quantity for l in order.lines.all())
        partial = max(Decimal("0"), min(partial, total))
        mixed = [Decimal("0")] * 3
        if payment_type == "CASH_CARD" and payment in ("PAID", "PARTIAL"):
            mixed = [_money(post.get("cash_amount"), Decimal("0")),
                     _money(post.get("card_amount"), Decimal("0")),
                     _money(post.get("transfer_amount"), Decimal("0"))]
            expected = total if payment == "PAID" else partial
            if abs(sum(mixed) - expected) > Decimal("0.01"):
                messages.error(request, f"Aralash to'lov yig'indisi ${expected} bo'lishi kerak.")
                return redirect("order_edit", pk=pk)
        raw_date = post.get("delivery_date", "").strip()
        try:
            delivery_date = datetime.strptime(raw_date, "%Y-%m-%d").date() if raw_date else None
        except ValueError:
            delivery_date = None

        order.client_name = client[:120]
        order.client_phone = post.get("phone", "")[:30]
        order.note = post.get("note", "")[:2000]
        order.payment_status = payment
        order.payment_type = payment_type
        order.partial_amount = partial
        order.cash_amount, order.card_amount, order.transfer_amount = mixed
        order.delivery_type = delivery
        order.delivery_date = delivery_date
        order.delivery_time = post.get("time", "")[:5]
        order.region = post.get("region", "")[:80]
        order.district = post.get("district", "")[:80]
        order.city = post.get("city", "")[:80]
        order.landmark = post.get("landmark", "")[:200]
        order.total = total
        rate = Decimal(str(_settings().usd_to_uzs or 0))
        order.total_uzs = int((total * rate).quantize(Decimal("1"))) if rate > 0 else 0
        order.save()
        messages.success(request, f"{order.display_order_number} yangilandi.")
        return redirect("order_detail", pk=pk)

    return render(request, "builder/order_edit.html", {
        "role": role,
        "order": order,
        "payment_choices": Order._meta.get_field("payment_status").choices,
        "payment_type_choices": Order._meta.get_field("payment_type").choices,
        "delivery_choices": Order._meta.get_field("delivery_type").choices,
    })


@require_POST
@login_required
def order_delete(request, pk):
    if role_of(request.user) != "admin":
        messages.error(request, "Buyurtmani o'chirish faqat admin uchun.")
        return redirect("orders_list")
    get_object_or_404(Order, pk=pk).delete()
    messages.success(request, "Buyurtma o'chirildi.")
    return redirect("orders_list")


@require_GET
@login_required
def export_orders(request):
    """Buyurtmalarni CSV ga eksport qiladi (sotuvchi — faqat o'ziniki)."""
    qs = _orders_for_user(request).filter(
        created_at__date__gte=request.GET.get("date_from") or date.min,
        created_at__date__lte=request.GET.get("date_to") or date.max,
    )
    if request.GET.get("tab") == "completed":
        qs = qs.filter(status="DELIVERED", payment_status="PAID")
    seller_id = request.GET.get("seller", "")
    if role_of(request.user) == "admin" and seller_id.isdigit():
        qs = qs.filter(seller_id=int(seller_id))
    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = 'attachment; filename="buyurtmalar.csv"'
    writer = csv.writer(response)
    writer.writerow(["Raqam", "Klient", "Telefon", "Sotuvchi", "Holat", "To'lov turi",
                     "To'lov holati", "Jami USD", "Jami so'm", "Qoldiq USD",
                     "Yetkazish", "Sana vaqti", "Yetkazish sanasi", "Manzil"])
    for o in qs:
        writer.writerow([o.display_order_number, o.client_name, phone_format(o.client_phone),
                         o.seller.username, o.status_display, o.get_payment_type_display(),
                         o.get_payment_status_display(), o.total, o.total_uzs,
                         o.remaining_amount, o.get_delivery_type_display(),
                         o.created_at.strftime("%d.%m.%Y %H:%M"),
                         str(o.delivery_date or ""), o.address])
    return response


# --- Saqlangan yig'malar API ----------------------------------------------------

def _owner(request):
    """Saqlangan yig'malarni brauzer sessioni bilan bog'laydi."""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


@require_POST
def save_build(request):
    payload = json.loads(request.body.decode("utf-8"))
    obj = SavedBuild.objects.create(
        owner=_owner(request),
        user=request.user if request.user.is_authenticated else None,
        name=str(payload.get("name", "Mening PCim"))[:120],
        data=payload.get("data", {}),
        total=payload.get("total", 0) or 0,
    )
    _record_calculation(request, payload.get("mode", "pc"), payload.get("data", {}))
    return JsonResponse({"ok": True, "id": obj.id, "name": obj.name})


@require_GET
def list_builds(request):
    qs = _saved_qs(request).order_by("-created_at")[:50]
    return JsonResponse({"items": [
        {"id": o.id, "name": o.name, "total": float(o.total),
         "created": o.created_at.strftime("%d.%m %H:%M")} for o in qs
    ]})


@require_POST
def load_build(request, bid):
    obj = _saved_qs(request).filter(id=bid).first()
    if not obj:
        return JsonResponse({"error": "topilmadi"}, status=404)
    return JsonResponse({"data": obj.data, "name": obj.name})


@require_POST
def delete_build(request, bid):
    _saved_qs(request).filter(id=bid).delete()
    return JsonResponse({"ok": True})


@require_POST
def clear_builds(request):
    _saved_qs(request).delete()
    return JsonResponse({"ok": True})
