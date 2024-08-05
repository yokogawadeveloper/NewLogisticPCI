from rest_framework import serializers
from .models import Department, SubDepartment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

User = get_user_model()


# Create your serializers here.
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class SubDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubDepartment
        fields = '__all__'
        depth = 1


class RegisterSerializer(serializers.ModelSerializer):
    default_password = "Yokogawa@12345"
    default_error_messages = {"username": "The username should only contain alphanumeric characters"}
    mail_error_messages = {"email": "Enter a valid email address."}

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "department", "sub_department"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            raise serializers.ValidationError(self.mail_error_messages)
        return attrs

    def create(self, validated_data):
        validated_data['password'] = self.default_password
        validated_data['name'] = validated_data['first_name'] + " " + validated_data['last_name']
        return User.objects.create_user(**validated_data)


class EmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
        depth = 1

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class EmployeeTokenObtainPairSerializer(TokenObtainPairSerializer):
    role = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    subDepartment = serializers.SerializerMethodField()

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
