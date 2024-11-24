from django import forms
from .models import CSVFile


class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = CSVFile
        fields = ['name', 'file']
