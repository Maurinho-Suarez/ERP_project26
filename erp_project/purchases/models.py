from django.db import models
from django.conf import settings
from suppliers.models import Supplier
from materials.models import Material, Unit
from core.models import Currency

class OrderStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name="Order Status Name")
    symbol = models.CharField(max_length=10, verbose_name="Order Status Symbol")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name = "Order Status"
        verbose_name_plural = "Order Statuses"

    def __str__(self):
        return self.symbol

class PurchaseOrder(models.Model):
    id_purchase_order = models.CharField(max_length=20, verbose_name="ID Purchase Order")
    id_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="Supplier")
    issue_date = models.DateField(auto_now_add=True)
    estimated_deliver_date = models.DateField(verbose_name="Estimated Delivery Date")
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, verbose_name="Order Status")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"

    def __str__(self):
        return self.id_purchase_order

class LinesPurchaseOrder(models.Model):
    id_purchase_order_line = models.CharField(max_length=20, verbose_name="ID Purchase Order Line")
    id_purchase_order = models.ForeignKey(PurchaseOrder, default=1, on_delete=models.CASCADE, verbose_name="Purchase Order")
    id_material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name="Material", related_name="id_material_1")
    position = models.IntegerField(verbose_name="Position")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantity")
    unit_material = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name="Unit Material")
    price = models.FloatField(verbose_name="Price")
    currency_supplier = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True, verbose_name="Currency")
    received_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Received Quantity", default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Line Purchase Order"
        verbose_name_plural = "Lines Purchase Orders"

    def __str__(self):
        return self.id_purchase_order_line
