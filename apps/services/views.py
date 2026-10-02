from django.shortcuts import get_object_or_404, render
from .models import Service

def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, "services/list.html", {"services": services})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related_services = Service.objects.filter(is_active=True).exclude(pk=service.pk)[:4]
    return render(request, "services/detail.html", {"service": service, "related_services": related_services})
