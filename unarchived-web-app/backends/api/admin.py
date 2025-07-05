from django.contrib import admin
from .models import (
    Supplier, SupplierContact, SupplierVerification, 
    RFQ, RFQDistribution, Quote, 
    Message, KPI, CommunicationLog
)

# Custom Admin Views for better usability


# Register other models directly for simplicity


admin.site.register(KPI)
