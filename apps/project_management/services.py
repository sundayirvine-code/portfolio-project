"""
Services for project management app
Includes CV generation, email notifications, and other business logic
"""

import os
import json
from io import BytesIO
from datetime import date
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
try:
    import weasyprint
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"WeasyPrint not available: {e}. CV generation will use fallback method.")
from apps.parameters.models import SiteParameter, ProfessionalJourney


class CVGenerationService:
    """Service for generating ATS-friendly PDF CVs"""
    
    def __init__(self):
        self.site_settings = SiteParameter.get_settings()
    
    def generate_cv_pdf(self, format_type='modern', include_sections=None):
        """
        Generate a PDF CV using dynamic data with fallbacks
        
        Args:
            format_type (str): CV format type ('modern', 'classic', 'minimal')
            include_sections (list): List of sections to include
        
        Returns:
            HttpResponse: PDF response
        """
        # Get CV data with fallbacks
        cv_data = self._get_cv_data()
        
        # Set default sections if not provided
        if include_sections is None:
            include_sections = [
                'header', 'summary', 'experience', 
                'education', 'skills', 'contact'
            ]
        
        # Select appropriate template
        template_name = f'cv/{format_type}_cv.html'
        if not self._template_exists(template_name):
            template_name = 'cv/modern_cv.html'  # fallback
        
        # Render HTML
        html_content = render_to_string(template_name, {
            'cv_data': cv_data,
            'include_sections': include_sections,
            'generated_date': timezone.now().date(),
            'format_type': format_type
        })
        
        # Generate PDF
        return self._html_to_pdf(html_content, cv_data['name'])
    
    def _get_cv_data(self):
        """Get CV data with fallbacks to default content"""
        
        # Basic information
        cv_data = {
            'name': self.site_settings.owner_name or 'Professional Name',
            'title': self.site_settings.owner_title or 'Full Stack Developer',
            'email': self.site_settings.email or 'contact@example.com',
            'phone': self.site_settings.phone or '+1 (555) 123-4567',
            'location': self.site_settings.location or 'City, State',
            'website': self.site_settings.site_url or 'www.example.com',
            'summary': self.site_settings.bio or self._get_default_summary(),
        }
        
        # Professional journey
        cv_data['experience'] = self._get_experience_data()
        cv_data['education'] = self._get_education_data()
        cv_data['skills'] = self._get_skills_data()
        cv_data['achievements'] = self._get_achievements_data()
        
        # Social links
        cv_data['social'] = {
            'linkedin': self.site_settings.linkedin_url,
            'github': self.site_settings.github_url,
            'twitter': self.site_settings.twitter_url,
        }
        
        return cv_data
    
    def _get_experience_data(self):
        """Get work experience data with fallbacks"""
        experience = []
        
        # Get from database
        work_entries = ProfessionalJourney.objects.filter(
            entry_type='work',
            is_active=True
        ).order_by('-start_date')
        
        for entry in work_entries:
            experience.append({
                'title': entry.title,
                'company': entry.company,
                'location': entry.location,
                'start_date': entry.start_date,
                'end_date': entry.end_date,
                'is_current': entry.is_current,
                'duration': entry.duration,
                'description': entry.description,
                'achievements': entry.achievements_list,
                'technologies': entry.technologies_list,
            })
        
        # Fallback if no data
        if not experience:
            experience = self._get_default_experience()
        
        return experience
    
    def _get_education_data(self):
        """Get education data with fallbacks"""
        education = []
        
        # Get from database
        edu_entries = ProfessionalJourney.objects.filter(
            entry_type='education',
            is_active=True
        ).order_by('-start_date')
        
        for entry in edu_entries:
            education.append({
                'degree': entry.title,
                'institution': entry.company,
                'location': entry.location,
                'start_date': entry.start_date,
                'end_date': entry.end_date,
                'description': entry.description,
                'achievements': entry.achievements_list,
            })
        
        # Fallback if no data
        if not education:
            education = self._get_default_education()
        
        return education
    
    def _get_skills_data(self):
        """Get skills data with fallbacks"""
        skills_data = {}
        
        # Try to get from new skills_expertise field
        try:
            if hasattr(self.site_settings, 'skills_expertise') and self.site_settings.skills_expertise:
                skills_list = self.site_settings.skills_expertise
                if isinstance(skills_list, str):
                    skills_list = json.loads(skills_list)
                
                # Group skills by category for CV format
                skills_data = {}
                for skill in skills_list:
                    category = skill.get('category', 'other')
                    if category not in skills_data:
                        skills_data[category] = []
                    skills_data[category].append({
                        'name': skill.get('name'),
                        'level': skill.get('level', 0),
                        'description': skill.get('description', '')
                    })
        except (json.JSONDecodeError, TypeError, AttributeError):
            pass
        
        # Fallback to default skills if no data found
        if not skills_data:
            skills_data = self._get_default_skills()
        
        return skills_data
    
    def _get_achievements_data(self):
        """Get achievements data with fallbacks"""
        achievements = []
        
        # Get certification and achievement entries
        achievement_entries = ProfessionalJourney.objects.filter(
            entry_type__in=['certification', 'achievement'],
            is_active=True
        ).order_by('-start_date')
        
        for entry in achievement_entries:
            achievements.append({
                'title': entry.title,
                'organization': entry.company,
                'date': entry.start_date,
                'description': entry.description,
            })
        
        # Fallback if no data
        if not achievements:
            achievements = self._get_default_achievements()
        
        return achievements
    
    def _html_to_pdf(self, html_content, filename_prefix):
        """Convert HTML to PDF using WeasyPrint or fallback method"""
        if WEASYPRINT_AVAILABLE:
            try:
                # Create PDF using WeasyPrint
                pdf_file = weasyprint.HTML(string=html_content).write_pdf()
                
                # Create response
                response = HttpResponse(
                    pdf_file,
                    content_type='application/pdf'
                )
                
                # Set filename
                filename = f"{filename_prefix.replace(' ', '_')}_CV_{date.today().strftime('%Y%m%d')}.pdf"
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                
                return response
            except Exception as e:
                # Log the error for debugging
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"WeasyPrint PDF generation failed: {e}")
                raise Exception(f"Error generating PDF with WeasyPrint: {str(e)}")
        else:
            # Fallback: Return HTML response with print instructions
            return self._html_fallback_response(html_content, filename_prefix)
    
    def _html_fallback_response(self, html_content, filename_prefix):
        """Fallback method when WeasyPrint is not available - return HTML for printing"""
        # Create a print-friendly HTML response
        print_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{filename_prefix} - CV</title>
            <style>
                @media print {{
                    body {{ margin: 0; }}
                    .no-print {{ display: none !important; }}
                }}
                .print-instructions {{
                    background: #fff3cd;
                    border: 1px solid #ffecb5;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 20px;
                    text-align: center;
                }}
                .cv-content {{
                    margin: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="print-instructions no-print">
                <h3>🖨️ PDF Generation Not Available</h3>
                <p>WeasyPrint is not properly configured. To save as PDF:</p>
                <ol>
                    <li>Press <kbd>Ctrl+P</kbd> (or <kbd>Cmd+P</kbd> on Mac)</li>
                    <li>Select "Save as PDF" as the destination</li>
                    <li>Choose appropriate print settings</li>
                    <li>Click "Save"</li>
                </ol>
                <button onclick="window.print()" class="btn btn-primary">🖨️ Print Now</button>
            </div>
            <div class="cv-content">
                {html_content}
            </div>
            <script>
                // Auto-trigger print dialog after page loads
                window.addEventListener('load', function() {{
                    setTimeout(function() {{
                        if (confirm('PDF generation is not available. Would you like to print the CV instead?')) {{
                            window.print();
                        }}
                    }}, 1000);
                }});
            </script>
        </body>
        </html>
        """
        
        response = HttpResponse(print_html, content_type='text/html')
        return response
    
    def _template_exists(self, template_name):
        """Check if template exists"""
        try:
            from django.template.loader import get_template
            get_template(template_name)
            return True
        except:
            return False
    
    # Fallback data methods
    def _get_default_summary(self):
        return """Experienced Full Stack Developer with a passion for creating innovative web applications and solving complex technical challenges. Proven track record of delivering high-quality software solutions using modern technologies and best practices. Strong problem-solving skills and ability to work effectively in collaborative team environments."""
    
    def _get_default_experience(self):
        return [
            {
                'title': 'Senior Full Stack Developer',
                'company': 'Tech Company Inc.',
                'location': 'City, State',
                'start_date': date(2022, 1, 1),
                'end_date': None,
                'is_current': True,
                'duration': '2+ years',
                'description': 'Lead development of scalable web applications using modern frameworks and technologies.',
                'achievements': [
                    'Developed and deployed 5+ production applications',
                    'Improved application performance by 40%',
                    'Mentored junior developers and established coding standards'
                ],
                'technologies': ['Python', 'Django', 'React', 'PostgreSQL', 'Docker'],
            },
            {
                'title': 'Frontend Developer',
                'company': 'Digital Agency',
                'location': 'City, State',
                'start_date': date(2020, 6, 1),
                'end_date': date(2021, 12, 31),
                'is_current': False,
                'duration': '1 year 6 months',
                'description': 'Created responsive web interfaces and interactive user experiences.',
                'achievements': [
                    'Built 10+ responsive websites',
                    'Improved user engagement by 25%',
                    'Collaborated with design team on UX improvements'
                ],
                'technologies': ['JavaScript', 'Vue.js', 'CSS3', 'Bootstrap'],
            }
        ]
    
    def _get_default_education(self):
        return [
            {
                'degree': 'Bachelor of Science in Computer Science',
                'institution': 'University of Technology',
                'location': 'City, State',
                'start_date': date(2016, 9, 1),
                'end_date': date(2020, 5, 31),
                'description': 'Graduated Magna Cum Laude with focus on Software Engineering',
                'achievements': [
                    'GPA: 3.8/4.0',
                    'Dean\'s List for 6 semesters',
                    'Computer Science Department Award'
                ],
            }
        ]
    
    def _get_default_skills(self):
        return {
            'programming_languages': [
                'Python', 'JavaScript', 'TypeScript', 'Java', 'C++'
            ],
            'frameworks_libraries': [
                'Django', 'React', 'Vue.js', 'Node.js', 'Express'
            ],
            'databases': [
                'PostgreSQL', 'MongoDB', 'Redis', 'MySQL'
            ],
            'tools_technologies': [
                'Docker', 'Git', 'AWS', 'CI/CD', 'Linux'
            ],
            'soft_skills': [
                'Problem Solving', 'Team Leadership', 'Communication',
                'Project Management', 'Mentoring'
            ]
        }
    
    def _get_default_achievements(self):
        return [
            {
                'title': 'AWS Certified Solutions Architect',
                'organization': 'Amazon Web Services',
                'date': date(2023, 6, 1),
                'description': 'Professional-level certification in cloud architecture',
            },
            {
                'title': 'Best Innovation Award',
                'organization': 'Tech Company Inc.',
                'date': date(2023, 12, 1),
                'description': 'Recognition for developing innovative solution that improved efficiency',
            }
        ]


class EmailNotificationService:
    """Service for sending email notifications using EmailMultiAlternatives"""
    
    @staticmethod
    def send_contact_acknowledgment(contact_data):
        """Send acknowledgment email for contact form submission"""
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string
        from django.utils import timezone
        
        # Add timestamp to contact data
        enhanced_contact_data = {
            **contact_data,
            'timestamp': timezone.now(),
            'message_preview': contact_data['message'][:100] + '...' if len(contact_data['message']) > 100 else contact_data['message'],
        }
        
        # Render HTML template
        html_content = render_to_string('emails/contact_acknowledgment.html', enhanced_contact_data)
        
        # Plain text fallback
        text_content = f"""
Dear {contact_data['name']},

Thank you for reaching out! We have received your message and will respond within 24 hours.

Your Message:
"{enhanced_contact_data['message_preview']}"

Best regards,
The Portfolio Team

---
This is an automated message. Please do not reply to this email.
        """.strip()
        
        # Create email message
        subject = f"Thank you for contacting us, {contact_data['name']}!"
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[contact_data['email']],
        )
        
        # Attach HTML alternative
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        email.send(fail_silently=False)
    
    @staticmethod
    def notify_admin_new_contact(contact_data):
        """Notify admin of new contact form submission"""
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string
        from django.utils import timezone
        
        # Get admin email
        site_settings = SiteParameter.get_settings()
        admin_email = site_settings.email
        
        if not admin_email:
            return
        
        # Add timestamp to contact data
        enhanced_contact_data = {
            **contact_data,
            'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        }
        
        # Render HTML template
        html_content = render_to_string('emails/admin_contact_notification.html', {
            'contact_data': enhanced_contact_data,
        })
        
        # Plain text fallback
        text_content = f"""
🚨 NEW CONTACT FORM SUBMISSION 🚨

Contact Information:
- Name: {contact_data['name']}
- Email: {contact_data['email']}
- Subject: {contact_data.get('subject', 'No subject provided')}
- Phone: {contact_data.get('phone', 'Not provided')}
- Received: {enhanced_contact_data['timestamp']}

Message:
{contact_data['message']}

---
Reply to: {contact_data['email']}
        """.strip()
        
        # Create email message
        subject = f"🚨 New Contact: {contact_data['name']} - {contact_data.get('subject', 'General Inquiry')}"
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[admin_email],
            reply_to=[contact_data['email']],  # Enable direct reply
        )
        
        # Attach HTML alternative
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        email.send(fail_silently=False)
    
    @staticmethod
    def send_cv_notification(user_email, cv_data):
        """Send CV generation notification with download link"""
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string
        from django.utils import timezone
        
        # Render HTML template (create this template)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Your CV is Ready!</title>
        </head>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 20px; border-radius: 8px; text-align: center;">
                <h1>Your CV is Ready! 🎉</h1>
            </div>
            
            <div style="padding: 20px; background: #f8f9fa; margin: 20px 0; border-radius: 8px;">
                <h2>CV Details:</h2>
                <ul>
                    <li><strong>Format:</strong> {cv_data.get('format_type', 'Modern').title()}</li>
                    <li><strong>Generated:</strong> {timezone.now().strftime('%Y-%m-%d %H:%M UTC')}</li>
                    <li><strong>Filename:</strong> {cv_data.get('filename', 'CV.pdf')}</li>
                </ul>
            </div>
            
            <p>Your professionally formatted CV has been generated successfully! You can download it using the link below:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="#" style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 15px 30px; text-decoration: none; border-radius: 6px; font-weight: bold;">Download Your CV</a>
            </div>
            
            <p><small>This link will be valid for 7 days. If you need to regenerate your CV, please visit our website.</small></p>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #dee2e6;">
            
            <p style="text-align: center; color: #6c757d; font-size: 14px;">
                Thank you for using our CV generation service!<br>
                <strong>Portfolio Team</strong>
            </p>
        </body>
        </html>
        """
        
        # Plain text fallback
        text_content = f"""
Your CV is Ready! 🎉

CV Details:
- Format: {cv_data.get('format_type', 'Modern').title()}
- Generated: {timezone.now().strftime('%Y-%m-%d %H:%M UTC')}
- Filename: {cv_data.get('filename', 'CV.pdf')}

Your professionally formatted CV has been generated successfully!

This notification confirms that your CV generation request has been completed.

Thank you for using our CV generation service!

---
Portfolio Team
        """.strip()
        
        # Create email message
        subject = f"✅ Your {cv_data.get('format_type', 'Modern').title()} CV is Ready!"
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email],
        )
        
        # Attach HTML alternative
        email.attach_alternative(html_content, "text/html")
        
        # TODO: In production, attach the actual PDF file
        # email.attach_file(cv_file_path)
        
        # Send email
        email.send(fail_silently=False)