from django.db import models

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name="Status Name")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"

    def __str__(self):
        return self.name
