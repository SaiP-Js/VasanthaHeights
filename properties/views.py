from django.shortcuts import render
from .models import Property


def property_list(request):
    props = Property.objects.all()
    return render(request, 'properties/list.html', {'properties': props})
