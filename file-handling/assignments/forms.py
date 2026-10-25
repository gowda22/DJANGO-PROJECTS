from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError

from .models import Assignment


ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".doc", ".docx", ".txt", ".zip"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["student_name", "course", "assignment_file"]
        labels = {
            "student_name": "Student name",
            "course": "Course / subject",
            "assignment_file": "Choose a file",
        }
        widgets = {
            "student_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your full name", "autocomplete": "name"}
            ),
            "course": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g. Python, Django, Web Development"}
            ),
            "assignment_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control file-control",
                    "accept": ".pdf,.png,.jpg,.jpeg,.doc,.docx,.txt,.zip",
                }
            ),
        }

    def clean_student_name(self):
        """Field-level validation: trim whitespace and require a useful name."""
        name = self.cleaned_data["student_name"].strip()
        if len(name) < 2:
            raise ValidationError("Enter a name with at least 2 characters.")
        if not any(character.isalpha() for character in name):
            raise ValidationError("The student name must contain letters.")
        return name

    def clean_course(self):
        """Field-level validation for the course name."""
        course = self.cleaned_data["course"].strip()
        if len(course) < 2:
            raise ValidationError("Enter a course or subject name with at least 2 characters.")
        return course

    def clean_assignment_file(self):
        """Validate extension and size. This is a learning-project safeguard, not malware scanning."""
        uploaded_file = self.cleaned_data.get("assignment_file")
        if not uploaded_file:
            raise ValidationError("Choose a file to upload.")

        extension = Path(uploaded_file.name).suffix.lower()
        if extension not in ALLOWED_EXTENSIONS:
            allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
            raise ValidationError(f"Unsupported file type. Allowed types: {allowed}.")

        if uploaded_file.size > MAX_FILE_SIZE:
            raise ValidationError("The file must be 10 MB or smaller.")

        return uploaded_file
