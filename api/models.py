from django.db import models
from django.contrib.auth.models import AbstractUser
from main.settings import AUTH_USER_MODEL
from cities_light.models import Country, Region

#USER MODEL

class CustomUSer(AbstractUser):
    ROLE_CHOICES = (
        ("User", "User"),
        ("Agent", "Agent"),
    )
    roles = models.CharField(max_length=40, choices=ROLE_CHOICES, default="User")


class AgentUser(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Success", "Success"),
        ("Failed", "Failed"),
    )

    user = models.OneToOneField(CustomUSer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    about = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    bvn_number = models.CharField(max_length=50, null=True, blank=True)
    nin_document = models.ImageField(null=True, blank=True, upload_to="media")
    profile_img = models.ImageField(null=True, blank=True)
    Rating = models.PositiveIntegerField(null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    verification_step = models.CharField(max_length=10, default="1")

    def __str__(self):
        return f"{self.user.username}"

class HouseModel(models.Model):
    CATEGORY_CHOICES = (
        ("ONE_BEDROOM", "One Bedroom"),
        ("TWO_BEDROOM", "Two Bedroom"),
        ("THREE_BEDROOM", "Three Bedroom"),
        ("SELFCON", "Selfcon"),
    )

    house_agent = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    house_name = models.CharField(max_length=100)
    house_description = models.CharField(max_length=1500)
    house_location = models.CharField(max_length=500)
    house_images = models.ImageField(upload_to="media")
    house_price = models.CharField(max_length=30)
    house_size = models.CharField(max_length=30)
    house_rooms_no = models.CharField(max_length=30)
    house_toilet_no = models.CharField(max_length=30)
    house_amenties = models.CharField(max_length=1500)
    house_category = models.CharField(max_length=80, choices=CATEGORY_CHOICES)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True)
    state = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null= True, blank=True)