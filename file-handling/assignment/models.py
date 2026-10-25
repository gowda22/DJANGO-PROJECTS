from django.db import models


class Assignment(models.Model):
    student_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    submission = models.FileField(upload_to="assignments/")
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name
