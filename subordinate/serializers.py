from rest_framework import serializers
from .models import *


# Create your serializers here.

class InsuranceScopeSerializer(serializers.ModelSerializer):
    insurance_scope_name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = InsuranceScope
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['is_active'] = True
        return super(InsuranceScopeSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(InsuranceScopeSerializer, self).update(instance=instance, validated_data=validated_data)


class FreightBasisSerializer(serializers.ModelSerializer):
    freight_basis_name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = FreightBasis
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['is_active'] = True
        return super(FreightBasisSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(FreightBasisSerializer, self).update(instance=instance, validated_data=validated_data)


class DeliveryTermsSerializer(serializers.ModelSerializer):
    delivery_terms_name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = DeliveryTerms
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['is_active'] = True
        return super(DeliveryTermsSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(DeliveryTermsSerializer, self).update(instance=instance, validated_data=validated_data)


class ModeOfShipmentSerializer(serializers.ModelSerializer):
    mode_of_shipment_name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = ModeOfShipment
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['is_active'] = True
        return super(ModeOfShipmentSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(ModeOfShipmentSerializer, self).update(instance=instance, validated_data=validated_data)


class PaymentStatusSerializer(serializers.ModelSerializer):
    payment_status_name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = PaymentStatus
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['is_active'] = True
        return super(PaymentStatusSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(PaymentStatusSerializer, self).update(instance=instance, validated_data=validated_data)


class SpecialPackingSerializer(serializers.ModelSerializer):
    special_packing_name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = SpecialPacking
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['is_active'] = True
        return super(SpecialPackingSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(SpecialPackingSerializer, self).update(instance=instance, validated_data=validated_data)


class ExportPackingRequirementSerializer(serializers.ModelSerializer):
    export_packing_requirement_name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = ExportPackingRequirement
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['is_active'] = True
        return super(ExportPackingRequirementSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(ExportPackingRequirementSerializer, self).update(instance=instance, validated_data=validated_data)


class SpecialGSTRateSerializer(serializers.ModelSerializer):
    special_gst_rate_name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = SpecialGSTRate
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['is_active'] = True
        return super(SpecialGSTRateSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(SpecialGSTRateSerializer, self).update(instance=instance, validated_data=validated_data)


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class TalukSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taluk
        fields = '__all__'


class PincodeSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    taluk = TalukSerializer(read_only=True)

    class Meta:
        model = Pincode
        fields = '__all__'


class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = '__all__'
