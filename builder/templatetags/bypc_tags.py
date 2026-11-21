from django import template

register = template.Library()


@register.filter
def get_item(mapping, key):
    """Lug'atdan kalit bo'yicha qiymat oladi (shablonda hisoblar uchun)."""
    if hasattr(mapping, "get"):
        return mapping.get(key, 0)
    return 0


@register.filter
def phone_format(value):
    """+998901234567 ni +998 (90) 123-45-67 ko'rinishiga keltiradi."""
    digits = "".join(ch for ch in str(value or "") if ch.isdigit())
    if len(digits) == 9:
        digits = "998" + digits
    if len(digits) != 12 or not digits.startswith("998"):
        return value or "—"
    return f"+998 ({digits[3:5]}) {digits[5:8]}-{digits[8:10]}-{digits[10:]}"
