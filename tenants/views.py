from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from properties.models import Unit
from .models import TenantApplication, Vehicle, HouseholdMember
from payments.models import Payment
from requests.models import TenantRequest


def public_home(request):
    return render(request, 'tenant/public_home.html')


@login_required
def tenant_dashboard(request):
    app = TenantApplication.objects.filter(user=request.user).order_by('-created_at').first()
    payments = Payment.objects.filter(tenant=request.user).order_by('-paid_at')[:10]
    reqs = TenantRequest.objects.filter(tenant=request.user).order_by('-created_at')[:10]
    return render(request, 'tenant/dashboard.html', {
        'application': app,
        'payments': payments,
        'requests': reqs,
    })


@login_required
def create_application(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)

    if request.method == 'POST':
        app = TenantApplication.objects.create(
            user=request.user,
            unit=unit,
            gender=request.POST['gender'],
            applicant_type=request.POST['applicant_type'],
            email=request.user.email,
            phone=request.user.phone,
            current_address=request.POST['current_address'],
            current_home_type=request.POST['current_home_type'],
            reason_for_leaving=request.POST['reason_for_leaving'],
            current_move_in_date=request.POST['current_move_in_date'],
            current_monthly_rent=request.POST['current_monthly_rent'],
            area_name=request.POST['area_name'],
            aadhaar_number=request.POST['aadhaar_number'],
            driving_license_number=request.POST['driving_license_number'],
            employer_name=request.POST.get('employer_name', ''),
            employer_address=request.POST.get('employer_address', ''),
            job_title=request.POST.get('job_title', ''),
            monthly_income=request.POST.get('monthly_income') or None,
        )

        vehicle_count = int(request.POST.get('vehicle_count', 0))
        for i in range(vehicle_count):
            prefix = f'vehicle_{i}_'
            Vehicle.objects.create(
                application=app,
                make=request.POST[prefix + 'make'],
                model=request.POST[prefix + 'model'],
                year=request.POST[prefix + 'year'],
                color=request.POST[prefix + 'color'],
                plate_number=request.POST[prefix + 'plate_number'],
                registered_state=request.POST[prefix + 'registered_state'],
            )

        member_count = int(request.POST.get('member_count', 0))
        for i in range(member_count):
            prefix = f'member_{i}_'
            HouseholdMember.objects.create(
                application=app,
                name=request.POST[prefix + 'name'],
                birthday=request.POST[prefix + 'birthday'],
                email=request.POST.get(prefix + 'email', ''),
                relationship=request.POST[prefix + 'relationship'],
            )

        messages.success(request, f"Application submitted. ID: {app.application_id}")
        return redirect('tenants:application_detail', app_id=app.id)

    return render(request, 'tenant/application_form.html', {'unit': unit})


@login_required
def application_detail(request, app_id):
    app = get_object_or_404(TenantApplication, id=app_id, user=request.user)
    return render(request, 'tenant/application_detail.html', {'application': app})


@login_required
def request_list(request):
    reqs = TenantRequest.objects.filter(tenant=request.user).order_by('-created_at')
    return render(request, 'tenant/requests_list.html', {'requests': reqs})


@login_required
def create_request(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        unit = TenantApplication.objects.filter(user=request.user).first().unit

        TenantRequest.objects.create(
            tenant=request.user,
            unit=unit,
            title=title,
            description=description,
        )
        messages.success(request, "Request created.")
        return redirect('tenants:request_list')

    return render(request, 'tenant/request_new.html')


@login_required
def payment_history(request):
    pays = Payment.objects.filter(tenant=request.user).order_by('-paid_at')
    return render(request, 'tenant/payments_list.html', {'payments': pays})
