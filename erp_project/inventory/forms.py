from django import forms
from .models import InventoryMovements, LocationInventory

class InventoryMovementForm(forms.ModelForm):

    class Meta:
        model = InventoryMovements
        fields = ['id_inventory_movement', 'id_location', 'id_material', 'quantity', 'unit_type', 'movement_type']


class CsvUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='Select a CSV file', 
        help_text='The file must contain headers that match the model fields.'
    )