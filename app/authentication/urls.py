from django.urls import path

from .views import (
    HandleRegister,
    HandleLogout,
    HandleHomePage,
    CustomTokenObtainPairView,
    UpdateProfileView,
    UserDetailsAPIView
)

urlpatterns = [
    path('signup/',HandleRegister.as_view(), name='signup'),
    path('home/',HandleHomePage.as_view(), name='home'),
    path('update_profile/<str:pk>/', UpdateProfileView.as_view(), name='update_profile'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user_details/<str:id>', UserDetailsAPIView.as_view(), name='user_details'),
    
]
