from django.contrib import admin
from .models import Campaign, Recipient, EmailLog


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'status', 'created_at', 'started_at', 'completed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'subject']


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'campaign', 'created_at']
    list_filter = ['campaign', 'created_at']
    search_fields = ['email', 'name']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'campaign', 'status', 'sent_at', 'opened_at']
    list_filter = ['status', 'sent_at']
    search_fields = ['recipient__email']
