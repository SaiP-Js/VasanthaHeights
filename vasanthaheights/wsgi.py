import os

# Render will override this environment variable
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE","vasanthaheights.settings_prod"
)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
