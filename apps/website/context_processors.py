from apps.services.models import Service
from .models import FooterLink, FooterSettings, NavigationItem, Page, SiteSettings, SocialLink


def site_settings(request):
    settings = SiteSettings.objects.first()
    footer_settings = FooterSettings.objects.first()
    social_links = SocialLink.objects.filter(is_active=True).order_by("display_order", "name")
    active_navigation = NavigationItem.objects.filter(is_active=True).order_by("display_order", "id")
    return {
        "site_settings": settings,
        "footer_settings": footer_settings,
        "social_links": social_links,
        "navigation_items": active_navigation.filter(is_cta=False),
        "navigation_cta": active_navigation.filter(is_cta=True).first(),
        "footer_services": Service.objects.filter(is_active=True).order_by("title")[:6],
        "footer_pages": Page.objects.filter(is_published=True).order_by("title")[:4],
        "footer_company_links": FooterLink.objects.filter(section=FooterLink.COMPANY, is_active=True),
        "footer_service_links": FooterLink.objects.filter(section=FooterLink.SERVICES, is_active=True),
        "footer_resource_links": FooterLink.objects.filter(section=FooterLink.RESOURCES, is_active=True),
    }