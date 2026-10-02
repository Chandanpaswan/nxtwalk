from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from apps.seo.sitemaps import CaseStudySitemap, PostSitemap, ProjectSitemap, ServiceSitemap, StaticSitemap

sitemaps = {
    "static": StaticSitemap,
    "services": ServiceSitemap,
    "blog": PostSitemap,
    "portfolio": ProjectSitemap,
    "case_studies": CaseStudySitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("accounts/", include("apps.accounts.urls")),
    path("services/", include("apps.services.urls")),
    path("blog/", include("apps.blog.urls")),
    path("portfolio/", include("apps.portfolio.urls")),
    path("case-studies/", include("apps.case_studies.urls")),
    path("contact/", include("apps.contact.urls")),
    path("", include("apps.website.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "apps.website.views.permission_denied"
handler404 = "apps.website.views.not_found"
handler500 = "apps.website.views.server_error"
