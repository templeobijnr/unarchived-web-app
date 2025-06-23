from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Supplier, RFQ, Quote, KPI
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Get or create admin user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write('Created admin user')
        
        # Create suppliers
        suppliers_data = [
            {
                'name': 'Shenzhen Tech Cases Ltd',
                'logo': 'https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&cs=tinysrgb&w=200&h=200&fit=crop',
                'category': 'Electronics Accessories',
                'reliability': 94,
                'region': 'Shenzhen, China',
                'capabilities': ['Injection Molding', 'UV Printing', 'Assembly'],
                'certifications': ['ISO 9001', 'BSCI', 'RoHS'],
                'contact_email': 'sales@sztechcases.com',
                'contact_phone': '+86 755 8888 9999',
                'contact_address': 'Building A, Tech Park, Shenzhen, China'
            },
            {
                'name': 'Guangzhou Mobile Accessories',
                'logo': 'https://images.pexels.com/photos/3184338/pexels-photo-3184338.jpeg?auto=compress&cs=tinysrgb&w=200&h=200&fit=crop',
                'category': 'Mobile Accessories',
                'reliability': 89,
                'region': 'Guangzhou, China',
                'capabilities': ['Screen Printing', 'Silicone Molding', 'Packaging'],
                'certifications': ['ISO 14001', 'SEDEX', 'CE'],
                'contact_email': 'info@gzmobile.com',
                'contact_phone': '+86 20 8888 7777',
                'contact_address': 'Industrial Zone, Guangzhou, China'
            },
            {
                'name': 'Premium Cases Co',
                'logo': 'https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=200&h=200&fit=crop',
                'category': 'Luxury Accessories',
                'reliability': 97,
                'region': 'Hong Kong',
                'capabilities': ['Leather Crafting', 'Embossing', 'Premium Packaging'],
                'certifications': ['ISO 9001', 'WRAP', 'FSC'],
                'contact_email': 'premium@casesco.hk',
                'contact_phone': '+852 3888 6666',
                'contact_address': 'Central District, Hong Kong'
            }
        ]
        
        suppliers = []
        for supplier_data in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                name=supplier_data['name'],
                defaults=supplier_data
            )
            suppliers.append(supplier)
            if created:
                self.stdout.write(f'Created supplier: {supplier.name}')
        
        # Create RFQs
        rfqs_data = [
            {
                'title': 'Custom Phone Cases - 10K Units',
                'description': 'Looking for custom phone cases with logo printing for iPhone 14/15 series',
                'category': 'Electronics',
                'quantity': 10000,
                'target_price': 2.00,
                'currency': 'USD',
                'deadline': datetime.now() + timedelta(days=7),
                'status': 'published',
                'responses': 12
            },
            {
                'title': 'Bluetooth Headphones - 5K Units',
                'description': 'Wireless earbuds with custom branding and packaging',
                'category': 'Electronics',
                'quantity': 5000,
                'target_price': 15.00,
                'currency': 'USD',
                'deadline': datetime.now() + timedelta(days=14),
                'status': 'published',
                'responses': 8
            }
        ]
        
        rfqs = []
        for rfq_data in rfqs_data:
            rfq, created = RFQ.objects.get_or_create(
                title=rfq_data['title'],
                defaults={**rfq_data, 'created_by': user}
            )
            rfqs.append(rfq)
            if created:
                self.stdout.write(f'Created RFQ: {rfq.title}')
        
        # Create quotes
        quotes_data = [
            {
                'rfq': rfqs[0],
                'supplier': suppliers[0],
                'product': 'Custom Phone Cases',
                'price': 2.50,
                'currency': 'USD',
                'lead_time': 15,
                'moq': 1000,
                'status': 'pending',
                'specs': {
                    'material': 'TPU + PC',
                    'printing': 'UV Printing',
                    'packaging': 'Individual poly bags'
                }
            },
            {
                'rfq': rfqs[0],
                'supplier': suppliers[1],
                'product': 'Custom Phone Cases',
                'price': 2.20,
                'currency': 'USD',
                'lead_time': 20,
                'moq': 500,
                'status': 'pending',
                'specs': {
                    'material': 'Silicone',
                    'printing': 'Screen Printing',
                    'packaging': 'Bulk packaging'
                }
            },
            {
                'rfq': rfqs[1],
                'supplier': suppliers[2],
                'product': 'Custom Phone Cases',
                'price': 3.80,
                'currency': 'USD',
                'lead_time': 12,
                'moq': 2000,
                'status': 'accepted',
                'specs': {
                    'material': 'Premium Leather',
                    'printing': 'Embossing',
                    'packaging': 'Gift boxes'
                }
            }
        ]
        
        for quote_data in quotes_data:
            quote, created = Quote.objects.get_or_create(
                rfq=quote_data['rfq'],
                supplier=quote_data['supplier'],
                defaults=quote_data
            )
            if created:
                self.stdout.write(f'Created quote: {quote.supplier.name} - {quote.product}')
        
        # Create KPI data
        kpi, created = KPI.objects.get_or_create(
            user=user,
            defaults={
                'saved_cost': 285000.00,
                'quotes_in_flight': 24,
                'on_time_rate': 94.2,
                'total_orders': 156,
                'active_suppliers': 43,
                'avg_lead_time': 18
            }
        )
        if created:
            self.stdout.write('Created KPI data')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        ) 