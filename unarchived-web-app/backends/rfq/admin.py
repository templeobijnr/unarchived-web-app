from django.contrib import admin
from .models import (
    RFQ, RFQDistribution
)


# Register your models here.
@admin.register(RFQ)
class RFQAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'deadline', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description')
    ordering = ('-deadline',)
    raw_id_fields = ('created_by',)
    
admin.site.register(RFQDistribution)