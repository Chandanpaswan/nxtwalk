from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("organization_name", "contact_email", "updated_at")
    fieldsets = (
        ("Organization", {"fields": ("organization_name", "tagline", "contact_email", "phone", "address")}),
        ("Social profiles", {"fields": ("linkedin_url", "instagram_url", "facebook_url", "x_url")}),
    )

    def has_add_permission(self, request):
        return super().has_add_permission(request) and not SiteSettings.objects.exists()