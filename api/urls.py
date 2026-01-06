from django.urls import path
from .views import *

urlpatterns = [
    path('register-user/', RegistrationView.as_view(), name='register-user'),
    path('', HouseView.as_view(), name='home')
]
