from rest_framework.routers import DefaultRouter
from .views import ComplaintViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'complaints', ComplaintViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
