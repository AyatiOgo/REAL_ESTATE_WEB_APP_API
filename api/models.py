from django.db import models
from django.contrib.auth.models import AbstractUser

#USER MODEL

class CustomUSer(AbstractUser):
    ROLE_CHOICES = (
        ("User", "User"),
        ("Agent", "Agent"),
    )

    roles = models.CharField(max_length=40, choices=ROLE_CHOICES, default="User")


class AgentUser(models.Model):
    user = models.OneToOneField(CustomUSer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    about = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    bvn_number = models.CharField(max_length=50, null=True, blank=True)
    nin_document = models.ImageField(null=True, blank=True, upload_to="media")
    profile_img = models.ImageField(null=True, blank=True)