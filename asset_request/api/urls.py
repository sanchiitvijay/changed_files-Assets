# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from asset_request.views import AssetRequestViewSet

router = DefaultRouter()
router.register(r"asset-request", AssetRequestViewSet)

urlpatterns = [
    path('', include(router.urls))
]