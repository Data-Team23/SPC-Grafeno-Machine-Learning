from django.contrib import admin
from .models import CSVFile


@admin.register(CSVFile)
class CSVFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at', 'file', )
    search_fields = ('name', )
    list_filter = ('uploaded_at', )
    ordering = ('-uploaded_at', )
