from django.test import SimpleTestCase
from django.urls import reverse, resolve
from assests.views import (
    AlertAPIView,
    AssetsAPIView,
    RuleAPIView
)

class ApiUrlsTests(SimpleTestCase):
    
    def test_AssetsAPIView_is_resolved(self):
        """
        django urls unit testing to see if it is firing the correct(AssetsAPIView) ViewClass.
        """
        url = reverse('get_asset', kwargs={'id':1})
        self.assertEquals(resolve(url).func.view_class, AssetsAPIView)
        
    def test_get_AlertAPIView_is_resolved(self):
        """
        django urls unit testing to see if it is firing the correct(AssetsAPIView) ViewClass.
        """
        url = reverse('get_alert', kwargs={'id':1})
        self.assertEquals(resolve(url).func.view_class, AlertAPIView)
        
    def test_AlertAPIView_is_resolved(self):
        """
        django urls unit testing to see if it is firing the correct(AlertAPIView) ViewClass.
        """
        url = reverse('alert')
        self.assertEquals(resolve(url).func.view_class, AlertAPIView)
        
           
    def test_RuleAPIView_is_resolved(self):
        """
        django urls unit testing to see if it is firing the correct(RuleAPIView) ViewClass.
        """
        url = reverse('post_rule')
        self.assertEquals(resolve(url).func.view_class, RuleAPIView)

   