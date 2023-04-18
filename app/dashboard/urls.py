from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("courses/", views.course_list, name="courses"),
    path("courses/add/", views.add_course, name="add_course"),
    path("courses/<int:pk>/", views.course_detail, name="course_detail"),
    path("holes/<int:pk>/", views.hole_detail, name="hole_detail"),
    path("tees/<int:hole_pk>/", views.create_tee, name="create_tee"),
]
