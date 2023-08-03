from django.test import SimpleTestCase
from django.urls import reverse, resolve
from authentication.views import HandleRegister, CustomTokenObtainPairView, UpdateProfileView, UserDetailsAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenBlacklistView

class ApiUrlsTests(SimpleTestCase):
    
    def test_CustomTokenObtainPairView_is_resolved(self):
        """
        django urls unit testing to see if it is firing the correct(CustomTokenObtainPairView) ViewClass.
        """
        url = reverse('token_obtain_pair')
        self.assertEquals(resolve(url).func.view_class, CustomTokenObtainPairView)
        
    def test_HandleRegister_is_resolved(self):
        """
        django urls unit testing to see if it is firing the correct(HandleRegister) ViewClass.
        """
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, HandleRegister)
        
    def test_UpdateProfileView_is_resolved(self):
        """
        django urls unit testing to see if it is firing the correct(UpdateProfileView) ViewClass.
        """
        url = reverse('update_profile', kwargs={'pk':1})
        self.assertEquals(resolve(url).func.view_class, UpdateProfileView)
        
    def test_UserDetailsAPIView_is_resolved(self):
        """
        django urls unit testing to see if it is firing the correct(UserDetailsAPIView) ViewClass.
        """
        url = reverse('user_details', kwargs={'id':1})
        self.assertEquals(resolve(url).func.view_class, UserDetailsAPIView)
        
    def test_TokenRefreshView_is_resolved(self):
        """
        django urls unit testing to see if it is firing the correct(TokenRefreshView) ViewClass.
        """
        url = reverse('token_refresh')
        self.assertEquals(resolve(url).func.view_class, TokenRefreshView)

    def test_TokenBlacklistView_is_resolved(self):
        """
        django urls unit testing to see if it is firing the correct(TokenBlacklistView) ViewClass.
        """
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, TokenBlacklistView)
