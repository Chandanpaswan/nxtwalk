from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from .forms import ContactForm
from .models import ContactMessage, ProjectEnquiry


class ContactFormTests(SimpleTestCase):
    def test_valid_enquiry_passes_validation(self):
        form = ContactForm(data={
            "name": "Example Visitor",
            "email": "visitor@example.com",
            "company": "Example Studio",
            "budget": "not_sure",
            "message": "I would like to discuss a website.",
        })

        self.assertTrue(form.is_valid(), form.errors)

    def test_honeypot_rejects_automated_submission(self):
        form = ContactForm(data={
            "name": "Example Visitor",
            "email": "visitor@example.com",
            "message": "I would like to discuss a website.",
            "website": "https://spam.example",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("website", form.errors)

    def test_message_and_contact_details_are_required(self):
        form = ContactForm(data={})

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("message", form.errors)


class ContactModelWorkflowTests(TestCase):
    def test_project_enquiry_form_persists_timeline_and_new_status(self):
        response = self.client.post(reverse("contact:project_enquiry"), {
            "name": "Project Lead",
            "email": "project-lead@example.org",
            "company": "Example Studio",
            "timeline": "Next quarter",
            "message": "Build a product site.",
            "website": "",
        })

        enquiry = ProjectEnquiry.objects.get(email="project-lead@example.org")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(enquiry.timeline, "Next quarter")
        self.assertEqual(enquiry.status, ProjectEnquiry.NEW)

    def test_contact_form_persists_company_and_status(self):
        response = self.client.post(reverse("contact:contact"), {
            "name": "Contact Lead",
            "email": "contact-lead@example.org",
            "company": "Example Studio",
            "message": "Please contact me.",
            "website": "",
        })

        message = ContactMessage.objects.get(email="contact-lead@example.org")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(message.company, "Example Studio")
        self.assertEqual(message.status, ContactMessage.NEW)