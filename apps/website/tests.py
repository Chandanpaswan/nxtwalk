from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from apps.contact.models import ContactMessage, ProjectEnquiry
from apps.portfolio.models import Project
from apps.services.models import Service
from .models import FooterLink, FooterSettings, NavigationItem, NewsletterSubscriber, Page, SiteSettings, SocialLink


class PublicRouteTests(SimpleTestCase):
    def test_primary_pages_have_named_routes(self):
        route_names = [
            "website:home",
            "website:about",
            "services:list",
            "blog:list",
            "portfolio:list",
            "case_studies:list",
            "contact:contact",
            "website:privacy",
            "website:terms",
            "website:html_sitemap",
            "sitemap",
        ]

        for route_name in route_names:
            with self.subTest(route_name=route_name):
                self.assertTrue(reverse(route_name).startswith("/"))

    def test_content_detail_routes_use_slugs(self):
        routes = {
            "services:detail": "services/web-development/",
            "blog:detail": "blog/digital-growth/",
            "portfolio:detail": "portfolio/project-name/",
            "case_studies:detail": "case-studies/project-name/",
        }

        for route_name, expected in routes.items():
            with self.subTest(route_name=route_name):
                self.assertEqual(reverse(route_name, kwargs={"slug": expected.split("/")[-2]}), f"/{expected}")


class SiteManagementWorkflowTests(TestCase):
    def test_seeded_site_settings_have_official_links_and_no_invented_email(self):
        settings = SiteSettings.objects.get(pk=1)
        self.assertEqual(settings.whatsapp_number, "+917015907650")
        self.assertEqual(settings.whatsapp_link, "https://wa.me/917015907650")
        self.assertEqual(settings.contact_email, "")
        self.assertEqual(FooterSettings.objects.count(), 1)
        self.assertEqual(Page.objects.get(slug="faq").is_published, True)

        links = {link.platform: link.url for link in SocialLink.objects.filter(is_active=True)}
        self.assertEqual(links, {
            "instagram": "https://www.instagram.com/nxtwalk/",
            "facebook": "https://www.facebook.com/nxtwalk",
            "x": "https://x.com/nxtwalk",
            "linkedin": "https://www.linkedin.com/company/nxtwalk/",
            "youtube": "https://www.youtube.com/@nxtwalk",
        })
        self.assertTrue(FooterLink.objects.filter(section=FooterLink.RESOURCES, title="FAQ", url="/pages/faq/").exists())
        self.assertEqual(NavigationItem.objects.filter(is_cta=True).count(), 1)

    def test_newsletter_signup_is_idempotent_and_honeypot_blocks_bots(self):
        response = self.client.post(reverse("website:newsletter_subscribe"), {"email": "person@example.org", "name": "NXT Visitor"})
        self.assertEqual(response.status_code, 302)
        self.client.post(reverse("website:newsletter_subscribe"), {"email": "PERSON@example.org"})
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)

        self.client.post(reverse("website:newsletter_subscribe"), {"email": "bot@example.org", "website": "https://spam.example"})
        self.assertFalse(NewsletterSubscriber.objects.filter(email="bot@example.org").exists())

    def test_contact_and_project_leads_are_saved_with_new_status(self):
        contact_response = self.client.post(reverse("contact:contact"), {
            "name": "Contact Visitor",
            "email": "contact@example.org",
            "message": "Please get in touch about digital services.",
            "website": "",
        })
        project_response = self.client.post(reverse("contact:project_enquiry"), {
            "name": "Project Visitor",
            "email": "project@example.org",
            "timeline": "This quarter",
            "message": "We need a new website.",
            "website": "",
        })
        self.assertEqual(contact_response.status_code, 302)
        self.assertEqual(project_response.status_code, 302)
        self.assertEqual(ContactMessage.objects.get(email="contact@example.org").status, ContactMessage.NEW)
        self.assertEqual(ProjectEnquiry.objects.get(email="project@example.org").status, ProjectEnquiry.NEW)

    def test_admin_dashboard_counts_database_records(self):
        existing_service_count = Service.objects.filter(is_active=True).count()
        ContactMessage.objects.create(name="Lead", email="lead@example.org", message="A real test lead")
        ProjectEnquiry.objects.create(name="Project", email="project@example.org", message="A real test project enquiry")
        Service.objects.create(title="Test service", slug="test-service", short_description="Short", description="Full", is_active=True)
        Project.objects.create(title="Test work", slug="test-work", client_name="Test client", category="Website", description="A database test project", is_published=True)
        NewsletterSubscriber.objects.create(email="subscriber@example.org")
        get_user_model().objects.create_user(username="staff", password="StrongPassword123!", is_staff=True)
        self.client.login(username="staff", password="StrongPassword123!")

        response = self.client.get(reverse("website:admin_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_leads"], 2)
        self.assertEqual(response.context["new_leads"], 2)
        self.assertEqual(response.context["service_count"], existing_service_count + 1)
        self.assertEqual(response.context["project_count"], 1)
        self.assertEqual(response.context["subscriber_count"], 1)

    def test_admin_content_and_contact_sections_are_registered(self):
        administrator = get_user_model().objects.create_superuser(
            username="site-admin",
            email="admin@example.org",
            password="StrongPassword123!",
        )
        self.client.force_login(administrator)
        route_names = [
            "admin:website_sitesettings_changelist",
            "admin:website_footersettings_changelist",
            "admin:website_footerlink_changelist",
            "admin:website_sociallink_changelist",
            "admin:website_navigationitem_changelist",
            "admin:website_page_changelist",
            "admin:website_newslettersubscriber_changelist",
            "admin:contact_contactmessage_changelist",
            "admin:contact_projectenquiry_changelist",
            "admin:services_service_changelist",
            "admin:blog_post_changelist",
            "admin:portfolio_project_changelist",
            "admin:case_studies_casestudy_changelist",
            "admin:testimonials_testimonial_changelist",
        ]

        for route_name in route_names:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)