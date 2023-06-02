from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("golf-courses", views.GolfCourseViewSet, basename="golf-course")
router.register("games", views.GameViewSet, basename="game")

urlpatterns = router.urls
