from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tenants import views as tenant_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('tenant/', include('tenants.urls')),
    path('owner/', include('owner.urls')),
    path('properties/', include('properties.urls')),
    path('requests/', include('requests.urls')),
    path('payments/', include('payments.urls')),

    # ❌ Removed duplicate root route
    path('', tenant_views.public_home, name='home'),

    # ✅ This will now properly handle /
    #path('', lambda request: redirect('/accounts/create-account/')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

