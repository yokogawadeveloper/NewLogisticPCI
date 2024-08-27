from rest_framework import serializers
from dispatch.serializers import DispatchInstructionSerializer
from .models import *


# Create your serializers here.
class BoxTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxType
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        box_type = BoxType.objects.create(**validated_data)
        return box_type

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        instance.box_type = validated_data.get('box_type', instance.box_type)
        instance.save()
        return instance


class BoxSizeSerializer(serializers.ModelSerializer):
    box_type = BoxTypeSerializer(read_only=True)

    class Meta:
        model = BoxSize
        fields = ('box_size_id', 'box_type', 'box_size', 'box_description', 'created_by', 'created_at', 'updated_by',)
        read_only_fields = ('created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super(BoxSizeSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(BoxSizeSerializer, self).update(instance=instance, validated_data=validated_data)


class BoxDetailSerializer(serializers.ModelSerializer):
    box_size = BoxSizeSerializer(read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BoxDetails
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')
        depth = 1

    #
    # def __init__(self, *args, **kwargs):
    #     depth = kwargs.get('context', {}).get('depth', 0)
    #     super().__init__(*args, **kwargs)
    #     if depth <= 1:
    #         self.fields.pop('dil_id')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super(BoxDetailSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(BoxDetailSerializer, self).update(instance=instance, validated_data=validated_data)


class UnRelatedBoxDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxDetails
        fields = '__all__'


class BoxDetailsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxDetailsFile
        fields = '__all__'


class ItemPackingInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPackingInline
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('tag_no') is None:
            representation['tag_no'] = ''
        return representation

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super(ItemPackingInlineSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(ItemPackingInlineSerializer, self).update(instance=instance, validated_data=validated_data)


class ItemPackingSerializer(serializers.ModelSerializer):
    item_packing_inline = ItemPackingInlineSerializer(many=True)
    created_by = serializers.StringRelatedField()
    updated_by = serializers.StringRelatedField()

    class Meta:
        model = ItemPacking
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')
        depth = 1

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super(ItemPackingSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(ItemPackingSerializer, self).update(instance=instance, validated_data=validated_data)


class DispatchInstructionDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchInstruction
        fields = '__all__'
