from django.db.models import Sum
from subordinate.serializers import *
from accounts.serializers import *
from .models import *


# Serializers define the API representation.
class DispatchInstructionSerializer(serializers.ModelSerializer):
    dil_from = serializers.PrimaryKeyRelatedField(queryset=SubDepartment.objects.all(), allow_null=True,
                                                  write_only=True)
    insurance_scope = serializers.PrimaryKeyRelatedField(queryset=InsuranceScope.objects.all(), allow_null=True,
                                                         write_only=True)
    freight_basis = serializers.PrimaryKeyRelatedField(queryset=FreightBasis.objects.all(), allow_null=True,
                                                       write_only=True)
    delivery_terms = serializers.PrimaryKeyRelatedField(queryset=DeliveryTerms.objects.all(), allow_null=True,
                                                        write_only=True)
    mode_of_shipment = serializers.PrimaryKeyRelatedField(queryset=ModeOfShipment.objects.all(), allow_null=True,
                                                          write_only=True)
    payment_status = serializers.PrimaryKeyRelatedField(queryset=PaymentStatus.objects.all(), allow_null=True,
                                                        write_only=True)
    special_packing = serializers.PrimaryKeyRelatedField(queryset=SpecialPacking.objects.all(), allow_null=True,
                                                         write_only=True)
    export_packing_req = serializers.PrimaryKeyRelatedField(queryset=ExportPackingRequirement.objects.all(),
                                                            allow_null=True, write_only=True)
    special_gst_rate = serializers.PrimaryKeyRelatedField(queryset=SpecialGSTRate.objects.all(), allow_null=True,
                                                          write_only=True)

    dil_from_details = SubDepartmentSerializer(source='dil_from', read_only=True)
    insurance_scope_details = InsuranceScopeSerializer(source='insurance_scope', read_only=True)
    freight_basis_details = FreightBasisSerializer(source='freight_basis', read_only=True)
    delivery_terms_details = DeliveryTermsSerializer(source='delivery_terms', read_only=True)
    mode_of_shipment_details = ModeOfShipmentSerializer(source='mode_of_shipment', read_only=True)
    payment_status_details = PaymentStatusSerializer(source='payment_status', read_only=True)
    special_packing_details = SpecialPackingSerializer(source='special_packing', read_only=True)
    export_packing_req_details = ExportPackingRequirementSerializer(source='export_packing_req', read_only=True)
    special_gst_rate_details = SpecialGSTRateSerializer(source='special_gst_rate', read_only=True)

    class Meta:
        model = DispatchInstruction
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at', 'is_active', 'dil_from_details',
                            'insurance_scope_details', 'freight_basis_details', 'delivery_terms_details',
                            'mode_of_shipment_details', 'payment_status_details', 'special_packing_details',
                            'export_packing_req_details', 'special_gst_rate_details']
        depth = 1

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user
        validated_data['is_active'] = True
        validated_data['dil_stage'] = 1
        validated_data['current_level'] = 1
        return DispatchInstruction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(DispatchInstructionSerializer, self).update(instance, validated_data)


class DispatchUnRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchInstruction
        fields = '__all__'


class SAPDispatchInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SAPDispatchInstruction
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at', 'is_active']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user
        validated_data['is_active'] = True
        return DispatchInstruction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(SAPDispatchInstructionSerializer, self).update(instance, validated_data)


class DispatchBillDetailsSerializer(serializers.ModelSerializer):
    dil_id = serializers.PrimaryKeyRelatedField(queryset=DispatchInstruction.objects.all(), required=True)

    class Meta:
        model = DispatchBillDetails
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at', 'is_active']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user
        validated_data['is_active'] = True
        return DispatchBillDetails.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(DispatchBillDetailsSerializer, self).update(instance, validated_data)


class DispatchPODetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchPODetails
        fields = '__all__'


class MasterItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterItemList
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at', 'is_active']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user
        validated_data['is_active'] = True
        return MasterItemList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(MasterItemListSerializer, self).update(instance, validated_data)


class InlineItemListSerializer(serializers.ModelSerializer):
    serial_no = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = InlineItemList
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at', 'is_active']


# for new
class TestInlineItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InlineItemList
        fields = '__all__'


class TestMasterItemListSerializer(serializers.ModelSerializer):
    inline_items = TestInlineItemListSerializer(many=True, read_only=True)
    sum_quantity = serializers.SerializerMethodField()

    class Meta:
        model = MasterItemList
        fields = ['item_id', 'dil_id', 'material_description', 'material_no', 'ms_code', 'item_no', 'so_no',
                  's_loc', 'bin', 'plant', 'linkage_no', 'group', 'quantity', 'country_of_origin', 'serial_no',
                  'match_no', 'tag_no', 'range', 'customer_po_sl_no', 'customer_po_item_code',
                  'item_status', 'item_status_no', 'packed_quantity', 'revision_flag', 'revision_count', 'verified_by',
                  'verified_at', 'verified_flag', 'packed_by', 'packed_at', 'packing_flag', 'custom_po_flag',
                  'serial_no_qty', 'serial_flag', 'warranty_flag', 'warranty_date', 'status', 'status_no',
                  'inline_items', 'sum_quantity']

    def get_sum_quantity(self, obj):
        sum_quantity = MasterItemList.objects.filter(
            ms_code=obj.ms_code,
            material_no=obj.material_no,
            dil_id=obj.dil_id
        ).aggregate(total_quantity=Sum('quantity'))['total_quantity']

        return sum_quantity


class MasterItemBatchSerializer(serializers.ModelSerializer):
    inline_items = InlineItemListSerializer(many=True)

    class Meta:
        model = MasterItemList
        fields = (
            'item_id', 'dil_id', 'item_no', 'so_no', 'material_description', 'material_no',
            'ms_code', 's_loc', 'bin', 'plant', 'linkage_no', 'group', 'quantity',
            'country_of_origin', 'serial_no', 'match_no', 'tag_no', 'range',
            'customer_po_sl_no', 'customer_po_item_code', 'packed_quantity',
            'revision_flag', 'revision_count', 'verified_by', 'verified_at',
            'verified_flag', 'packed_by', 'packed_at', 'packing_flag', 'custom_po_flag',
            'serial_no_qty', 'serial_flag', 'warranty_flag', 'warranty_date', 'status',
            'status_no', 'inline_items'
        )


class DAUserRequestAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DAUserRequestAllocation
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return DAUserRequestAllocation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(DAUserRequestAllocationSerializer, self).update(instance=instance, validated_data=validated_data)


class DAAuthThreadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DAAuthThreads
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        # take user id as integer and assign to emp_id
        validated_data['emp_id'] = self.context['request'].user.id
        return DAAuthThreads.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.da_id = validated_data.get('da_id', instance.da_id)
        instance.wf_id = validated_data.get('wf_id', instance.wf_id)
        return super(DAAuthThreadsSerializer, self).update(instance=instance, validated_data=validated_data)


class FileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileType
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return FileType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.file_type = validated_data.get('file_type', instance.file_type)
        instance.updated_by = self.context['request'].user
        return super(FileTypeSerializer, self).update(instance=instance, validated_data=validated_data)


class MultiFileAttachmentSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MultiFileAttachment
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['is_active'] = True
        return MultiFileAttachment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.file_name = validated_data.get('file_name', instance.file_name)
        instance.file_type = validated_data.get('file_type', instance.file_type)
        instance.updated_by = self.context['request'].user
        return super(MultiFileAttachmentSerializer, self).update(instance=instance, validated_data=validated_data)
