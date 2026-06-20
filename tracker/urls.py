from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tracker.views import HabitViewSet, PublicHabitListView

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('habits/public/', PublicHabitListView.as_view(), name='public-habits'),
    path('', include(router.urls)),
]