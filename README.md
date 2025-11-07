# Xoftion AutoReach - Email Distribution System

A full-stack Django email distribution system that automatically sends company updates, software product releases, and promotional content to multiple users via email.

## Features

- **Campaign Management**: Create and manage email campaigns with rich content
- **CSV Import**: Upload recipient lists via CSV files
- **HTML Email Generation**: Automatically converts plain text to professional HTML emails
- **Scheduled Sending**: Send emails one by one with configurable intervals (default: 10 minutes)
- **Image Attachments**: Support for up to 3 images per campaign
- **Open Tracking**: Track when recipients open emails using tracking pixels
- **Email Logging**: Complete logs of send time, recipient, and success/failure status
- **Keep-Alive System**: Built-in ping mechanism to prevent Render app from sleeping
- **Async Processing**: Uses Celery and Redis for background email sending

## Tech Stack

- **Backend**: Django 4.2.7
- **Task Queue**: Celery 5.3.4
- **Cache/Broker**: Redis 5.0.1
- **Database**: SQLite (default, easily switchable to PostgreSQL)
- **Email**: SMTP (Gmail or custom domain)
- **Deployment**: Docker, Render-ready

## Project Structure

```
autoreach/
├── campaigns/              # Main Django app
│   ├── models.py          # Campaign, Recipient, EmailLog models
│   ├── views.py           # Campaign management views
│   ├── forms.py           # Campaign creation forms
│   ├── tasks.py           # Celery tasks for email sending
│   ├── apps.py            # Keep-alive ping logic
│   └── templates/         # HTML templates
├── autoreach/             # Django project settings
│   ├── settings.py        # Project configuration
│   ├── celery.py          # Celery configuration
│   └── urls.py            # URL routing
├── start.sh               # Production startup script
├── build.sh               # Build/migration script
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
└── .env.example           # Environment variable template
```

## Setup Instructions

### 1. Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required variables:
- `EMAIL_HOST_USER`: Your email address (e.g., Gmail)
- `EMAIL_HOST_PASSWORD`: Your email app password
- `KEEP_ALIVE_URL`: Your deployed app URL (for Render keep-alive)
- `REDIS_URL`: Redis connection URL (default: redis://localhost:6379/0)

### 2. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver 0.0.0.0:5000

# In separate terminals, start Redis and Celery:
redis-server
celery -A autoreach worker --loglevel=info
```

### 3. Docker Deployment

```bash
# Build Docker image
docker build -t xoftion-autoreach .

# Run container
docker run -p 5000:5000 --env-file .env xoftion-autoreach
```

### 4. Render Deployment

1. Create a new Web Service on Render
2. Connect your Git repository
3. Configure environment variables in Render dashboard
4. Set build command: `./build.sh`
5. Set start command: `./start.sh`
6. Deploy!

**Important for Render**:
- Set `KEEP_ALIVE_URL` to your Render app URL (e.g., `https://your-app.onrender.com`)
- The keep-alive ping runs every 5 minutes to prevent app from sleeping
- Make sure to configure email credentials in environment variables

## Usage

### Creating a Campaign

1. Navigate to the home page
2. Click "Create New Campaign"
3. Fill in campaign details:
   - Campaign name
   - Email subject
   - Message content
   - Send interval (minutes between emails)
   - Upload up to 3 images (optional)
   - Upload CSV file with recipient emails

### CSV Format

Your CSV file should have the following format:

```csv
email,name
john@example.com,John Doe
jane@example.com,Jane Smith
```

### Starting a Campaign

1. Go to the campaign detail page
2. Click "Start Campaign"
3. Emails will be sent automatically based on the configured interval
4. Monitor progress in real-time on the campaign detail page

### Email Features

Each email includes:
- Professional HTML design
- Recipient name in greeting
- Your campaign message
- Company branding (Xoftion Systems)
- Contact email (xoftionc@gmail.com)
- Auto footer with copyright
- Optional tracking pixel for open tracking

## Keep-Alive System

The keep-alive system is hardcoded in `campaigns/apps.py`. When the Django app starts:
- A background thread is created
- Every 5 minutes, it pings the `KEEP_ALIVE_URL`
- This prevents Render from putting the app to sleep
- No manual intervention required

## Admin Interface

Access the Django admin at `/admin/` to:
- View all campaigns
- Manage recipients
- Check email logs
- Monitor send status

## Email Configuration

### Gmail Setup

1. Enable 2-factor authentication on your Google account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Create a new app password
3. Use this app password in `EMAIL_HOST_PASSWORD`

### Custom Domain

Update these settings in `.env`:
```
EMAIL_HOST=smtp.yourdomain.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-password
```

## Monitoring

- **Campaign Dashboard**: View all campaigns and their status
- **Email Logs**: Track every email sent, including timestamps
- **Open Tracking**: See which recipients opened emails
- **Error Handling**: Failed emails are logged with error messages

## Security Notes

- Never commit `.env` file to version control
- Keep `EMAIL_HOST_PASSWORD` secure
- Use strong `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Configure `ALLOWED_HOSTS` appropriately

## Troubleshooting

### Emails not sending
- Check email credentials in `.env`
- Verify Redis is running
- Check Celery worker logs
- Ensure SMTP settings are correct

### Keep-alive not working
- Verify `KEEP_ALIVE_URL` is set correctly
- Check app logs for ping messages
- Ensure the URL is accessible

### Docker issues
- Make sure Redis is included in container
- Verify all environment variables are passed
- Check logs: `docker logs <container-id>`

## License

© Xoftion Systems. All rights reserved.

## Support

For questions or issues, contact: xoftionc@gmail.com
