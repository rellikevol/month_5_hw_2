from django.contrib import admin
from users.models import User, Transaction
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'date_joined', 'wallet_address', 'phone_number')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'amount', 'created_at')
    search_fields = ('from_user', 'to_user', 'amount', 'created_at')