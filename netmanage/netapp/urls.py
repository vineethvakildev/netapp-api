from django.urls import path
from . import views

urlpatterns = [
    path('configure/', views.ConfigureDeviceView.as_view(), name='configure'),
    path('interfaces/', views.ListInterfacesView.as_view(), name='interfaces'),
]