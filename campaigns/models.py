from django.db import models
from django.utils import timezone
import uuid


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField(help_text="Campaign description or message content")
    html_content = models.TextField(blank=True, help_text="Auto-generated HTML content")
    
    image1 = models.ImageField(upload_to='campaign_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='campaign_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='campaign_images/', blank=True, null=True)
    
    send_interval_minutes = models.IntegerField(default=10, help_text="Minutes between each email send")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Recipient(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='recipients')
    email = models.EmailField()
    name = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['id']
        unique_together = ['campaign', 'email']
    
    def __str__(self):
        return f"{self.name or 'No Name'} <{self.email}>"


class EmailLog(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('opened', 'Opened'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='email_logs')
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='email_logs')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"Email to {self.recipient.email} - {self.status}"
