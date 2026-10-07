from django.db import models
from django.conf import settings

# Create your models here.
class Material(models.Model):
    id_material = models.CharField(max_length=50, null=True, blank=True, verbose_name="Material ID")
    name = models.CharField(max_length=100, verbose_name="Material Name")
    description = models.TextField(max_length=250, blank=True, verbose_name="Material Description")
    unit = models.CharField(max_length=50, verbose_name="Unit measurement")
    material_type = models.CharField(max_length=50, verbose_name="Material Type")
    status = models.CharField(max_length=50, verbose_name="Status")

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"

    def __str__(self):
        return self.name
