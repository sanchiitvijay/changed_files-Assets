from django.db import models

# Create your models here.
from django.db import models
from master.models import Department
from audit_fields.models import AuditUuidModelMixin


class AssetRequest(AuditUuidModelMixin):
    # Required Fields
    ar_no = models.CharField(max_length=1000, unique=True)
    created_by = models.CharField(max_length=255, null=True)
    request_date = models.DateTimeField(null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Asset Request {self.ar_no}"


class AssetRequestItem(AuditUuidModelMixin):
    # asset request order details
    asset_request = models.ForeignKey(AssetRequest, on_delete=models.CASCADE, related_name='asset_request_items',
                                       null=True, blank=True)
    asset_code = models.CharField(max_length=50, default=None, null=True)
    asset_name = models.CharField(max_length=255, default=None, null=True)
    required_date = models.DateField(null=True)
    asset_description = models.CharField(max_length=50, default=None, null=True)
    unit = models.CharField(max_length=50, default=None, null=True)
    qty = models.PositiveBigIntegerField(default=0, null=True)
    
    def __str__(self):
        return f"{self.part_no} - {self.part_name} ({self.asset_request})"
