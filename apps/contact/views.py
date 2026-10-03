from django.contrib import messages
from django.shortcuts import redirect, render
from apps.services.models import Service
from .forms import ContactForm, ProjectEnquiryForm

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you. Your message has been received.")
            return redirect("contact:contact")
    else:
        form = ContactForm()
        service_slug = request.GET.get("service", "").strip()
        if service_slug:
            service = Service.objects.filter(slug=service_slug, is_active=True).first()
            if service:
                form.initial["service"] = service.pk
    return render(request, "contact/contact.html", {
        "form": form,
        "services": form.fields["service"].queryset,
    })


def project_enquiry(request):
    form = ProjectEnquiryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Thanks. Your project enquiry has been sent to our team.")
        return redirect("contact:project_enquiry")
    return render(request, "contact/project_enquiry.html", {"form": form})
