from django.test import SimpleTestCase
from .forms import ContactForm


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