from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    phone_number = models.CharField(max_length=13, verbose_name="Номер телефона")
    age = models.IntegerField(default=0, verbose_name="Возраст")
    wallet_address = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Адрес кошелька")
    wallet_amount = models.FloatField(default=0, verbose_name="Сумма на счету")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Transaction(models.Model):
    from_user = models.OneToOneField(User, on_delete=models.DO_NOTHING, verbose_name="От кого", related_name='from_user')
    to_user = models.OneToOneField(User, on_delete=models.DO_NOTHING, verbose_name="Кому", related_name='to_user')
    is_completed = models.BooleanField(default=False, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата")
    amount = models.FloatField(default=0, verbose_name="Сумма")

    def __str__(self):
        return f"{self.from_user.username} - {self.to_user.username}, сумма: {self.amount}"

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
