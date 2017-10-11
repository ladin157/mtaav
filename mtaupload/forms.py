from django import  forms
from django.contrib.auth.models import User

from .models import Category, File

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['provider', 'category_title', "type", 'category_logo']

class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['filename', 'data_file']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']