# Vasantha Heights – Rental Management Platform

- A full-stack rental management application built with Django, featuring:

- Tenant Portal – account creation, OTP verification, online application, dashboard.

- Owner/Admin Portal – tenant management, document access, payments, requests.

- Secure data handling – masking sensitive PII, OTP-based account verification.

- Production-ready deployment on Render.

# Features
### Tenant Portal

- Create account with:

    - First name, last name, phone, email, address

    - Password + Confirm Password

    - OTP email verification

- Auto-generated application ID

- Enter property details, address, vehicle info, employment info, co-applicants, etc.

- Login, reset password, continue application anytime.

### Owner/Admin Portal

- View all tenants and applications

- View uploaded tenant documents

- Update backend information

- Export monthly reports

- Receive notifications on new requests

- Full access to sensitive fields (masked on UI)

## Tech Stack

- Backend: Django 6, Python 3.10+

- Frontend: HTML, CSS, JavaScript

- Database: SQLite (dev), PostgreSQL (prod – via Render recommended)

- Email: Django Email Backend (console for dev, SMTP for prod)

- Hosting: Render (Web Service + Static Files)

Project Structure

vasanthaheights/

│── accounts/     ### User model, registration, OTP, login
│── owner/            # Owner/admin portal
│── tenants/          # Tenant application workflow + dashboard
│── properties/       # Property units, floors, metadata
│── payments/         # Payment logs (future integration)
│── requests/         # Maintenance requests
│── static/           # CSS, JS, images
│── templates/        # HTML templates
│── media/            # Uploaded tenant files
│── vasanthaheights/  # Settings, URLs, WSGI, ASGI
│── manage.py

# Environment Setup (Local)
1. Create Virtual Environment

- python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

2. Install Dependencies

- pip install -r requirements.txt

3. Apply Migrations
- python manage.py makemigrations
- python manage.py migrate

4. Create Superuser
- python manage.py createsuperuser

5. Run Server
- python manage.py runserver

# Environment Variables

- Create a file called .env locally and NEVER commit it to GitHub.

- SECRET_KEY=your-secret-key-here

- DEBUG=True

- EMAIL_HOST=smtp.example.com

- EMAIL_HOST_USER=your-email

- EMAIL_HOST_PASSWORD=your-password

- EMAIL_PORT=587

- DEFAULT_FROM_EMAIL=no-reply@vasanthaheights.com

# Email Configuration
- Development

- Use console backend so OTP prints in terminal:

- EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

- Production (Render)

# Update:

- EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
- EMAIL_HOST = smtp.gmail.com
- EMAIL_PORT = 587
- EMAIL_HOST_USER = <gmail>
- EMAIL_HOST_PASSWORD = <app-password>
- EMAIL_USE_TLS = True

- Static Files (Render Deployment)
- Add to settings:
- STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Build Script:
- python manage.py collectstatic --noinput

# Gunicorn:
- gunicorn vasanthaheights.wsgi:application

# Deployment Steps (Render)

- Create New Web Service

- Connect GitHub repo

Choose:

Build Command:
pip install -r requirements.txt && python manage.py collectstatic --noinput

Start Command:
gunicorn vasanthaheights.wsgi:application

Add environment variables under Render > Environment

Deploy

Visit:
https://vasanthaheights.onrender.com

Production Notes

Logging out does not shut down the Render service.

Sensitive info (phone, email, leasing office info) should be stored in .env – not hardcoded.

Phase 2 enhancements will be integrated safely without breaking deployment.

Future Enhancements (Phase 2)

Tenant payment gateway

Owner dashboard charts/analytics

Lease agreement upload + e-sign

Maintenance request workflow

SMS OTP (Twilio)

Multiple applicants per unit

Improved UI/UX layout


User Browsers (Tenant / Owner / Admin)
                |
                v
       Render Web Service (Gunicorn + Django App)
                |
       ---------------------------------------------------------
       |                         |                            |
       v                         v                            v
  Frontend               Django App Layer         External Email Service
(HTML/CSS/JS)          (Accounts, Tenants,        (SMTP / Gmail / SES)
                       Owners, Properties)        - Sends OTP & Alerts
       |                         |
       v                         v
------------------------------------------------------------
                     Database Layer
            - Dev: SQLite | Prod: PostgreSQL (Render)
            - Key Tables:
              * accounts_user
              * accounts_emailotp
              * tenant_applications
              * tenant_documents
              * owner_units / properties
              * maintenance_requests
                |
                v
           Media Storage
     - Tenant uploaded files
     - Local (Render Disk) or S3 (optional)
