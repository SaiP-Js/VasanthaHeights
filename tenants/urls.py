from django.urls import path
from . import views

app_name = 'tenants'

urlpatterns = [
    path('', views.tenant_dashboard, name='dashboard'),
    path('apply/<int:unit_id>/', views.create_application, name='apply'),
    path('application/<int:app_id>/', views.application_detail, name='application_detail'),
    path('requests/', views.request_list, name='request_list'),
    path('requests/new/', views.create_request, name='create_request'),
    path('payments/', views.payment_history, name='payment_history'),
]
