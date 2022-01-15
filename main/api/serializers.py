from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User
    """
    email = serializers.EmailField(
        write_only=True,
        required=True,
        validators=[UniqueValidator(User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'photo',
            'gender',
            'password',
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
