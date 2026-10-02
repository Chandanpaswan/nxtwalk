from django.test import SimpleTestCase
from django.urls import reverse


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