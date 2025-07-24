from django.contrib import admin
from .models import DigitalProductGenome

@admin.register(DigitalProductGenome)
class DigitalProductGenomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'owner', 'stage', 'created_at', 'updated_at')
    list_filter = ('stage', 'created_at', 'updated_at')
    search_fields = ('title', 'owner__username', 'version', 'summary')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'version', 'owner', 'description', 'summary', 'stage')
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('data',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
