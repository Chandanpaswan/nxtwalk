from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("sitemap/", views.html_sitemap, name="html_sitemap"),
    path("robots.txt", views.robots_txt, name="robots"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
