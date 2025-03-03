from django.urls import path, include
from .views import ContactViewSet, TaskViewSet, SubtaskViewSet, SummaryView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'subtasks', SubtaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', SummaryView.as_view(), name="summary"),
]
