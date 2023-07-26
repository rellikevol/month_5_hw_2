from rest_framework import serializers
from users.models import User, Transaction
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'wallet_address')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=30, write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=30, write_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'email', 'age', 'phone_number')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Пароли отличаются'})
        password_validation.validate_password(attrs['password'], self.instance)
        if len(attrs['phone_number']) < 13:
            raise serializers.ValidationError({'phone_number': 'В телефонном номере на достаточно цифр'})
        if attrs['phone_number'][:4] != '+996':
            raise serializers.ValidationError({'phone_number': 'Введите верный код региона (+996)'})
        return attrs

    def create(self, validated_data: dict):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            age=validated_data['age'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])

        user.save()
        return user

class UserTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'from_user', 'to_user', 'is_completed', 'created_at', 'amount')


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'age', 'phone_number',
                  'date_joined', 'wallet_address', 'wallet_amount')
