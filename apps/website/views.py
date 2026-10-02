from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from apps.blog.models import Post
from apps.case_studies.models import CaseStudy
from apps.portfolio.models import Project
from apps.services.models import Service
from apps.testimonials.models import Testimonial


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
    from apps.contact.models import ContactMessage

    return render(request, "website/admin_dashboard.html", {
        "unread_messages": ContactMessage.objects.filter(is_read=False).count(),
        "open_messages": ContactMessage.objects.filter(is_contacted=False).count(),
        "service_count": Service.objects.filter(is_active=True).count(),
        "post_count": Post.objects.filter(status=Post.PUBLISHED, published_at__lte=timezone.now()).count(),
        "recent_messages": ContactMessage.objects.select_related("service")[:6],
    })
