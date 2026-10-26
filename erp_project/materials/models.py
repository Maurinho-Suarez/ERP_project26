from django.db import models
from django.conf import settings
from core.models import Status

# Create your models here.
class Unit(models.Model):
    name = models.CharField(max_length=50, verbose_name="Unit Name")
    symbol = models.CharField(max_length=10, unique=True, verbose_name="Symbol")

    class Meta:
        verbose_name = "Unit"
        verbose_name_plural = "Units"

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class MaterialType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Material Type Name")
    symbol = models.CharField(max_length=10, unique=True, verbose_name="Symbol")

    class Meta:
        verbose_name = "Material Type"
        verbose_name_plural = "Material Types"

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class Material(models.Model):
    id_material = models.CharField(max_length=50, null=True, unique=True, verbose_name="Material ID")
    name = models.CharField(max_length=100, verbose_name="Material Name")
    description = models.TextField(max_length=250, blank=True, verbose_name="Material Description")
    unit = models.ForeignKey(Unit, default=1, on_delete=models.PROTECT, verbose_name="Unit measurement")
    material_type = models.ForeignKey(MaterialType, default=1, on_delete=models.PROTECT, verbose_name="Material Type")
    status = models.ForeignKey(Status, default=1, on_delete=models.PROTECT, verbose_name="Status")

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"

    def __str__(self):
        return self.name
