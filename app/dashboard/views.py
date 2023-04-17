from django.shortcuts import render


def index(request):
    return render(request, "dashboard/index.html", {})


def course_list(request):
    return render(request, "dashboard/courses.html", {})
