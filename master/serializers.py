from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your serializers here.
class RoleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleMaster
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        role = RoleMaster.objects.create(**validated_data)
        return role

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        instance.role_name = validated_data.get('role_name', instance.role_name)
        instance.save()
        return instance


class ModuleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleMaster
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super(ModuleMasterSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(ModuleMasterSerializer, self).update(instance=instance, validated_data=validated_data)


class UserRoleSerializer(serializers.ModelSerializer):
    module_slug_name = serializers.ReadOnlyField(source='module_id.module_slug')

    class Meta:
        model = UserRole
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super(UserRoleSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(UserRoleSerializer, self).update(instance=instance, validated_data=validated_data)


class UserAccessSerializer(serializers.ModelSerializer):
    empName = serializers.ReadOnlyField(source='emp_id.employee_name')
    userName = serializers.ReadOnlyField(source='emp_id.username')

    class Meta:
        model = UserAccess
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super(UserAccessSerializer, self).create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(UserAccessSerializer, self).update(instance=instance, validated_data=validated_data)
