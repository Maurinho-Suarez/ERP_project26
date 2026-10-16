from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['id_material', 'name', 'description', 'unit', 'material_type', 'status'] 


class CsvUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='Select a CSV file', 
        help_text='The file must contain headers that match the model fields.'
    )
        