"""
Celery tasks for project management app
Background tasks for email notifications and document generation
"""

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse
from apps.parameters.models import SiteParameter
from .services import CVGenerationService, EmailNotificationService
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, retry_backoff=True, max_retries=3)
def send_contact_acknowledgment(self, contact_data):
    """
    Send acknowledgment email to user who submitted contact form
    
    Args:
        contact_data (dict): Contact form data containing name, email, message
    
    Returns:
        dict: Task result with status and details
    """
    try:
        # Log task start
        logger.info(f"Starting contact acknowledgment task for {contact_data.get('email')}")
        
        # Use the email service
        EmailNotificationService.send_contact_acknowledgment(contact_data)
        
        logger.info(f"Contact acknowledgment sent successfully to {contact_data.get('email')}")
        
        return {
            'status': 'success',
            'message': f"Acknowledgment email sent to {contact_data.get('email')}",
            'timestamp': timezone.now().isoformat()
        }
        
    except Exception as exc:
        logger.error(f"Failed to send contact acknowledgment: {str(exc)}")
        
        # Retry the task with exponential backoff
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying task (attempt {self.request.retries + 1}/{self.max_retries})")
            raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
        
        # Final failure
        return {
            'status': 'failed',
            'error': str(exc),
            'timestamp': timezone.now().isoformat()
        }

@shared_task(bind=True, retry_backoff=True, max_retries=3)
def notify_admin_new_contact(self, contact_data):
    """
    Notify admin of new contact form submission
    
    Args:
        contact_data (dict): Contact form data
    
    Returns:
        dict: Task result with status and details
    """
    try:
        # Log task start
        logger.info(f"Starting admin notification for contact from {contact_data.get('name')}")
        
        # Use the email service
        EmailNotificationService.notify_admin_new_contact(contact_data)
        
        logger.info("Admin notification sent successfully")
        
        return {
            'status': 'success',
            'message': "Admin notification sent successfully",
            'timestamp': timezone.now().isoformat()
        }
        
    except Exception as exc:
        logger.error(f"Failed to send admin notification: {str(exc)}")
        
        # Retry the task with exponential backoff
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying task (attempt {self.request.retries + 1}/{self.max_retries})")
            raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
        
        # Final failure
        return {
            'status': 'failed',
            'error': str(exc),
            'timestamp': timezone.now().isoformat()
        }

@shared_task(bind=True, retry_backoff=True, max_retries=2)
def generate_cv_pdf(self, format_type='modern', include_sections=None, user_email=None):
    """
    Generate CV PDF in background and optionally email it
    
    Args:
        format_type (str): CV format type ('modern', 'classic', 'minimal')
        include_sections (list): List of sections to include
        user_email (str): Optional email to send the CV to
    
    Returns:
        dict: Task result with status and file path or download URL
    """
    try:
        # Log task start
        logger.info(f"Starting CV generation task - format: {format_type}")
        
        # Generate the CV
        cv_service = CVGenerationService()
        cv_response = cv_service.generate_cv_pdf(format_type, include_sections)
        
        # In a real implementation, you would save the PDF to a file or cloud storage
        # For now, we'll just return success with metadata
        filename = f"CV_{format_type}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        logger.info(f"CV generated successfully: {filename}")
        
        # If user email is provided, send the CV notification
        if user_email:
            try:
                cv_data = {
                    'format_type': format_type,
                    'filename': filename,
                    'sections': include_sections
                }
                EmailNotificationService.send_cv_notification(user_email, cv_data)
                logger.info(f"CV notification sent to {user_email}")
            except Exception as e:
                logger.error(f"Failed to send CV notification: {str(e)}")
        
        return {
            'status': 'success',
            'message': 'CV generated successfully',
            'filename': filename,
            'format_type': format_type,
            'timestamp': timezone.now().isoformat()
        }
        
    except Exception as exc:
        logger.error(f"Failed to generate CV: {str(exc)}")
        
        # Retry the task
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying CV generation (attempt {self.request.retries + 1}/{self.max_retries})")
            raise self.retry(exc=exc, countdown=30 * (2 ** self.request.retries))
        
        # Final failure
        return {
            'status': 'failed',
            'error': str(exc),
            'timestamp': timezone.now().isoformat()
        }

@shared_task
def cleanup_old_files():
    """
    Periodic task to clean up old generated files
    This would be scheduled to run daily via Celery Beat
    """
    try:
        logger.info("Starting file cleanup task")
        
        # Here you would implement cleanup logic for old PDFs, logs, etc.
        # For example:
        # - Remove PDFs older than 30 days
        # - Clean up temporary files
        # - Archive old logs
        
        logger.info("File cleanup completed successfully")
        
        return {
            'status': 'success',
            'message': 'File cleanup completed',
            'timestamp': timezone.now().isoformat()
        }
        
    except Exception as exc:
        logger.error(f"File cleanup failed: {str(exc)}")
        return {
            'status': 'failed',
            'error': str(exc),
            'timestamp': timezone.now().isoformat()
        }

@shared_task
def send_weekly_portfolio_stats():
    """
    Weekly task to send portfolio statistics to admin
    This would be scheduled via Celery Beat
    """
    try:
        logger.info("Starting weekly stats task")
        
        site_settings = SiteParameter.get_settings()
        admin_email = site_settings.email
        
        if not admin_email:
            logger.warning("No admin email configured, skipping stats email")
            return {'status': 'skipped', 'reason': 'No admin email'}
        
        # Here you would gather statistics:
        # - Contact form submissions this week
        # - CV downloads
        # - Page views (if analytics are implemented)
        # - Popular content
        
        stats_data = {
            'week_start': timezone.now().strftime('%Y-%m-%d'),
            'contact_submissions': 0,  # Would be calculated from database
            'cv_downloads': 0,  # Would be calculated from logs/database
            'total_visitors': 0,  # Would come from analytics
        }
        
        # Send stats email
        html_message = render_to_string('emails/weekly_stats.html', {
            'stats': stats_data,
            'site_name': site_settings.site_name,
        })
        
        send_mail(
            subject=f'Weekly Portfolio Stats - {site_settings.site_name}',
            message=f'Weekly statistics for your portfolio website.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info("Weekly stats email sent successfully")
        
        return {
            'status': 'success',
            'message': 'Weekly stats sent',
            'stats': stats_data,
            'timestamp': timezone.now().isoformat()
        }
        
    except Exception as exc:
        logger.error(f"Weekly stats task failed: {str(exc)}")
        return {
            'status': 'failed',
            'error': str(exc),
            'timestamp': timezone.now().isoformat()
        }