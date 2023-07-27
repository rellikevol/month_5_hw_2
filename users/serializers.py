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
        fields = ('id', 'from_user', 'to_user', 'created_at', 'amount')


class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount', 'to_address')

    def validate(self, attrs):
        if User.objects.get(pk=self.context['request'].user.id).wallet_address == attrs['to_address']:
            raise serializers.ValidationError({'to_adress': 'Нельзя перевести самому себе'})
        if attrs['amount'] > User.objects.get(pk=self.context['request'].user.id).wallet_amount:
            raise serializers.ValidationError({'amount': 'На балансе не достаточно средств'})
        if not User.objects.filter(wallet_address=attrs['to_address']).exists():
            raise serializers.ValidationError({'to_adress': 'Такого адреса не существует'})
        return attrs

    def create(self, validated_data: dict):
        from_user = User.objects.get(pk=self.context['request'].user.id)
        to_user = User.objects.get(wallet_address=validated_data['to_address'])
        from_user.wallet_amount = from_user.wallet_amount - validated_data['amount']
        from_user.save()
        to_user.wallet_amount = to_user.wallet_amount + validated_data['amount']
        to_user.save()
        transaction = Transaction.objects.create(
            from_user=from_user,
            from_address=from_user.wallet_address,
            to_user=to_user,
            to_address=to_user.wallet_address,
            amount=validated_data['amount']
        )
        transaction.save()
        return transaction


class UserDetailSerializer(serializers.ModelSerializer):
    user_transactions = UserTransactionsSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'age', 'phone_number',
                  'date_joined', 'wallet_address', 'wallet_amount', 'user_transactions')
