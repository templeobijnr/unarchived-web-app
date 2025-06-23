"""
RFQ Distribution Service
Handles automated RFQ distribution to suppliers
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models import Q
from typing import List, Dict, Any
import logging

from .models import RFQ, Supplier, RFQDistribution, CommunicationLog

logger = logging.getLogger(__name__)


class RFQDistributionService:
    """Handles RFQ distribution to suppliers"""
    
    def distribute_rfq(self, rfq_id: int, distribution_method: str = 'auto', 
                      manual_supplier_ids: List[int] = None) -> List[RFQDistribution]:
        """
        Distribute RFQ to relevant suppliers
        
        Args:
            rfq_id: ID of the RFQ to distribute
            distribution_method: 'auto', 'manual', or 'hybrid'
            manual_supplier_ids: List of supplier IDs for manual distribution
        
        Returns:
            List of RFQDistribution objects
        """
        try:
            rfq = RFQ.objects.get(id=rfq_id)
            
            if distribution_method == 'auto':
                suppliers = self.auto_match_suppliers(rfq)
            elif distribution_method == 'manual':
                suppliers = self.get_manually_selected_suppliers(rfq, manual_supplier_ids)
            else:  # hybrid
                suppliers = self.hybrid_match_suppliers(rfq, manual_supplier_ids)
            
            # Create distribution records
            distributions = []
            for supplier in suppliers:
                distribution = RFQDistribution.objects.create(
                    rfq=rfq,
                    supplier=supplier,
                    status='sent',
                    sent_at=timezone.now()
                )
                distributions.append(distribution)
                
                # Send RFQ to supplier
                self.send_rfq_to_supplier(rfq, supplier, distribution)
                
                # Log communication
                self.log_communication(rfq, supplier, distribution)
            
            # Update RFQ status
            rfq.status = 'distributed'
            rfq.published_at = timezone.now()
            rfq.save()
            
            logger.info(f"RFQ {rfq_id} distributed to {len(suppliers)} suppliers")
            return distributions
            
        except RFQ.DoesNotExist:
            logger.error(f"RFQ {rfq_id} not found")
            raise
        except Exception as e:
            logger.error(f"Error distributing RFQ {rfq_id}: {str(e)}")
            raise
    
    def auto_match_suppliers(self, rfq: RFQ) -> List[Supplier]:
        """AI-powered supplier matching"""
        # Get verified suppliers in relevant categories
        suppliers = Supplier.objects.filter(
            verification_status='verified',
            reliability__gte=70  # Minimum reliability threshold
        )
        
        # Filter by category (check both category and categories fields)
        category_filter = Q(category=rfq.category) | Q(categories__contains=[rfq.category])
        suppliers = suppliers.filter(category_filter)
        
        # Apply region filter if specified
        if rfq.regions_preferred:
            suppliers = suppliers.filter(region__in=rfq.regions_preferred)
        
        # Score and rank suppliers
        scored_suppliers = []
        for supplier in suppliers:
            score = self.calculate_supplier_score(supplier, rfq)
            scored_suppliers.append((supplier, score))
        
        # Sort by score and return top matches
        scored_suppliers.sort(key=lambda x: x[1], reverse=True)
        return [supplier for supplier, score in scored_suppliers[:rfq.target_supplier_count]]
    
    def get_manually_selected_suppliers(self, rfq: RFQ, supplier_ids: List[int]) -> List[Supplier]:
        """Get manually selected suppliers"""
        if not supplier_ids:
            return []
        
        suppliers = Supplier.objects.filter(
            id__in=supplier_ids,
            verification_status='verified'
        )
        return list(suppliers)
    
    def hybrid_match_suppliers(self, rfq: RFQ, manual_supplier_ids: List[int] = None) -> List[Supplier]:
        """Combine AI matching with manual selection"""
        auto_suppliers = self.auto_match_suppliers(rfq)
        manual_suppliers = self.get_manually_selected_suppliers(rfq, manual_supplier_ids or [])
        
        # Combine and remove duplicates
        all_suppliers = auto_suppliers + manual_suppliers
        unique_suppliers = list({supplier.id: supplier for supplier in all_suppliers}.values())
        
        return unique_suppliers[:rfq.target_supplier_count]
    
    def calculate_supplier_score(self, supplier: Supplier, rfq: RFQ) -> float:
        """Calculate supplier relevance score for RFQ"""
        score = 0.0
        
        # Category match (40%)
        if rfq.category == supplier.category or rfq.category in supplier.categories:
            score += 40
        
        # Reliability score (30%)
        score += (supplier.reliability * 0.3)
        
        # Response time (20%)
        if supplier.response_time_avg <= 24:
            score += 20
        elif supplier.response_time_avg <= 48:
            score += 15
        elif supplier.response_time_avg <= 72:
            score += 10
        
        # Quote acceptance rate (10%)
        score += float(supplier.quote_acceptance_rate * 0.1)
        
        return score
    
    def send_rfq_to_supplier(self, rfq: RFQ, supplier: Supplier, distribution: RFQDistribution):
        """Send RFQ notification to supplier"""
        try:
            # Email template context
            context = {
                'rfq': rfq,
                'supplier': supplier,
                'distribution': distribution,
                'rfq_url': f"https://platform.com/rfq/{rfq.id}",
                'supplier_dashboard_url': f"https://platform.com/supplier/rfq/{rfq.id}",
            }
            
            # Generate email content
            subject = f"New RFQ: {rfq.title}"
            text_message = self.generate_rfq_email_text(context)
            html_message = self.generate_rfq_email_html(context)
            
            # Send email
            send_mail(
                subject=subject,
                message=text_message,
                from_email='noreply@platform.com',
                recipient_list=[supplier.contact_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # Update distribution record
            distribution.email_sent = True
            distribution.status = 'delivered'
            distribution.delivered_at = timezone.now()
            distribution.save()
            
            logger.info(f"RFQ email sent to supplier {supplier.id}")
            
        except Exception as e:
            logger.error(f"Failed to send RFQ email to supplier {supplier.id}: {str(e)}")
            distribution.status = 'failed'
            distribution.save()
    
    def generate_rfq_email_text(self, context: Dict[str, Any]) -> str:
        """Generate plain text email content"""
        rfq = context['rfq']
        supplier = context['supplier']
        
        return f"""
Dear {supplier.name},

We have a new Request for Quote (RFQ) that matches your capabilities:

RFQ Title: {rfq.title}
Category: {rfq.category}
Quantity: {rfq.quantity:,}
Target Price: {rfq.currency} {rfq.target_price}
Deadline: {rfq.deadline.strftime('%B %d, %Y')}

Description:
{rfq.description}

To view the complete RFQ and submit your quote, please visit:
{context['supplier_dashboard_url']}

Please respond by: {rfq.quote_deadline.strftime('%B %d, %Y') if rfq.quote_deadline else rfq.deadline.strftime('%B %d, %Y')}

Best regards,
The Sourcing Platform Team
        """.strip()
    
    def generate_rfq_email_html(self, context: Dict[str, Any]) -> str:
        """Generate HTML email content"""
        rfq = context['rfq']
        supplier = context['supplier']
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .header {{ background-color: #f8f9fa; padding: 20px; }}
        .content {{ padding: 20px; }}
        .rfq-details {{ background-color: #f8f9fa; padding: 15px; margin: 15px 0; }}
        .button {{ background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>New RFQ Opportunity</h2>
    </div>
    
    <div class="content">
        <p>Dear {supplier.name},</p>
        
        <p>We have a new Request for Quote (RFQ) that matches your capabilities:</p>
        
        <div class="rfq-details">
            <h3>{rfq.title}</h3>
            <p><strong>Category:</strong> {rfq.category}</p>
            <p><strong>Quantity:</strong> {rfq.quantity:,}</p>
            <p><strong>Target Price:</strong> {rfq.currency} {rfq.target_price}</p>
            <p><strong>Deadline:</strong> {rfq.deadline.strftime('%B %d, %Y')}</p>
        </div>
        
        <p><strong>Description:</strong></p>
        <p>{rfq.description}</p>
        
        <p style="margin-top: 30px;">
            <a href="{context['supplier_dashboard_url']}" class="button">
                View RFQ & Submit Quote
            </a>
        </p>
        
        <p><strong>Response Deadline:</strong> {rfq.quote_deadline.strftime('%B %d, %Y') if rfq.quote_deadline else rfq.deadline.strftime('%B %d, %Y')}</p>
        
        <p>Best regards,<br>The Sourcing Platform Team</p>
    </div>
</body>
</html>
        """.strip()
    
    def log_communication(self, rfq: RFQ, supplier: Supplier, distribution: RFQDistribution):
        """Log RFQ communication"""
        CommunicationLog.objects.create(
            supplier=supplier,
            communication_type='rfq',
            subject=f"RFQ: {rfq.title}",
            content=f"RFQ distributed to supplier. Distribution ID: {distribution.id}",
            direction='outbound',
            related_rfq=rfq,
            status='sent'
        )
    
    def track_rfq_view(self, rfq_id: int, supplier_id: int):
        """Track when supplier views RFQ"""
        try:
            distribution = RFQDistribution.objects.get(
                rfq_id=rfq_id,
                supplier_id=supplier_id
            )
            
            if distribution.status == 'delivered':
                distribution.status = 'viewed'
                distribution.viewed_at = timezone.now()
                distribution.save()
                
                # Update RFQ view count
                rfq = distribution.rfq
                rfq.views += 1
                rfq.save()
                
                logger.info(f"RFQ {rfq_id} viewed by supplier {supplier_id}")
                
        except RFQDistribution.DoesNotExist:
            logger.warning(f"RFQ distribution not found for RFQ {rfq_id} and supplier {supplier_id}")
    
    def track_rfq_response(self, rfq_id: int, supplier_id: int):
        """Track when supplier responds to RFQ"""
        try:
            distribution = RFQDistribution.objects.get(
                rfq_id=rfq_id,
                supplier_id=supplier_id
            )
            
            distribution.status = 'responded'
            distribution.responded_at = timezone.now()
            distribution.save()
            
            # Update RFQ response count
            rfq = distribution.rfq
            rfq.responses += 1
            rfq.save()
            
            logger.info(f"RFQ {rfq_id} responded by supplier {supplier_id}")
            
        except RFQDistribution.DoesNotExist:
            logger.warning(f"RFQ distribution not found for RFQ {rfq_id} and supplier {supplier_id}")
    
    def get_distribution_stats(self, rfq_id: int) -> Dict[str, Any]:
        """Get RFQ distribution statistics"""
        distributions = RFQDistribution.objects.filter(rfq_id=rfq_id)
        
        stats = {
            'total_sent': distributions.count(),
            'delivered': distributions.filter(status='delivered').count(),
            'viewed': distributions.filter(status='viewed').count(),
            'responded': distributions.filter(status='responded').count(),
            'failed': distributions.filter(status='failed').count(),
        }
        
        stats['delivery_rate'] = (stats['delivered'] / stats['total_sent'] * 100) if stats['total_sent'] > 0 else 0
        stats['response_rate'] = (stats['responded'] / stats['total_sent'] * 100) if stats['total_sent'] > 0 else 0
        
        return stats


# Create service instance
rfq_distribution_service = RFQDistributionService() 