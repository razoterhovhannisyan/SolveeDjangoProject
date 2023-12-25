from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Team)
admin.site.register(models.Review)
admin.site.register(models.Booking)
admin.site.register(models.Offer)
admin.site.register(models.PendingOffer)
admin.site.register(models.AcceptedOffer)
admin.site.register(models.RejectedOffer)
admin.site.register(models.PendingBookingRequest)
admin.site.register(models.AcceptedBookingRequest)
admin.site.register(models.RejectedBookingRequest)
admin.site.register(models.Calendar)
