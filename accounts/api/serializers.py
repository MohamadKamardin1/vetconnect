from django.contrib.auth import authenticate
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from accounts.models import Role, User, UserRole


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["code", "name", "description"]


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(read_only=True)
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "phone_number", "first_name", "last_name", "display_name", "roles", "email_verified_at", "phone_verified_at", "created_at"]
        read_only_fields = ["id", "display_name", "roles", "email_verified_at", "phone_verified_at", "created_at"]

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_roles(self, obj) -> list[str]:
        return list(obj.user_roles.filter(is_active=True).values_list("role__code", flat=True))


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=12)
    role = serializers.ChoiceField(choices=[(value, value) for value, _ in UserRole._meta.get_field("role").remote_field.model._meta.get_field("code").choices], write_only=True, required=False)

    class Meta:
        model = User
        fields = ["email", "phone_number", "first_name", "last_name", "password", "role"]

    def create(self, validated_data):
        role = validated_data.pop("role", "OWNER")
        user = User.objects.create_user(is_active=False, **validated_data)
        user.assign_role(role)
        return user


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.RegexField(r"^\d{6}$", max_length=6, min_length=6, error_messages={"invalid": "Enter the six-digit code from your email."})


class EmailVerificationResendSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials.")
        attrs["user"] = user
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=12)
