import csv
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404

from tenants.models import TenantApplication
from requests.models import TenantRequest
from payments.models import Payment


@staff_member_required
def owner_dashboard(request):
    apps = TenantApplication.objects.order_by('-created_at')[:10]
    open_requests = TenantRequest.objects.filter(status='OPEN')
    recent_payments = Payment.objects.order_by('-paid_at')[:10]
    return render(request, 'owner/dashboard.html', {
        'applications': apps,
        'open_requests': open_requests,
        'recent_payments': recent_payments,
    })


@staff_member_required
def export_payments_month(request, year, month):
    payments = Payment.objects.filter(paid_at__year=year, paid_at__month=month)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="payments_{year}_{month}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Tenant', 'Unit', 'Amount', 'Mode', 'Transaction Ref', 'Paid At'])
    for p in payments:
        writer.writerow([p.tenant.email, str(p.unit), p.amount, p.mode, p.transaction_ref, p.paid_at])
    return response


@staff_member_required
def application_list(request):
    apps = TenantApplication.objects.order_by('-created_at')
    return render(request, 'owner/application_list.html', {'applications': apps})


@staff_member_required
def application_detail(request, app_id):
    app = get_object_or_404(TenantApplication, id=app_id)
    return render(request, 'owner/tenant_detail.html', {'application': app})


@staff_member_required
def request_list(request):
    reqs = TenantRequest.objects.order_by('-created_at')
    return render(request, 'owner/requests_list.html', {'requests': reqs})
