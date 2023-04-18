from django.urls import path, include

app_name = "core"

urlpatterns = [
    path("api/", include("core.api.urls")),
]
