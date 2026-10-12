from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ['id_supplier', 'legal_name', 'name', 'tax_id', 'country', 'state_province', 'city', 'address', 'zip_code', 'phone', 'email', 'contact_name', 'contact_role',
                  'category', 'payment_terms', 'currency', 'payment_method', 'bank_account', 'status']