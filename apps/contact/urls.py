from django.urls import path
from . import views

app_name = "contact"

urlpatterns = [
    path("project/", views.project_enquiry, name="project_enquiry"),
    path("", views.contact, name="contact"),
]
