from django.urls import path
from rest_framework.routers import DefaultRouter
from users import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()

router.register('users_list', views.UserAPIView, 'api_users_list')
router.register('user_transactions', views.UserTransactionAPIView, 'api_user_transactions_list')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='api_login'),
    path('refresh/', TokenRefreshView.as_view(), name='api_refresh')
]

urlpatterns += router.urls
