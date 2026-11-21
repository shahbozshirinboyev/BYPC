from django.db import migrations


def forwards(apps, schema_editor):
    Order = apps.get_model("builder", "Order")
    OrderItem = apps.get_model("builder", "OrderItem")

    status_map = {"new": "NEW", "done": "DELIVERED", "canceled": "CANCELLED"}
    for order in Order.objects.all():
        changes = []
        if order.status in status_map:
            order.status = status_map[order.status]
            changes.append("status")
        if not order.order_number:
            order.order_number = "ORDER#%s" % order.pk
            changes.append("order_number")
        if changes:
            order.save(update_fields=changes)

        if not OrderItem.objects.filter(order_id=order.pk).exists():
            for item in order.items or []:
                try:
                    price = float(item.get("price", 0) or 0)
                except (TypeError, ValueError):
                    price = 0
                try:
                    qty = int(item.get("qty", 1) or 1)
                except (TypeError, ValueError):
                    qty = 1
                OrderItem.objects.create(
                    order_id=order.pk,
                    kind=str(item.get("kind", "") or "")[:20],
                    name=str(item.get("name", "Qism") or "Qism")[:200],
                    quantity=max(1, qty),
                    unit_price_usd=price,
                )


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("builder", "0009_order_delivered_at_order_delivery_date_and_more"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
