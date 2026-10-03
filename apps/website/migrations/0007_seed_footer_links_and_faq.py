from django.db import migrations


FOOTER_LINKS = [
    ("company", "About", "/about/", 1),
    ("company", "Services", "/services/", 2),
    ("company", "Work", "/portfolio/", 3),
    ("company", "Blog", "/blog/", 4),
    ("company", "Contact", "/contact/", 5),
    ("services", "Web Development", "/services/website-development/", 1),
    ("services", "UI / UX", "/services/web-design/", 2),
    ("services", "Django / Python", "/services/django-development/", 3),
    ("services", "SEO", "/services/seo-services/", 4),
    ("services", "Digital Marketing", "/services/digital-marketing/", 5),
    ("services", "Google Ads", "/services/google-ads/", 6),
    ("resources", "Blog", "/blog/", 1),
    ("resources", "Case Studies", "/case-studies/", 2),
    ("resources", "FAQ", "/pages/faq/", 3),
    ("resources", "Privacy Policy", "/privacy/", 4),
    ("resources", "Terms", "/terms/", 5),
]

FAQ_CONTENT = """What does NXTWALK work on?
NXTWALK brings website development, design, SEO and digital marketing together to build useful digital systems.

How do we start a project?
Send a project enquiry with your goals, timing and service interests. The team will use that context to plan a useful first conversation.

Can we request one service on its own?
Yes. Share the specific outcome you need, and the team can discuss an individual service or a wider engagement.

What should a project enquiry include?
Tell us about your business, audience, goals, preferred timeline and any known budget range. You can leave details blank if you are still working them out.
"""


def seed_footer_links_and_faq(apps, schema_editor):
    alias = schema_editor.connection.alias
    footer_link_model = apps.get_model("website", "FooterLink")
    page_model = apps.get_model("website", "Page")

    for section, title, url, display_order in FOOTER_LINKS:
        footer_link_model.objects.using(alias).get_or_create(
            section=section,
            title=title,
            defaults={
                "url": url,
                "display_order": display_order,
                "is_active": True,
                "is_external": False,
            },
        )

    page_model.objects.using(alias).get_or_create(
        slug="faq",
        defaults={
            "title": "Frequently Asked Questions",
            "summary": "Answers to common questions about working with NXTWALK.",
            "content": FAQ_CONTENT,
            "seo_title": "Frequently Asked Questions | NXTWALK",
            "seo_description": "Learn what NXTWALK does and how to start a website or digital growth project.",
            "keywords": "NXTWALK, website development, digital marketing, SEO",
            "is_published": True,
        },
    )


class Migration(migrations.Migration):
    dependencies = [("website", "0006_footerlink")]

    operations = [migrations.RunPython(seed_footer_links_and_faq, migrations.RunPython.noop)]