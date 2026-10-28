
from django.urls import path

from users import views
from .custom_jwt_claims import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path(
        'token/',
        CustomTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('register/', views.Register.as_view(), name='register-user'),
    path('me/', views.Me.as_view(), name='user'),
]
