from django.urls import path


from .views import (
    HandleIotThings,
    HandleSendCommand,
    HandleGetDataView,
)

urlpatterns = [
    path('things/<str:id>/',HandleIotThings.as_view(), name='things'),
    path('get_data/<str:id>/',HandleGetDataView.as_view(), name='things'),
    path('send_command/',HandleSendCommand.as_view(), name='send-command'),
    path('get_data/',HandleGetDataView.as_view(), name='get_data'),
]
