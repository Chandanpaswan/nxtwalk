import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import FooterLink, FooterSettings, NavigationItem, NewsletterSubscriber, Page, SiteSettings, SocialLink


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("organization_name", "contact_email", "whatsapp_number", "updated_at")
    fieldsets = (
        ("Identity", {"fields": ("organization_name", "logo", "favicon", "tagline", "footer_description", "website_url")}),
        ("Contact", {"fields": ("contact_email", "phone", "whatsapp_number", "address", "city", "country", "business_hours", "google_maps_url")}),
        ("Search and analytics", {"fields": ("default_seo_title", "default_meta_description", "default_keywords", "default_og_image", "google_analytics_id", "search_console_verification")}),
    )

    def has_add_permission(self, request):
        return super().has_add_permission(request) and not SiteSettings.objects.exists()


@admin.register(FooterSettings)
class FooterSettingsAdmin(admin.ModelAdmin):
    list_display = ("show_social_links", "show_whatsapp", "show_email", "show_phone", "updated_at")
    fieldsets = (
        ("Footer content", {"fields": ("logo", "description", "copyright_text")}),
        ("Visibility", {"fields": ("show_social_links", "show_whatsapp", "show_email", "show_phone", "show_address")}),
    )

    def has_add_permission(self, request):
        return super().has_add_permission(request) and not FooterSettings.objects.exists()


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "url", "external_url", "is_active", "display_order")
    list_filter = ("section", "is_active", "is_external")
    list_editable = ("is_active", "display_order")
    search_fields = ("title", "url", "external_url")
    ordering = ("section", "display_order", "id")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "platform", "url", "is_active", "display_order", "open_new_tab")
    list_filter = ("platform", "is_active", "open_new_tab")
    list_editable = ("is_active", "display_order")
    search_fields = ("name", "url")
    ordering = ("display_order", "name")
    list_per_page = 30
    actions = ("activate_links", "deactivate_links")

    @admin.action(description="Enable selected social links")
    def activate_links(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Disable selected social links")
    def deactivate_links(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "external_url", "is_active", "is_cta", "display_order")
    list_filter = ("is_active", "is_external")
    list_editable = ("is_active", "is_cta", "display_order")
    search_fields = ("title", "url", "external_url")
    ordering = ("display_order", "id")


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "is_active", "subscribed_at")
    list_filter = ("is_active", "subscribed_at")
    list_editable = ("is_active",)
    search_fields = ("email", "name")
    date_hierarchy = "subscribed_at"
    actions = ("export_subscribers",)

    @admin.action(description="Export selected subscribers as CSV")
    def export_subscribers(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="nxtwalk-subscribers.csv"'
        writer = csv.writer(response)
        writer.writerow(("email", "name", "active", "subscribed_at"))
        for subscriber in queryset.iterator():
            writer.writerow((subscriber.email, subscriber.name, subscriber.is_active, subscriber.subscribed_at.isoformat()))
        return response


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "updated_at")
    list_filter = ("is_published", "updated_at")
    list_editable = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "content", "keywords")
    date_hierarchy = "updated_at"