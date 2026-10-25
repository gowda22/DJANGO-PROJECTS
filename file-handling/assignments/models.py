from django.db import models


class Assignment(models.Model):
    """One uploaded assignment and the student/course details attached to it."""

    student_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    assignment_file = models.FileField(upload_to="assignments/")
    submitted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_on"]
        verbose_name = "assignment submission"
        verbose_name_plural = "assignment submissions"

    def __str__(self):
        return f"{self.student_name} - {self.course}"
