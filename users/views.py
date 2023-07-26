from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from users.models import User, Transaction
from users.serializers import UserSerializer, UserRegisterSerializer, \
    UserDetailSerializer, UserTransactionsSerializer
from users.permissions import UserPermissions
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserAPIView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('update', 'destroy', 'retrieve'):
            return (UserPermissions(), )
        return (AllowAny(), )

    def get_serializer_class(self):
        if self.action in ('create',):
            return UserRegisterSerializer
        if self.action in ('retrieve',):
            return UserDetailSerializer
        return UserSerializer


class UserTransactionAPIView(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                             mixins.CreateModelMixin, GenericViewSet):

    serializer_class = UserTransactionsSerializer

    def get_queryset(self):
        queryset = Transaction.objects.filter(from_user=self.request.user.id)
        return queryset

    def get_permissions(self):
        if self.action in ('list', 'create'):
            return (UserPermissions(), )
        return (AllowAny(), )
"""
    def get_serializer_class(self):
        self.queryset = self.queryset.filter(from_user=self.request.user.id)
        return UserTransactionsSerializer
    """