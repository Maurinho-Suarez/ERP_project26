from django.contrib import admin
from .models import MovementType, LocationInventory, InventoryMovements

@admin.register(MovementType)
class MovementTypeAdmin(admin.ModelAdmin):
    list_display = ('name','symbol')

@admin.register(LocationInventory)
class LocationInventoryAdmin(admin.ModelAdmin):
    list_display = ('id_location','name','code','main_location','location')

@admin.register(InventoryMovements)
class InventoryMovementsAdmin(admin.ModelAdmin):
    list_display = ('id_inventory_movement','id_location','id_material','quantity','unit_type','movement_type') 
