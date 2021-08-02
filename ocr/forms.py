from django import forms
from .models import *
  
class OcrForm(forms.ModelForm):
  
    class Meta:
        model = Ocr
        fields = ['image',]