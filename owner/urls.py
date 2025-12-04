from django.urls import path
from . import views

app_name = 'owner'

urlpatterns = [
    path('', views.owner_dashboard, name='dashboard'),
    path('payments/export/<int:year>/<int:month>/', views.export_payments_month, name='export_payments_month'),
    path('applications/', views.application_list, name='application_list'),
    path('applications/<int:app_id>/', views.application_detail, name='application_detail'),
    path('requests/', views.request_list, name='request_list'),
]
