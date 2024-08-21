from rest_framework import serializers
from dispatch.models import *
from .models import *


# Create your serializers here.
class SAPInvoiceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SAPInvoiceDetails
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user
        return SAPInvoiceDetails.objects.create(**validated_data)


class TruckTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckType
        fields = '__all__'


class TrackingTransportationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingTransportation
        fields = '__all__'


class TruckRequestSerializer(serializers.ModelSerializer):
    transporter = TrackingTransportationSerializer()

    class Meta:
        model = TruckRequest
        fields = '__all__'


class TruckRequestTypesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckRequestTypesList
        fields = '__all__'


class TruckListSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TruckList
        fields = '__all__'
        depth = 1

    def __init__(self, *args, **kwargs):
        depth = kwargs.get('context', {}).get('depth', 0)
        super().__init__(*args, **kwargs)
        if depth <= 1:
            self.fields.pop('check_out_by')


class TruckTransportationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckList
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.transportation = validated_data.get('transportation', instance.transportation)
        instance.save()
        return instance


class TruckDIlMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckDilMappingDetails
        fields = '__all__'


class TruckLoadingDetailsSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TruckLoadingDetails
        fields = '__all__'
        depth = 1


class TruckDeliveryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckDeliveryDetails
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super(TruckDeliveryDetailsSerializer, self).create(validated_data=validated_data)


class DCInvoiceDetailsSerializer(serializers.ModelSerializer):
    lrn_no = serializers.ReadOnlyField(source='delivery_challan.lrn_no')
    lrn_date = serializers.ReadOnlyField(source='delivery_challan.lrn_date')
    e_way_bill_no = serializers.ReadOnlyField(source='delivery_challan.e_way_bill_no')
    truck_no = serializers.ReadOnlyField(source='truck_list.vehicle_no')
    no_of_packages = serializers.SerializerMethodField()

    class Meta:
        model = DCInvoiceDetails
        fields = '__all__'
        depth = 1

    def get_no_of_packages(self, obj):
        count = TruckLoadingDetails.objects.filter(dil_id=obj.dil_id, truck_list_id=obj.truck_list).count()
        return count if count else 0


class DeliveryChallanSerializer(serializers.ModelSerializer):
    dc_invoice_details = DCInvoiceDetailsSerializer(many=True)

    class Meta:
        model = DeliveryChallan
        fields = ('id', 'truck_list', 'e_way_bill_no', 'lrn_no', 'lrn_date', 'no_of_boxes',
                  'description_of_goods', 'mode_of_delivery', 'freight_mode', 'destination',
                  'kind_attended', 'consignee_remakes', 'remarks', 'created_by', 'created_at',
                  'updated_by', 'updated_at', 'is_active', 'dc_invoice_details'
                  )


# unrelated serializer
class UnRelatedDCInvoiceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DCInvoiceDetails
        fields = '__all__'


class UnRelatedDeliveryChallanSerializer(serializers.ModelSerializer):
    dc_invoice_details = UnRelatedDCInvoiceDetailsSerializer(many=True)

    class Meta:
        model = DeliveryChallan
        fields = (
            'id', 'truck_list', 'e_way_bill_no', 'e_way_bills_date', 'delivers_dates', 'lrn_no', 'lrn_date',
            'no_of_boxes',
            'description_of_goods', 'mode_of_delivery', 'freight_mode', 'destination', 'kind_attended',
            'consignee_remakes',
            'remarks', 'created_by', 'created_at', 'updated_by', 'updated_at', 'is_active', 'dc_invoice_details'
        )


class InvoiceChequeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceChequeDetails
        fields = '__all__'


class EWBDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EWBDetails
        fields = '__all__'


class GatePassInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatePassInfo
        fields = '__all__'
        depth = 1


class GatePassTruckDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatePassTruckDetails
        fields = '__all__'
    #     depth = 1
    #
    # def __init__(self, *args, **kwargs):
    #     depth = kwargs.get('context', {}).get('depth', 0)
    #     super().__init__(*args, **kwargs)
    #     if depth <= 1:
    #         self.fields.pop('create_by')
    #         self.fields.pop('updated_by')


class GatePassApproverDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatePassApproverDetails
        fields = '__all__'
