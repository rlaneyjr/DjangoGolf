from django.shortcuts import render
from home import models as home_models


def index(request):
    return render(request, "dashboard/index.html", {})


def course_list(request):
    course_list = home_models.GolfCourse.objects.all()
    return render(request, "dashboard/courses.html", {"course_list": course_list})
