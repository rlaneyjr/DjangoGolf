from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("golf-courses", views.GolfCourseViewSet, basename="golf-course")
router.register("games", views.GameViewSet, basename="game")
router.register("players", views.PlayerViewSet, basename="player")

urlpatterns = router.urls
