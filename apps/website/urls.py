from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("pages/<slug:slug>/", views.content_page, name="page"),
    path("newsletter/subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"),
    path("sitemap/", views.html_sitemap, name="html_sitemap"),
    path("robots.txt", views.robots_txt, name="robots"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
