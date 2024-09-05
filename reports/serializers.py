from packing.serializers import *
from dispatch.serializers import *


# Create your serializers here.
class PackingListPDFBoxDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxDetails
        fields = '__all__'


# Serializers for reports
class BoxDetailsReportSerializer(serializers.ModelSerializer):
    # dispatch_instruction = DispatchInstructionSerializer(source='dil_id', read_only=True)

    class Meta:
        model = BoxDetails
        fields = '__all__'


class ItemPackingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPacking
        fields = '__all__'
        depth = 1


class ItemPackingInlineReportSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    updated_by = serializers.ReadOnlyField(source='updated_by.username')
    box_details = serializers.SerializerMethodField()

    class Meta:
        model = ItemPackingInline
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')
        depth = 1

    def get_box_details(self, obj):
        if obj.item_pack_id:
            box_details = BoxDetails.objects.filter(box_code=obj.item_pack_id.box_code)
            return BoxDetailsReportSerializer(box_details, many=True).data
        return []


class InlineItemListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InlineItemList
        fields = '__all__'


class MasterItemListReportSerializer(serializers.ModelSerializer):
    inline_items = InlineItemListReportSerializer(many=True)

    class Meta:
        model = MasterItemList
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')
