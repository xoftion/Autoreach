from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from .models import Campaign, EmailLog


@shared_task
def send_campaign_emails(campaign_id):
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        campaign.status = 'sending'
        campaign.started_at = timezone.now()
        campaign.save()
        
        pending_logs = EmailLog.objects.filter(campaign=campaign, status='pending').order_by('id')
        
        for index, log in enumerate(pending_logs):
            countdown_seconds = index * campaign.send_interval_minutes * 60
            send_single_email.apply_async(args=[str(log.id), str(campaign_id)], countdown=countdown_seconds)
        
        total_time = len(pending_logs) * campaign.send_interval_minutes * 60
        mark_campaign_completed.apply_async(args=[str(campaign_id)], countdown=total_time + 60)
        
    except Campaign.DoesNotExist:
        pass


@shared_task
def mark_campaign_completed(campaign_id):
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        pending_count = EmailLog.objects.filter(campaign=campaign, status='pending').count()
        if pending_count == 0:
            campaign.status = 'completed'
            campaign.completed_at = timezone.now()
            campaign.save()
    except Campaign.DoesNotExist:
        pass


@shared_task
def send_single_email(log_id, campaign_id):
    try:
        log = EmailLog.objects.get(id=log_id)
        campaign = log.campaign
        recipient = log.recipient
        
        tracking_pixel = f'<img src="{settings.KEEP_ALIVE_URL}/track/{log.id}/" width="1" height="1" />' if settings.KEEP_ALIVE_URL else ''
        
        image_urls = []
        if campaign.image1:
            image_urls.append(f"{settings.KEEP_ALIVE_URL}{campaign.image1.url}" if settings.KEEP_ALIVE_URL else campaign.image1.url)
        if campaign.image2:
            image_urls.append(f"{settings.KEEP_ALIVE_URL}{campaign.image2.url}" if settings.KEEP_ALIVE_URL else campaign.image2.url)
        if campaign.image3:
            image_urls.append(f"{settings.KEEP_ALIVE_URL}{campaign.image3.url}" if settings.KEEP_ALIVE_URL else campaign.image3.url)
        
        html_content = campaign.html_content or generate_html_email(
            campaign.subject,
            campaign.message,
            recipient.name or 'Valued Customer',
            tracking_pixel,
            image_urls
        )
        
        subject = campaign.subject
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = recipient.email
        
        msg = EmailMultiAlternatives(subject, campaign.message, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        log.status = 'sent'
        log.sent_at = timezone.now()
        log.save()
        
    except Exception as e:
        log.status = 'failed'
        log.error_message = str(e)
        log.save()
        raise


def generate_html_email(subject, message, recipient_name, tracking_pixel='', image_urls=None):
    if image_urls is None:
        image_urls = []
    
    images_html = ''
    if image_urls:
        images_html = '<div style="margin: 20px 0;">'
        for img_url in image_urls:
            images_html += f'<img src="{img_url}" alt="Campaign Image" style="max-width: 100%; height: auto; margin: 10px 0; border-radius: 8px; display: block;" />'
        images_html += '</div>'
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }}
            .container {{ max-width: 600px; margin: 20px auto; background: white; padding: 30px; border-radius: 8px; }}
            .header {{ background: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ padding: 20px; line-height: 1.6; color: #333; }}
            .footer {{ background: #f8f9fa; padding: 15px; text-align: center; color: #666; font-size: 14px; border-radius: 0 0 8px 8px; }}
            .contact {{ color: #2563eb; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{subject}</h1>
            </div>
            <div class="content">
                <p>Dear {recipient_name},</p>
                <p>{message.replace(chr(10), '<br>')}</p>
                {images_html}
                <p>For questions, contact us at <a href="mailto:xoftionc@gmail.com" class="contact">xoftionc@gmail.com</a></p>
            </div>
            <div class="footer">
                <p>&copy; Xoftion Systems. All rights reserved.</p>
            </div>
        </div>
        {tracking_pixel}
    </body>
    </html>
    """
