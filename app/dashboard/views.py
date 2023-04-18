from django.shortcuts import render, redirect
from home import models as home_models
from . import forms
from . import utils


def index(request):
    return render(request, "dashboard/index.html", {})


def course_list(request):
    course_list = home_models.GolfCourse.objects.all()
    return render(request, "dashboard/courses.html", {"course_list": course_list})


def add_course(request):
    if request.method == "POST":
        form = forms.GolfCourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            utils.create_holes_for_course(course)
            return redirect("dashboard:courses")
    else:
        form = forms.GolfCourseForm()
    return render(request, "dashboard/add_course.html", {"form": form})
