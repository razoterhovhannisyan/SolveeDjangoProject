from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.TeamUser)
admin.site.register(models.SoloUser)
