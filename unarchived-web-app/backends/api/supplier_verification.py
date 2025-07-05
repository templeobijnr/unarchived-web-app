"""
Supplier Verification Service
Handles supplier verification and onboarding process
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from typing import List, Dict, Any
import logging

from .models import Supplier, SupplierVerification, SupplierContact, User

logger = logging.getLogger(__name__)


class SupplierVerificationService:
    """Handles supplier verification process"""
    
    def initiate_verification(self, supplier_id: int) -> SupplierVerification:
        """Start verification process for a supplier"""
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            
            # Create verification record
            verification = SupplierVerification.objects.create(
                supplier=supplier,
                status='initiated',
                documents_required=[
                    'business_license',
                    'tax_certificate', 
                    'quality_certifications',
                    'bank_references',
                    'trade_references'
                ]
            )
            
            # Send verification email
            self.send_verification_email(supplier, verification)
            
            logger.info(f"Verification initiated for supplier {supplier_id}")
            return verification
            
        except Supplier.DoesNotExist:
            logger.error(f"Supplier {supplier_id} not found")
            raise
        except Exception as e:
            logger.error(f"Error initiating verification for supplier {supplier_id}: {str(e)}")
            raise
    
    def submit_documents(self, supplier_id: int, documents: Dict[str, Any]) -> SupplierVerification:
        """Submit verification documents"""
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            verification = SupplierVerification.objects.get(supplier=supplier)
            
            # Store documents
            verification.documents_submitted = documents
            verification.status = 'documents_received'
            verification.save()
            
            # Notify verification team
            self.notify_verification_team(verification)
            
            logger.info(f"Documents submitted for supplier {supplier_id}")
            return verification
            
        except (Supplier.DoesNotExist, SupplierVerification.DoesNotExist) as e:
            logger.error(f"Supplier or verification not found: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error submitting documents for supplier {supplier_id}: {str(e)}")
            raise
    
    def review_supplier(self, supplier_id: int, reviewer_id: int, decision: str, notes: str = "") -> Supplier:
        """Review and approve/reject supplier"""
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            reviewer = User.objects.get(id=reviewer_id)
            
            if decision == 'approved':
                supplier.verification_status = 'verified'
                supplier.verification_date = timezone.now()
                supplier.verified_by = reviewer
            else:
                supplier.verification_status = 'rejected'
            
            supplier.save()
            
            # Update verification record
            verification = SupplierVerification.objects.get(supplier=supplier)
            verification.status = decision
            verification.reviewer = reviewer
            verification.review_notes = notes
            verification.review_date = timezone.now()
            verification.save()
            
            # Notify supplier
            self.notify_supplier_decision(supplier, decision, notes)
            
            logger.info(f"Supplier {supplier_id} {decision} by reviewer {reviewer_id}")
            return supplier
            
        except (Supplier.DoesNotExist, User.DoesNotExist) as e:
            logger.error(f"Supplier or reviewer not found: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error reviewing supplier {supplier_id}: {str(e)}")
            raise
    
    def send_verification_email(self, supplier: Supplier, verification: SupplierVerification):
        """Send verification initiation email to supplier"""
        try:
            context = {
                'supplier': supplier,
                'verification': verification,
                'verification_url': f"https://platform.com/supplier/verify/{supplier.id}",
            }
            
            subject = "Welcome to Our Sourcing Platform - Verification Required"
            text_message = self.generate_verification_email_text(context)
            html_message = self.generate_verification_email_html(context)
            
            send_mail(
                subject=subject,
                message=text_message,
                from_email='noreply@platform.com',
                recipient_list=[supplier.contact_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Verification email sent to supplier {supplier.id}")
            
        except Exception as e:
            logger.error(f"Failed to send verification email to supplier {supplier.id}: {str(e)}")
    
    def generate_verification_email_text(self, context: Dict[str, Any]) -> str:
        """Generate plain text verification email"""
        supplier = context['supplier']
        
        return f"""
Dear {supplier.name},

Welcome to our sourcing platform! We're excited to have you join our network of trusted suppliers.

To complete your registration and start receiving RFQ opportunities, we need to verify your business credentials.

Required Documents:
- Business License
- Tax Certificate
- Quality Certifications (ISO, CE, etc.)
- Bank References
- Trade References

Please visit the following link to submit your documents:
{context['verification_url']}

Our verification team will review your submission within 3-5 business days.

If you have any questions, please don't hesitate to contact us.

Best regards,
The Verification Team
        """.strip()
    
    def generate_verification_email_html(self, context: Dict[str, Any]) -> str:
        """Generate HTML verification email"""
        supplier = context['supplier']
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .header {{ background-color: #f8f9fa; padding: 20px; }}
        .content {{ padding: 20px; }}
        .button {{ background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
        .documents {{ background-color: #f8f9fa; padding: 15px; margin: 15px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>Welcome to Our Sourcing Platform!</h2>
    </div>
    
    <div class="content">
        <p>Dear {supplier.name},</p>
        
        <p>Welcome to our sourcing platform! We're excited to have you join our network of trusted suppliers.</p>
        
        <p>To complete your registration and start receiving RFQ opportunities, we need to verify your business credentials.</p>
        
        <div class="documents">
            <h3>Required Documents:</h3>
            <ul>
                <li>Business License</li>
                <li>Tax Certificate</li>
                <li>Quality Certifications (ISO, CE, etc.)</li>
                <li>Bank References</li>
                <li>Trade References</li>
            </ul>
        </div>
        
        <p style="margin-top: 30px;">
            <a href="{context['verification_url']}" class="button">
                Submit Verification Documents
            </a>
        </p>
        
        <p>Our verification team will review your submission within 3-5 business days.</p>
        
        <p>If you have any questions, please don't hesitate to contact us.</p>
        
        <p>Best regards,<br>The Verification Team</p>
    </div>
</body>
</html>
        """.strip()
    
    def notify_verification_team(self, verification: SupplierVerification):
        """Notify verification team of new document submission"""
        try:
            # Get verification team members (you can customize this logic)
            verification_team = User.objects.filter(
                groups__name='verification_team'
            ).values_list('email', flat=True)
            
            if not verification_team:
                # Fallback to admin users
                verification_team = User.objects.filter(
                    is_staff=True
                ).values_list('email', flat=True)
            
            if verification_team:
                context = {
                    'verification': verification,
                    'supplier': verification.supplier,
                    'review_url': f"https://platform.com/admin/verify/{verification.id}",
                }
                
                subject = f"New Supplier Verification: {verification.supplier.name}"
                text_message = self.generate_team_notification_text(context)
                
                send_mail(
                    subject=subject,
                    message=text_message,
                    from_email='noreply@platform.com',
                    recipient_list=list(verification_team),
                    fail_silently=False,
                )
                
                logger.info(f"Verification team notified about supplier {verification.supplier.id}")
                
        except Exception as e:
            logger.error(f"Failed to notify verification team: {str(e)}")
    
    def generate_team_notification_text(self, context: Dict[str, Any]) -> str:
        """Generate team notification text"""
        verification = context['verification']
        supplier = context['supplier']
        
        return f"""
New supplier verification documents submitted:

Supplier: {supplier.name}
Email: {supplier.contact_email}
Category: {supplier.category}
Region: {supplier.region}

Documents submitted: {', '.join(verification.documents_submitted.keys())}

Review URL: {context['review_url']}

Please review the submitted documents and approve or reject the supplier.
        """.strip()
    
    def notify_supplier_decision(self, supplier: Supplier, decision: str, notes: str):
        """Notify supplier of verification decision"""
        try:
            context = {
                'supplier': supplier,
                'decision': decision,
                'notes': notes,
            }
            
            if decision == 'approved':
                subject = "Verification Approved - Welcome to Our Platform!"
                text_message = self.generate_approval_email_text(context)
                html_message = self.generate_approval_email_html(context)
            else:
                subject = "Verification Update - Additional Information Required"
                text_message = self.generate_rejection_email_text(context)
                html_message = self.generate_rejection_email_html(context)
            
            send_mail(
                subject=subject,
                message=text_message,
                from_email='noreply@platform.com',
                recipient_list=[supplier.contact_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Decision notification sent to supplier {supplier.id}")
            
        except Exception as e:
            logger.error(f"Failed to send decision notification to supplier {supplier.id}: {str(e)}")
    
    def generate_approval_email_text(self, context: Dict[str, Any]) -> str:
        """Generate approval email text"""
        supplier = context['supplier']
        
        return f"""
Dear {supplier.name},

Great news! Your verification has been approved.

You are now a verified supplier on our platform and can start receiving RFQ opportunities.

Next steps:
1. Complete your supplier profile
2. Set up your product catalog
3. Configure your notification preferences

You can access your supplier dashboard at: https://platform.com/supplier/dashboard

Welcome to our network!

Best regards,
The Verification Team
        """.strip()
    
    def generate_approval_email_html(self, context: Dict[str, Any]) -> str:
        """Generate approval email HTML"""
        supplier = context['supplier']
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .header {{ background-color: #28a745; color: white; padding: 20px; }}
        .content {{ padding: 20px; }}
        .button {{ background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>🎉 Verification Approved!</h2>
    </div>
    
    <div class="content">
        <p>Dear {supplier.name},</p>
        
        <p>Great news! Your verification has been approved.</p>
        
        <p>You are now a verified supplier on our platform and can start receiving RFQ opportunities.</p>
        
        <h3>Next steps:</h3>
        <ol>
            <li>Complete your supplier profile</li>
            <li>Set up your product catalog</li>
            <li>Configure your notification preferences</li>
        </ol>
        
        <p style="margin-top: 30px;">
            <a href="https://platform.com/supplier/dashboard" class="button">
                Access Your Dashboard
            </a>
        </p>
        
        <p>Welcome to our network!</p>
        
        <p>Best regards,<br>The Verification Team</p>
    </div>
</body>
</html>
        """.strip()
    
    def generate_rejection_email_text(self, context: Dict[str, Any]) -> str:
        """Generate rejection email text"""
        supplier = context['supplier']
        notes = context['notes']
        
        return f"""
Dear {supplier.name},

Thank you for your interest in joining our platform. After reviewing your submitted documents, we need additional information to complete your verification.

Notes from our review team:
{notes}

Please review the feedback above and resubmit your documents with the requested information.

You can update your submission at: https://platform.com/supplier/verify/{supplier.id}

If you have any questions, please don't hesitate to contact our support team.

Best regards,
The Verification Team
        """.strip()
    
    def generate_rejection_email_html(self, context: Dict[str, Any]) -> str:
        """Generate rejection email HTML"""
        supplier = context['supplier']
        notes = context['notes']
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .header {{ background-color: #ffc107; color: #212529; padding: 20px; }}
        .content {{ padding: 20px; }}
        .button {{ background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
        .notes {{ background-color: #f8f9fa; padding: 15px; margin: 15px 0; border-left: 4px solid #ffc107; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>📋 Additional Information Required</h2>
    </div>
    
    <div class="content">
        <p>Dear {supplier.name},</p>
        
        <p>Thank you for your interest in joining our platform. After reviewing your submitted documents, we need additional information to complete your verification.</p>
        
        <div class="notes">
            <h3>Notes from our review team:</h3>
            <p>{notes}</p>
        </div>
        
        <p>Please review the feedback above and resubmit your documents with the requested information.</p>
        
        <p style="margin-top: 30px;">
            <a href="https://platform.com/supplier/verify/{supplier.id}" class="button">
                Update Your Submission
            </a>
        </p>
        
        <p>If you have any questions, please don't hesitate to contact our support team.</p>
        
        <p>Best regards,<br>The Verification Team</p>
    </div>
</body>
</html>
        """.strip()
    
    def get_verification_stats(self) -> Dict[str, Any]:
        """Get verification statistics"""
        total_suppliers = Supplier.objects.count()
        pending_verifications = Supplier.objects.filter(verification_status='pending').count()
        verified_suppliers = Supplier.objects.filter(verification_status='verified').count()
        rejected_suppliers = Supplier.objects.filter(verification_status='rejected').count()
        
        stats = {
            'total_suppliers': total_suppliers,
            'pending_verifications': pending_verifications,
            'verified_suppliers': verified_suppliers,
            'rejected_suppliers': rejected_suppliers,
            'verification_rate': (verified_suppliers / total_suppliers * 100) if total_suppliers > 0 else 0,
        }
        
        return stats


# Create service instance
supplier_verification_service = SupplierVerificationService() 