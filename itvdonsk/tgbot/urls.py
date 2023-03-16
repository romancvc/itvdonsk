from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'api/v1/tgevents', ClientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]