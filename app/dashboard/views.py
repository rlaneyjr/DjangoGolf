from django.shortcuts import render, redirect, get_object_or_404
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


def course_detail(request, pk):
    course_data = get_object_or_404(home_models.GolfCourse, pk=pk)
    course_location = None
    hole_list = home_models.Hole.objects.filter(course=course_data).order_by("name")
    if all([course_data.city, course_data.state, course_data.zip_code]):
        course_location = (
            f"{course_data.city}, {course_data.state}, {course_data.zip_code}"
        )
    return render(
        request,
        "dashboard/course_detail.html",
        {
            "course_data": course_data,
            "course_location": course_location,
            "hole_list": hole_list,
        },
    )
