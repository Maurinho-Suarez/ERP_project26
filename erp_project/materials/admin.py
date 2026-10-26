from django.contrib import admin
from .models import Unit, MaterialType

@admin.register(Unit)
class UnitMeasurementAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
