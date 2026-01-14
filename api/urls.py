from django.urls import path
from .views import *

urlpatterns = [
    path('register-user/', RegistrationView.as_view(), name='register-user'),
    path('', HouseView.as_view(), name='home'),
    path('upload-house/', HouseView.as_view(), name='upload-house'),
    path('agent-profile-verification/', AgentProfileVerificationView.as_view(), name='agent-profile-verification'),
    path('agent-kyc-verification/', AgentKYCView.as_view(), name='agent-kyc-verification'),
    path('agent-profile/<str:user>/', AgentProfileView.as_view(), name='agent-profile'),
    path('user-profile/<str:user>/', UserProfileView.as_view(), name='user-profile'),
]