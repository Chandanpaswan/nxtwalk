from django.db import migrations


SOCIAL_LINKS = [
    ("instagram", "Instagram", "https://www.instagram.com/nxtwalk/", 1),
    ("facebook", "Facebook", "https://www.facebook.com/nxtwalk", 2),
    ("x", "X", "https://x.com/nxtwalk", 3),
    ("linkedin", "LinkedIn", "https://www.linkedin.com/company/nxtwalk/", 4),
    ("youtube", "YouTube", "https://www.youtube.com/@nxtwalk", 5),
]

NAVIGATION_ITEMS = [
    ("Home", "/", 1, False),
    ("About", "/about/", 2, False),
    ("Services", "/services/", 3, False),
    ("Work", "/portfolio/", 4, False),
    ("Case Studies", "/case-studies/", 5, False),
    ("Blog", "/blog/", 6, False),
    ("Contact", "/contact/", 7, False),
    ("Start a Project", "/contact/project/", 8, True),
]


def seed_site_controls(apps, schema_editor):
    alias = schema_editor.connection.alias
    SiteSettings = apps.get_model("website", "SiteSettings")
    FooterSettings = apps.get_model("website", "FooterSettings")
    SocialLink = apps.get_model("website", "SocialLink")
    NavigationItem = apps.get_model("website", "NavigationItem")

    site_settings = SiteSettings.objects.using(alias).order_by("pk").first()
    if site_settings is None:
        SiteSettings.objects.using(alias).create(
            pk=1,
            organization_name="NXTWALK",
            tagline="Build. Grow. Walk Ahead.",
            whatsapp_number="+917015907650",
            footer_description="Digital systems for the next generation.",
        )
    elif not site_settings.whatsapp_number:
        SiteSettings.objects.using(alias).filter(pk=site_settings.pk).update(whatsapp_number="+917015907650")

    if not FooterSettings.objects.using(alias).exists():
        FooterSettings.objects.using(alias).create(
            pk=1,
            description="Digital systems for the next generation.",
        )

    for platform, name, url, display_order in SOCIAL_LINKS:
        SocialLink.objects.using(alias).get_or_create(
            platform=platform,
            defaults={
                "name": name,
                "url": url,
                "icon": platform,
                "display_order": display_order,
                "is_active": True,
                "open_new_tab": True,
            },
        )

    for title, url, display_order, is_cta in NAVIGATION_ITEMS:
        NavigationItem.objects.using(alias).get_or_create(
            title=title,
            defaults={
                "url": url,
                "display_order": display_order,
                "is_active": True,
                "is_cta": is_cta,
            },
        )


class Migration(migrations.Migration):
    dependencies = [("website", "0003_footersettings_navigationitem_newslettersubscriber_and_more")]

    operations = [migrations.RunPython(seed_site_controls, migrations.RunPython.noop)]