from django.urls import path

from .views import (
    AlertAPIView,
    AssetsAPIView,
    RuleAPIView
)

urlpatterns = [
    path('asset/<str:id>', AssetsAPIView.as_view(), name='get_asset'),
    path('asset/', AssetsAPIView.as_view(), name='asset'),
    path('alert/<str:id>', AlertAPIView.as_view(), name='get_alert'),
    path('alert/', AlertAPIView.as_view(), name='alert'),
    path('rule/', RuleAPIView.as_view(), name="post_rule")
]
