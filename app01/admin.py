from django.contrib import admin
from app01 import models
# Register your models here.
admin.site.register(models.Commodity)
admin.site.register(models.F2C)
admin.site.register(models.Factory)
admin.site.register(models.UserInfo)
admin.site.register(models.Message)
