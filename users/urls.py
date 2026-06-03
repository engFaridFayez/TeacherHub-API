from django.urls import path

from users import views

from .custom_jwt_claims import CustomTokenObtainPairView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

]