from django.contrib import admin
from .models import (
    Supplier, SupplierContact, SupplierVerification, 
    CommunicationLog
)

# Register your models here.

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'region', 'reliability', 'verification_status', 'created_at')
    list_filter = ('verification_status', 'region', 'category')
    search_fields = ('name', 'contact_person', 'company_info')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SupplierContact)
class SupplierContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'email', 'phone', 'contact_type')
    list_filter = ('contact_type', 'supplier__name')
    search_fields = ('name', 'email', 'supplier__name')
    raw_id_fields = ('supplier',)




@admin.register(CommunicationLog)
class CommunicationLogAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'communication_type', 'direction', 'created_at')
    list_filter = ('communication_type', 'direction')
    search_fields = ('summary', 'supplier__name')
    raw_id_fields = ('supplier', 'initiated_by')

admin.site.register(SupplierVerification)