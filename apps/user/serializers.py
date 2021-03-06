from rest_framework import serializers
from .models import CustomUser, Profile
from apps.core.mixins import ReadKeywordData



class UserReadKeywordData(ReadKeywordData):
    input_keyword = "user"


class UserSerializer(UserReadKeywordData, serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "first_name", "last_name",]
        read_only_fields = ["first_name", "last_name"]


class UserRegistrationSerializer(UserReadKeywordData, serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"}, write_only=True)

    class Meta:
        model = CustomUser
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
        
        #password = self.validated_data.pop("password")
        
        model = self.__class__.Meta.model
        instance = model.objects.create_user(**self.validated_data)

        Profile.objects.create(user=instance, 
                                image=self.context["request"].data["image"] )

        return instance

    def validate_password(self, password):
        if self.initial_data["password"] != self.initial_data["password2"]:
            raise serializers.ValidationError("'password' field must be equal to 'password2'.")
        
        return password


class UserLoginSerializer(UserReadKeywordData, serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["email", "username", "first_name", "last_name"]
        read_only_fields = ["first_name", "last_name"]


class ProfileSerializer(ReadKeywordData, serializers.ModelSerializer):
    input_keyword = "profile"
    class Meta:
        model = Profile
        fields = "__all__"