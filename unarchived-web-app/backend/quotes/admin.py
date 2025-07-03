from django.contrib import admin
from .models import (
    Quote
)

# Register your models here.

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'supplier', 'status', 'price', 'created_at')
    list_filter = ('status', 'supplier__name')
    search_fields = ('rfq__title', 'supplier__name')
    raw_id_fields = ('rfq', 'supplier')
