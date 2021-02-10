from django import forms
from .models import Cloth

class ClothCreationForm(forms.ModelForm):
    class Meta:
        model = Cloth
        fields = ['name','price','image']
