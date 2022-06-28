from rest_framework import serializers
from .models import User, Profile



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name",]
        read_only_fields = ["first_name", "last_name"]

    def validate(self, *args, **kwargs):
        return super().validate(*args, **kwargs)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "password2"]
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def save(self, *args, **kwargs):
        del self.validated_data["password2"]
        
        return super().save(*args, **kwargs)

    def create(self, validated_data):
        if ("password" not in self.validated_data)\
                and ("password2" not in self.validated_data):
            raise serializers.ValidationError("You should provide 'password' alongside with 'password2'")
        
        return super().create(validated_data)

    def validate_password(self, password):
        if self.initial_data["password"] != self.initial_data["password2"]:
            raise serializers.ValidationError("'password' field must be equal to 'password2'.")
        
        return password


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name"]
        read_only_fields = ["first_name", "last_name"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"