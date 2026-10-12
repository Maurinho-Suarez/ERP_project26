from django.db import models
from django.conf import settings

# Create your models here.
class Supplier(models.Model):
    id_supplier = models.CharField(max_length=50, null=True, unique=True, verbose_name="Supplier ID")
    legal_name = models.CharField(max_length=150, verbose_name="Legal Name")
    name = models.TextField(max_length=100, verbose_name="Name")
    tax_id = models.CharField(max_length=30, verbose_name="Tax ID")
    country = models.CharField(max_length=70, verbose_name="Country")
    state_province = models.CharField(max_length=70, verbose_name="State/Province")
    city = models.CharField(max_length=100, verbose_name="City")
    address = models.CharField(max_length=150, verbose_name="Address")
    zip_code = models.IntegerField(verbose_name="Zip Code")
    phone = models.IntegerField(verbose_name="Phone")
    email = models.EmailField(max_length=150, verbose_name="Email")
    contact_name = models.CharField(max_length=150, verbose_name="Contact Name")
    contact_role = models.CharField(max_length=150, verbose_name="Contact Role")
    category = models.CharField(max_length=150, verbose_name="Category")
    payment_terms = models.CharField(max_length=150, verbose_name="Payment Terms")
    currency = models.CharField(max_length=150, verbose_name="Currency")
    payment_method = models.CharField(max_length=150, verbose_name="Payment Method")
    bank_account = models.CharField(max_length=150, verbose_name="Bank Account")
    
    status = models.CharField(max_length=50, verbose_name="Status")

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    def __str__(self):
        return self.name

