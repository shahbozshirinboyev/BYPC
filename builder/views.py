import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .models import (
    CPU, Motherboard, RAM, Cooler, GPU, SSD, HDD, PSU, Case,
    Monitor, KeyboardMouse, Headset, SavedBuild, Settings,
)

FIELDS = {
    "cpu": (CPU, "id name price brand socket cores watt"),
    "mb": (Motherboard, "id name price brand socket ram_type form_factor m2_slots"),
    "ram": (RAM, "id name price brand ram_type capacity_gb speed_mhz"),
    "cool": (Cooler, "id name price brand cooler_type sockets cooling_watt height_mm"),
    "gpu": (GPU, "id name price brand chipset vram_gb watt length_mm"),
    "ssd": (SSD, "id name price brand interface capacity_gb"),
    "hdd": (HDD, "id name price brand form_factor capacity_gb rpm"),
    "psu": (PSU, "id name price brand watt efficiency modular"),
    "case": (Case, "id name price brand case_type form_factors max_gpu_length max_cooler_height"),
    "mon": (Monitor, "id name price brand panel size_inch refresh_hz"),
    "kbm": (KeyboardMouse, "id name price brand connection layout"),
    "head": (Headset, "id name price brand connection surround"),
}


def index(request):
    """Baza ma'lumotlarini kalkulyatorga JSON sifatida uzatadi."""
    conf = Settings.objects.first()
    if conf is None:
        conf = Settings.objects.create()
    catalog = {}
    for key, (model, fields) in FIELDS.items():
        items = list(model.objects.values(*fields.split()))
        for item in items:
            item["price"] = float(item["price"])
        catalog[key] = items
    return render(request, "builder/index.html", {
        "catalog": catalog,
        "rate": str(conf.usd_to_uzs),
        "markup": str(conf.markup_percent),
    })


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
        name=str(payload.get("name", "Mening PCim"))[:120],
        data=payload.get("data", {}),
        total=payload.get("total", 0) or 0,
    )
    return JsonResponse({"ok": True, "id": obj.id, "name": obj.name})


@require_GET
def list_builds(request):
    qs = SavedBuild.objects.filter(owner=_owner(request)).order_by("-created_at")[:50]
    return JsonResponse({"items": [
        {"id": o.id, "name": o.name, "total": float(o.total),
         "created": o.created_at.strftime("%d.%m %H:%M")} for o in qs
    ]})


@require_POST
def load_build(request, bid):
    obj = SavedBuild.objects.filter(id=bid, owner=_owner(request)).first()
    if not obj:
        return JsonResponse({"error": "topilmadi"}, status=404)
    return JsonResponse({"data": obj.data, "name": obj.name})


@require_POST
def delete_build(request, bid):
    SavedBuild.objects.filter(id=bid, owner=_owner(request)).delete()
    return JsonResponse({"ok": True})


@require_POST
def clear_builds(request):
    SavedBuild.objects.filter(owner=_owner(request)).delete()
    return JsonResponse({"ok": True})
