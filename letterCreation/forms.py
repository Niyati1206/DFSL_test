from django import forms
from .models import Manufacturer
from .models import MainItem


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'



class MainItemForm(forms.ModelForm):
    manufacturer = forms.CharField(max_length=100)
    
    class Meta:
        model = MainItem
        fields = ['name']