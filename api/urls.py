from django.urls import path
from .views import RegistrationView

urlpatterns = [
    path('register-user/', RegistrationView.as_view(), name='register-user')
]
