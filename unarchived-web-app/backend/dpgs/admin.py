from django.contrib import admin
from .models import DigitalProductGenome, DPGComponent, GeneratedAsset, ApparelDPGExtension

# Inline for DPGComponents
class DPGComponentInline(admin.TabularInline):
    model = DPGComponent
    extra = 1  # To add at least one blank component row by default
    fields = ('name', 'description', 'order')  # Fields to display for DPGComponent
    ordering = ('order',)  # Ensure the components are ordered by their 'order' field

# Inline for GeneratedAssets
class GeneratedAssetInline(admin.TabularInline):
    model = GeneratedAsset
    extra = 1  # Allow one additional blank asset row
    fields = ('file', 'description')  # Fields to display for GeneratedAsset

# Admin for ApparelDPGExtension
class ApparelDPGExtensionInline(admin.StackedInline):
    model = ApparelDPGExtension
    extra = 1  # One extra blank apparel extension row (can be zero if optional)
    fields = ('fabric_composition', 'sizing_chart', 'fit_information', 'construction_details', 'hardware_components', 'colorways', 'cost_breakdown', 'manufacturing_data')
    classes = ('collapse',)  # Make this section collapsible for easier management

# Main admin for DigitalProductGenome
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
        ('Components and Assets', {
            'classes': ('collapse',),
            'fields': ('data',)
        }),
        ('Apparel Extension', {
            'classes': ('collapse',),
            'fields': ('apparel_extension',)  # Linking to the ApparelDPGExtension model
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    # Including inlines for components, assets, and apparel extensions
    inlines = [DPGComponentInline, GeneratedAssetInline, ApparelDPGExtensionInline]

    def get_inline_instances(self, request, obj=None):
        """
        Customize the inline instances depending on whether the object exists or not.
        In this case, we make sure to show the ApparelDPGExtension only if it's an apparel DPG.
        """
        inline_instances = super().get_inline_instances(request, obj)
        if obj and obj.data.get('category') == 'apparel':  # Only show the apparel extension if it's an apparel DPG
            inline_instances.append(ApparelDPGExtensionInline(self.model, self.admin_site))
        return inline_instances
