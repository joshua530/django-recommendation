from django import forms
from .models import Cloth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class ClothCreationForm(forms.ModelForm):
    class Meta:
        model = Cloth
        fields = ['name','price','image']

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']

    def clean_password(self):
        password = self.data['password']
        password_2 = self.data['confirm_password']

        if password != password_2:
            raise forms.ValidationError('The password and password confirmation fields must match')
        return make_password(password)
