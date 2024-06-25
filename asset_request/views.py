# views.py
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from asset_request.api.serializers import AssetRequestSerializer
from asset_request.models import AssetRequest

# Asset Request ViewSets
class AssetRequestViewSet(viewsets.ModelViewSet):
    queryset = AssetRequest.objects.all()
    serializer_class = AssetRequestSerializer
    search_fields = []
    filterset_fields = {
        'w_id': ['exact'],
        's_id': ['exact']
    }
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
