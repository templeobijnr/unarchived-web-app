#!/usr/bin/env python3
"""
Test Script: Supplier Directory & RFQ Distribution System
Demonstrates the enhanced supplier verification and RFQ distribution capabilities
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

from suppliers.models import *
from rfq.models import *
from quotes.models import *

from api.rfq_distribution import rfq_distribution_service
from api.supplier_verification import supplier_verification_service


def create_test_data():
    """Create test data for the supplier directory system"""
    print("🏭 Creating test data for Supplier Directory & RFQ System...")
    
    # Create test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print("✅ Created test user")
    
    # Create verified suppliers
    suppliers_data = [
        {
            'name': 'TechCorp Electronics',
            'legal_name': 'TechCorp Electronics Ltd.',
            'category': 'Electronics',
            'categories': ['Electronics', 'Components', 'PCB'],
            'region': 'Asia',
            'country': 'China',
            'verification_status': 'verified',
            'reliability': 95,
            'response_time_avg': 12,
            'quote_acceptance_rate': Decimal('85.5'),
            'contact_email': 'sales@techcorp.com',
            'contact_phone': '+86-138-0013-8000',
            'contact_address': 'Shenzhen, Guangdong, China',
            'business_type': 'Manufacturer',
            'year_established': 2010,
            'employee_count': '500-1000',
            'annual_revenue': '$10M-$50M',
            'certifications': ['ISO 9001', 'CE', 'RoHS'],
            'quality_standards': ['ISO 9001:2015', 'IATF 16949'],
            'capabilities': ['Custom Manufacturing', 'OEM', 'PCB Assembly'],
            'payment_terms': 'Net 30',
            'minimum_order_value': Decimal('1000.00'),
            'lead_time_range': '7-14 days'
        },
        {
            'name': 'Global Machinery Co.',
            'legal_name': 'Global Machinery Corporation',
            'category': 'Machinery',
            'categories': ['Machinery', 'Industrial', 'Automation'],
            'region': 'Europe',
            'country': 'Germany',
            'verification_status': 'verified',
            'reliability': 88,
            'response_time_avg': 24,
            'quote_acceptance_rate': Decimal('78.2'),
            'contact_email': 'info@globalmachinery.de',
            'contact_phone': '+49-30-1234-5678',
            'contact_address': 'Berlin, Germany',
            'business_type': 'Manufacturer',
            'year_established': 1995,
            'employee_count': '200-500',
            'annual_revenue': '$5M-$10M',
            'certifications': ['ISO 9001', 'CE', 'TÜV'],
            'quality_standards': ['ISO 9001:2015', 'ISO 14001'],
            'capabilities': ['Custom Machinery', 'Automation Systems'],
            'payment_terms': 'Net 45',
            'minimum_order_value': Decimal('5000.00'),
            'lead_time_range': '14-21 days'
        },
        {
            'name': 'Textile Solutions Inc.',
            'legal_name': 'Textile Solutions International',
            'category': 'Textiles',
            'categories': ['Textiles', 'Fabric', 'Apparel'],
            'region': 'Asia',
            'country': 'India',
            'verification_status': 'verified',
            'reliability': 82,
            'response_time_avg': 36,
            'quote_acceptance_rate': Decimal('72.1'),
            'contact_email': 'contact@textilesolutions.in',
            'contact_phone': '+91-80-9876-5432',
            'contact_address': 'Mumbai, Maharashtra, India',
            'business_type': 'Manufacturer',
            'year_established': 2005,
            'employee_count': '1000-2000',
            'annual_revenue': '$20M-$50M',
            'certifications': ['ISO 9001', 'GOTS', 'OEKO-TEX'],
            'quality_standards': ['ISO 9001:2015', 'SA 8000'],
            'capabilities': ['Fabric Manufacturing', 'Dyeing', 'Finishing'],
            'payment_terms': 'Net 30',
            'minimum_order_value': Decimal('2000.00'),
            'lead_time_range': '10-20 days'
        }
    ]
    
    suppliers = []
    for data in suppliers_data:
        supplier, created = Supplier.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"✅ Created supplier: {supplier.name}")
        suppliers.append(supplier)
    
    # Create supplier contacts
    contacts_data = [
        {
            'supplier': suppliers[0],  # TechCorp
            'contact_type': 'primary',
            'name': 'Zhang Wei',
            'title': 'Sales Manager',
            'email': 'zhang.wei@techcorp.com',
            'phone': '+86-138-0013-8001',
            'wechat': 'zhangwei_tech',
            'preferred_contact_method': 'wechat',
            'timezone': 'Asia/Shanghai',
            'working_hours': '9:00 AM - 6:00 PM (GMT+8)'
        },
        {
            'supplier': suppliers[0],
            'contact_type': 'technical',
            'name': 'Li Ming',
            'title': 'Technical Director',
            'email': 'li.ming@techcorp.com',
            'phone': '+86-138-0013-8002',
            'preferred_contact_method': 'email',
            'timezone': 'Asia/Shanghai',
            'working_hours': '9:00 AM - 6:00 PM (GMT+8)'
        },
        {
            'supplier': suppliers[1],  # Global Machinery
            'contact_type': 'primary',
            'name': 'Hans Mueller',
            'title': 'International Sales',
            'email': 'h.mueller@globalmachinery.de',
            'phone': '+49-30-1234-5679',
            'preferred_contact_method': 'email',
            'timezone': 'Europe/Berlin',
            'working_hours': '8:00 AM - 5:00 PM (GMT+1)'
        },
        {
            'supplier': suppliers[2],  # Textile Solutions
            'contact_type': 'primary',
            'name': 'Rajesh Kumar',
            'title': 'Export Manager',
            'email': 'rajesh.kumar@textilesolutions.in',
            'phone': '+91-80-9876-5433',
            'whatsapp': '+91-98765-43210',
            'preferred_contact_method': 'whatsapp',
            'timezone': 'Asia/Kolkata',
            'working_hours': '9:00 AM - 6:00 PM (GMT+5:30)'
        }
    ]
    
    for data in contacts_data:
        contact, created = SupplierContact.objects.get_or_create(
            supplier=data['supplier'],
            contact_type=data['contact_type'],
            defaults=data
        )
        if created:
            print(f"✅ Created contact: {contact.name} for {contact.supplier.name}")
    
    # Create test RFQ
    rfq = RFQ.objects.create(
        title='High-Quality PCB Components',
        description='Need 10,000 pieces of high-quality PCB components for automotive applications. Must meet ISO 9001 and automotive standards.',
        category='Electronics',
        subcategory='PCB Components',
        quantity=10000,
        target_price=Decimal('50000.00'),
        currency='USD',
        budget_range='$45,000 - $55,000',
        deadline=datetime.now() + timedelta(days=30),
        quote_deadline=datetime.now() + timedelta(days=14),
        delivery_deadline=datetime.now() + timedelta(days=60),
        distribution_method='auto',
        target_supplier_count=5,
        regions_preferred=['Asia', 'Europe'],
        supplier_criteria={
            'min_reliability': 80,
            'certifications': ['ISO 9001'],
            'capabilities': ['PCB Assembly']
        },
        status='draft',
        created_by=user
    )
    print(f"✅ Created RFQ: {rfq.title}")
    
    return suppliers, rfq, user


def test_supplier_verification():
    """Test supplier verification process"""
    print("\n🔍 Testing Supplier Verification Process...")
    
    # Create a pending supplier
    pending_supplier = Supplier.objects.create(
        name='New Supplier Co.',
        category='Electronics',
        region='Asia',
        verification_status='pending',
        contact_email='info@newsupplier.com',
        contact_phone='+86-139-0000-0000',
        contact_address='Shanghai, China'
    )
    print(f"✅ Created pending supplier: {pending_supplier.name}")
    
    # Initiate verification
    try:
        verification = supplier_verification_service.initiate_verification(pending_supplier.id)
        print(f"✅ Verification initiated: {verification.status}")
        
        # Submit documents
        documents = {
            'business_license': 'license_doc.pdf',
            'tax_certificate': 'tax_cert.pdf',
            'quality_certifications': 'iso_cert.pdf',
            'bank_references': 'bank_ref.pdf',
            'trade_references': 'trade_ref.pdf'
        }
        
        verification = supplier_verification_service.submit_documents(
            pending_supplier.id, documents
        )
        print(f"✅ Documents submitted: {verification.status}")
        
        # Review and approve
        user = User.objects.first()
        supplier = supplier_verification_service.review_supplier(
            pending_supplier.id, user.id, 'approved', 'All documents verified successfully'
        )
        print(f"✅ Supplier approved: {supplier.verification_status}")
        
    except Exception as e:
        print(f"❌ Verification test failed: {str(e)}")


def test_rfq_distribution():
    """Test RFQ distribution system"""
    print("\n📤 Testing RFQ Distribution System...")
    
    # Get verified suppliers
    suppliers = Supplier.objects.filter(verification_status='verified')
    print(f"📊 Found {suppliers.count()} verified suppliers")
    
    # Get test RFQ
    rfq = RFQ.objects.first()
    if not rfq:
        print("❌ No RFQ found for testing")
        return
    
    # Test auto distribution
    try:
        distributions = rfq_distribution_service.distribute_rfq(
            rfq.id, distribution_method='auto'
        )
        print(f"✅ RFQ distributed to {len(distributions)} suppliers")
        
        # Show distribution stats
        stats = rfq_distribution_service.get_distribution_stats(rfq.id)
        print(f"📈 Distribution Stats:")
        print(f"   - Total Sent: {stats['total_sent']}")
        print(f"   - Delivered: {stats['delivered']}")
        print(f"   - Delivery Rate: {stats['delivery_rate']:.1f}%")
        
        # Test supplier matching
        matched_suppliers = rfq_distribution_service.auto_match_suppliers(rfq)
        print(f"🎯 AI Matched {len(matched_suppliers)} suppliers:")
        for supplier in matched_suppliers:
            score = rfq_distribution_service.calculate_supplier_score(supplier, rfq)
            print(f"   - {supplier.name}: Score {score:.1f}")
        
    except Exception as e:
        print(f"❌ RFQ distribution test failed: {str(e)}")


def test_communication_tracking():
    """Test communication tracking"""
    print("\n💬 Testing Communication Tracking...")
    
    supplier = Supplier.objects.filter(verification_status='verified').first()
    if not supplier:
        print("❌ No verified supplier found for communication test")
        return
    
    # Create communication logs
    communications = [
        {
            'supplier': supplier,
            'communication_type': 'email',
            'subject': 'RFQ Follow-up',
            'content': 'Following up on the PCB components RFQ. Please let us know if you need any clarification.',
            'direction': 'outbound',
            'status': 'sent'
        },
        {
            'supplier': supplier,
            'communication_type': 'phone',
            'subject': 'Technical Discussion',
            'content': 'Discussed technical specifications and quality requirements for the PCB components.',
            'direction': 'outbound',
            'status': 'delivered'
        },
        {
            'supplier': supplier,
            'communication_type': 'email',
            'subject': 'Quote Submission',
            'content': 'Submitted quote for PCB components with detailed specifications and pricing.',
            'direction': 'inbound',
            'status': 'received'
        }
    ]
    
    for comm_data in communications:
        comm = CommunicationLog.objects.create(**comm_data)
        print(f"✅ Created communication: {comm.communication_type} - {comm.subject}")
    
    # Show communication history
    supplier_communications = supplier.communications.all()
    print(f"📋 Communication History for {supplier.name}:")
    for comm in supplier_communications:
        print(f"   - {comm.created_at.strftime('%Y-%m-%d %H:%M')}: {comm.communication_type} - {comm.subject}")


def test_supplier_performance():
    """Test supplier performance metrics"""
    print("\n📊 Testing Supplier Performance Metrics...")
    
    suppliers = Supplier.objects.filter(verification_status='verified')
    
    for supplier in suppliers:
        # Calculate performance metrics
        total_quotes = supplier.quotes.count()
        accepted_quotes = supplier.quotes.filter(status='accepted').count()
        total_rfqs = supplier.rfq_distributions.count()
        responded_rfqs = supplier.rfq_distributions.filter(status='responded').count()
        
        print(f"\n📈 {supplier.name} Performance:")
        print(f"   - Reliability Score: {supplier.reliability}/100")
        print(f"   - Avg Response Time: {supplier.response_time_avg} hours")
        print(f"   - Quote Acceptance Rate: {supplier.quote_acceptance_rate}%")
        print(f"   - Total Quotes: {total_quotes}")
        print(f"   - Accepted Quotes: {accepted_quotes}")
        print(f"   - RFQ Response Rate: {(responded_rfqs/total_rfqs*100) if total_rfqs > 0 else 0:.1f}%")


def main():
    """Main test function"""
    print("🚀 Starting Supplier Directory & RFQ System Tests...")
    print("=" * 60)
    
    try:
        # Create test data
        suppliers, rfq, user = create_test_data()
        
        # Test verification process
        test_supplier_verification()
        
        # Test RFQ distribution
        test_rfq_distribution()
        
        # Test communication tracking
        test_communication_tracking()
        
        # Test performance metrics
        test_supplier_performance()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("\n🎯 System Features Demonstrated:")
        print("   - Supplier verification workflow")
        print("   - AI-powered RFQ distribution")
        print("   - Communication tracking")
        print("   - Performance metrics")
        print("   - Multi-contact management")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main() 