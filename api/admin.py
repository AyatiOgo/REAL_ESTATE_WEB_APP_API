from django.contrib import admin
from .models import AgentUser, CustomUSer, HouseModel
from django.contrib.admin import ModelAdmin
# Register your models here.

class AgentAdmin(ModelAdmin):
    list_display = ["user", "first_name", "verification_status", "verification_step" ]

admin.site.register(AgentUser, AgentAdmin)

class HouseAdmin(ModelAdmin):
    list_display = ["house_name", ]

admin.site.register(HouseModel, HouseAdmin )