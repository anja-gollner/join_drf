from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']


class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self, **kwargs):
        full_name = self.validated_data['full_name']
        pw = self.validated_data['password']
        repeated_password = self.validated_data['repeated_password']
        if pw != repeated_password:
            raise serializers.ValidationError(
                {'error': 'passwords dont match'})
        username = full_name.replace(" ", "")
        account = User(
            email=self.validated_data['email'], username=username)
        account.set_password(pw)
        account.first_name = full_name
        account.is_staff = True
        account.save()
        return account


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        data["user"] = user
        return data


class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
