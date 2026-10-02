from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from apps.blog.models import Post
from apps.case_studies.models import CaseStudy
from apps.portfolio.models import Project
from apps.services.models import Service


class StaticSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return [
            "website:home",
            "website:about",
            "services:list",
            "blog:list",
            "portfolio:list",
            "case_studies:list",
            "contact:contact",
            "website:privacy",
            "website:terms",
        ]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_active=True)

    def location(self, item):
        return reverse("services:detail", kwargs={"slug": item.slug})


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.objects.filter(status=Post.PUBLISHED, published_at__lte=timezone.now())

    def lastmod(self, item):
        return item.updated_at

    def location(self, item):
        return reverse("blog:detail", kwargs={"slug": item.slug})


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Project.objects.filter(is_published=True)

    def lastmod(self, item):
        return item.updated_at

    def location(self, item):
        return reverse("portfolio:detail", kwargs={"slug": item.slug})


class CaseStudySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return CaseStudy.objects.filter(is_published=True, project__is_published=True).select_related("project")

    def location(self, item):
        return reverse("case_studies:detail", kwargs={"slug": item.project.slug})