from django.db import models
from django import forms
from django.forms import ClearableFileInput

class ModelFormWithFileField(models.Model):
    file_field = models.FileField()

class FileFieldForm(forms.ModelForm):
    class Meta:
        model = ModelFormWithFileField
        fields=['file_field']
        widgets={
            'file_field':ClearableFileInput(attrs={'multiple':True}),
        }
        exclude = ('',)
