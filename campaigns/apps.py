from django.apps import AppConfig
import threading
import time
import requests
from django.conf import settings


class CampaignsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'campaigns'
    
    def ready(self):
        def keep_alive_ping():
            keep_alive_url = settings.KEEP_ALIVE_URL
            if not keep_alive_url:
                return
            
            while True:
                try:
                    time.sleep(300)
                    response = requests.get(keep_alive_url, timeout=10)
                    print(f"Keep-alive ping sent to {keep_alive_url} - Status: {response.status_code}")
                except Exception as e:
                    print(f"Keep-alive ping failed: {e}")
        
        if settings.KEEP_ALIVE_URL:
            thread = threading.Thread(target=keep_alive_ping, daemon=True)
            thread.start()
            print("Keep-alive ping thread started")
