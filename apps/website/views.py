from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils import timezone
from apps.blog.models import Post
from apps.case_studies.models import CaseStudy
from apps.contact.models import ContactMessage, ProjectEnquiry
from apps.portfolio.models import Project
from apps.services.models import Service
from apps.testimonials.models import Testimonial
from .forms import NewsletterForm
from .models import NewsletterSubscriber, Page


def home(request):
    posts = Post.objects.filter(status=Post.PUBLISHED, published_at__lte=timezone.now()).select_related("author")[:3]
    return render(request, "website/home.html", {
        "services": Service.objects.filter(is_active=True)[:8],
        "projects": Project.objects.filter(is_published=True)[:3],
        "case_studies": CaseStudy.objects.filter(is_published=True, project__is_published=True).select_related("project")[:2],
        "testimonials": Testimonial.objects.filter(is_published=True)[:3],
        "posts": posts,
    })

def about(request):
    return render(request, "website/about.html")


def privacy(request):
    return render(request, "website/privacy.html")


def terms(request):
    return render(request, "website/terms.html")


def content_page(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, "website/page.html", {"page": page})


def newsletter_subscribe(request):
    if request.method != "POST":
        return redirect("website:home")
    form = NewsletterForm(request.POST)
    if form.is_valid():
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=form.cleaned_data["email"],
            defaults={"name": form.cleaned_data.get("name", ""), "is_active": True},
        )
        if not created:
            changed_fields = []
            submitted_name = form.cleaned_data.get("name", "")
            if submitted_name and subscriber.name != submitted_name:
                subscriber.name = submitted_name
                changed_fields.append("name")
            if not subscriber.is_active:
                subscriber.is_active = True
                changed_fields.append("is_active")
            if changed_fields:
                subscriber.save(update_fields=changed_fields)
        messages.success(request, "You're on the list. Thanks for subscribing.")
    else:
        messages.error(request, "Please enter a valid email address to subscribe.")
    next_url = request.POST.get("next", "")
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return redirect(next_url)
    return redirect("website:home")


def html_sitemap(request):
    return render(request, "website/sitemap.html", {
        "services": Service.objects.filter(is_active=True),
        "posts": Post.objects.filter(status=Post.PUBLISHED, published_at__lte=timezone.now()),
        "projects": Project.objects.filter(is_published=True),
        "case_studies": CaseStudy.objects.filter(is_published=True, project__is_published=True).select_related("project"),
    })


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    return HttpResponse(
        f"User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /admin-dashboard/\nDisallow: /accounts/\n\nSitemap: {sitemap_url}\n",
        content_type="text/plain",
    )


def not_found(request, exception):
    return render(request, "404.html", status=404)


def permission_denied(request, exception):
    return render(request, "403.html", status=403)


def server_error(request):
    return render(request, "500.html", status=500)


@staff_member_required
def admin_dashboard(request):
    return render(request, "website/admin_dashboard.html", {
        "total_leads": ContactMessage.objects.count() + ProjectEnquiry.objects.count(),
        "new_leads": ContactMessage.objects.filter(status=ContactMessage.NEW).count() + ProjectEnquiry.objects.filter(status=ProjectEnquiry.NEW).count(),
        "contacted_leads": ContactMessage.objects.filter(status=ContactMessage.CONTACTED).count() + ProjectEnquiry.objects.filter(status=ProjectEnquiry.CONTACTED).count(),
        "converted_leads": ContactMessage.objects.filter(status=ContactMessage.CONVERTED).count() + ProjectEnquiry.objects.filter(status=ProjectEnquiry.CONVERTED).count(),
        "blog_count": Post.objects.filter(status=Post.PUBLISHED, published_at__lte=timezone.now()).count(),
        "service_count": Service.objects.filter(is_active=True).count(),
        "project_count": Project.objects.filter(is_published=True).count(),
        "subscriber_count": NewsletterSubscriber.objects.filter(is_active=True).count(),
        "recent_messages": ContactMessage.objects.select_related("service")[:6],
        "recent_project_enquiries": ProjectEnquiry.objects.select_related("service")[:6],
    })
