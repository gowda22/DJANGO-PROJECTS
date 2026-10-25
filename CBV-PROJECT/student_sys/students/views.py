from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .models import Student
from django.views.generic import(
    ListView,
    DetailView,CreateView,UpdateView,DeleteView
)

# Create your views here.
class StudentListView(ListView):
    model=Student
    template_name="student_list.html"
    context_object_name="students"
class StudentDetailsView(DetailView):
    model=Student
    template_name="student_detail.html"
class StudentCreateView(CreateView):
    model=Student
    fields=["name","age","course"]
    template_name="student_form.html"
    success_url=reverse_lazy("student-list")
class StudentUpdateView(UpdateView):
    model=Student
    fields=["name","age","course"]
    template_name="student_form.html"
    success_url=reverse_lazy("student-list")
class StudentDeleteView(DeleteView):
    model=Student
    template_name="student_confirm_delete.html"
    success_url=reverse_lazy("student-list")


    



