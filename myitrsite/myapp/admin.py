from django.contrib import admin
from .models import ModelFormWithFileField

class ModelFormWithFileFieldAdmin(admin.ModelAdmin):
    list_display=('file_field',)

admin.site.register(ModelFormWithFileField,ModelFormWithFileFieldAdmin)
