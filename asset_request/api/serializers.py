from audit_fields.serializers import AuditModelMixinSerializer
from asset_request.models import AssetRequest, AssetRequestItem
from utils.constants import NumberConstructorConstants
from utils.number_constuctor import NumberConstructor


class AssetRequestItemsSerializer(AuditModelMixinSerializer):
    class Meta:
        model = AssetRequestItem
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print("data: ",data)
        if instance.asset is not None:
            data['asset_request_id'] = instance.asset.asset_code
            data['asset_name'] = instance.asset.asset_name
            data['asset_description'] = instance.asset.asset_description
        return data
    
class AssetRequestSerializer(AuditModelMixinSerializer):
    asset_request_items = AssetRequestItemsSerializer(many=True)

    class Meta:
        model = AssetRequest
        fields = '__all__'

    def create(self, validated_data):
        # Extract nested data from validated_data
        asset_request_item_details = validated_data.pop('asset_request_items', [])
        # generate the code.
        
        validated_data['ar_no'] = NumberConstructor().generate_next_sequence(
            NumberConstructorConstants.ASSET_REQUEST_NUMBERING, False)

        # print(validated_data)
        # Create Asset Request  instance
        instance = super().create(validated_data)

        print(validated_data)
        
        # Create AssetRequest Item instances related to the VendorMaster using bulk_create
        asset_request_item_instances = [AssetRequestItem(asset_request=instance, **data) for data in asset_request_item_details]
        AssetRequestItem.objects.bulk_create(asset_request_item_instances)
    

        print(12344)
        return instance;

    def update(self, instance, validated_data):
        # Update or create AssetRequest  items instances related to the AssetRequest 
        asset_request_item_data = self.initial_data.pop('asset_request_items', [])
        validated_data.pop('asset_request_items', [])
        existing_asset_request_items_ids = []
        for asset_request_item in asset_request_item_data:
            asset_request_item_instance = AssetRequestItem.objects.filter(id=asset_request_item.get('id')).first()
            if asset_request_item_instance:
                existing_asset_request_items_ids.append(asset_request_item_instance.id)
                # Update existing instance
                AssetRequestItem.objects.filter(id=asset_request_item_instance.id).update(**asset_request_item)
            else:
                # Create new instance
                new_po_item_instance = AssetRequestItem.objects.create(asset_request=instance,asset_id=asset_request_item.pop('asset', None),**asset_request_item)
                existing_asset_request_items_ids.append(new_po_item_instance.id)

        # Delete Asset Request  Items instances that were not provided in the update data
        instance.asset_request_items.exclude(id_in=[_id for _id in existing_asset_request_items_ids]).delete()

        return super().update(instance, validated_data)
