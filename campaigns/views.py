from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
from .models import Campaign, Recipient, EmailLog
from .forms import CampaignForm
from .tasks import send_campaign_emails
import csv
import io


def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, 'campaigns/campaign_list.html', {'campaigns': campaigns})


def campaign_create(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.save()
            
            csv_file = request.FILES.get('csv_file')
            if csv_file:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                
                for row in reader:
                    email = row.get('email', '').strip()
                    name = row.get('name', '').strip()
                    if email:
                        Recipient.objects.get_or_create(
                            campaign=campaign,
                            email=email,
                            defaults={'name': name}
                        )
            
            for recipient in campaign.recipients.all():
                EmailLog.objects.create(campaign=campaign, recipient=recipient)
            
            messages.success(request, f'Campaign "{campaign.name}" created successfully!')
            return redirect('campaign_detail', pk=campaign.id)
    else:
        form = CampaignForm()
    
    return render(request, 'campaigns/campaign_form.html', {'form': form, 'action': 'Create'})


def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    recipients = campaign.recipients.all()
    email_logs = campaign.email_logs.all()
    
    stats = {
        'total': email_logs.count(),
        'sent': email_logs.filter(status='sent').count(),
        'pending': email_logs.filter(status='pending').count(),
        'failed': email_logs.filter(status='failed').count(),
        'opened': email_logs.filter(status='opened').count(),
    }
    
    return render(request, 'campaigns/campaign_detail.html', {
        'campaign': campaign,
        'recipients': recipients,
        'email_logs': email_logs,
        'stats': stats
    })


def campaign_start(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if campaign.status == 'draft' or campaign.status == 'paused':
        campaign.status = 'scheduled'
        campaign.save()
        send_campaign_emails.delay(str(campaign.id))
        messages.success(request, f'Campaign "{campaign.name}" started!')
    return redirect('campaign_detail', pk=campaign.id)


def track_open(request, log_id):
    try:
        log = EmailLog.objects.get(id=log_id)
        if log.status == 'sent':
            log.status = 'opened'
            log.opened_at = timezone.now()
            log.save()
    except EmailLog.DoesNotExist:
        pass
    
    pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    return HttpResponse(pixel, content_type='image/gif')
