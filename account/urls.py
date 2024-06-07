from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
