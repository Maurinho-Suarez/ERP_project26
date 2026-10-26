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

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Country Name")
    code = models.CharField(max_length=10, unique=True, verbose_name="Country Code")

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name} ({self.code})"

class Currency(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Currency Name")
    code = models.CharField(max_length=10, unique=True, verbose_name="Currency Code")
    symbol = models.CharField(max_length=10, unique=True, verbose_name="Currency Symbol")
    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
