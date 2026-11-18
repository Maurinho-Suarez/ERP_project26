from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from core.models import Status
from materials.models import Material, Unit

class MovementType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    symbol = models.CharField(max_length=10, verbose_name='Symbol')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Movement Type"
        verbose_name_plural = "Movement Types"


    def __str__(self):
        return f"{self.symbol} - {self.name}"

class LocationInventory(models.Model):
    id_location = models.CharField(max_length=10, primary_key=True, verbose_name="Location ID")
    name = models.CharField(max_length=100,verbose_name="Name")
    code = models.CharField(max_length=100,verbose_name="Code")
    main_location = models.BooleanField(default=False,verbose_name="Main Location")
    location = models.TextField(blank=True,verbose_name="Address")
    status = models.ForeignKey(Status,default=1,on_delete=models.PROTECT,verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    class Meta:
        verbose_name = "Inventory Location"
        verbose_name_plural = "Inventory Locations"

    def __str__(self):
        return f"{self.code} - {self.name}"


class InventoryMovements(models.Model):

    id_inventory_movement = models.CharField(max_length=10, primary_key=True, verbose_name="Inventory Movement ID")
    id_location = models.ForeignKey(LocationInventory, on_delete=models.PROTECT, verbose_name="Location ID")
    id_material = models.ForeignKey(Material, on_delete=models.PROTECT, verbose_name="Material ID")
    quantity = models.IntegerField(verbose_name="Quantity")
    unit_type = models.ForeignKey(Unit,on_delete=models.PROTECT,verbose_name="Unit Type")
    movement_type = models.ForeignKey(MovementType,on_delete=models.PROTECT,verbose_name="Movement ID")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
        
    class Meta:
        verbose_name = "Inventory Movement"
        verbose_name_plural = "Inventory Movements"
        
        
    def __str__(self):
        return f"{self.id_material} - {self.quantity} - {self.unit_type}"
    