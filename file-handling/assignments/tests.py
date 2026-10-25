from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .forms import AssignmentForm


class AssignmentFormTests(TestCase):
    def test_valid_pdf_form(self):
        uploaded = SimpleUploadedFile("notes.pdf", b"small test file", content_type="application/pdf")
        form = AssignmentForm(
            data={"student_name": "Asha Rao", "course": "Django"},
            files={"assignment_file": uploaded},
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_rejects_unsupported_extension(self):
        uploaded = SimpleUploadedFile("script.exe", b"not really an exe", content_type="application/octet-stream")
        form = AssignmentForm(
            data={"student_name": "Asha Rao", "course": "Django"},
            files={"assignment_file": uploaded},
        )
        self.assertFalse(form.is_valid())
        self.assertIn("assignment_file", form.errors)


class AssignmentPageTests(TestCase):
    def test_home_redirects_to_assignment_list(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/assignments/")

    def test_list_page_loads(self):
        response = self.client.get(reverse("assignments:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assignment submissions")
