from django.db import models
from Users.models import CustomUser, SoloUser, TeamUser

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    about = models.TextField()
    members = models.ManyToManyField(CustomUser, related_name='teams', limit_choices_to={'user_type':'Team'})
    works_done = models.PositiveIntegerField()
    contacts = models.CharField(max_length=300)
    email = models.EmailField()



    def __str__(self):
        return self.name + ' id ' + str(self.id)


class Review(models.Model):
    team = models.ForeignKey(Team, on_delete = models.CASCADE, null = True, related_name = 'review_set')
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdat = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    solo_user = models.ForeignKey(SoloUser, on_delete=models.SET_NULL, null=True)
    booking_date = models.DateField()
    description = models.TextField()




class Offer(models.Model):
    accepted_booking_request = models.OneToOneField('AcceptedBookingRequest', on_delete=models.SET_NULL, related_name = 'offer_relation', null=True)
    amount = models.CharField(max_length=50)
    message = models.TextField()
    solo_user = models.ForeignKey(SoloUser, on_delete=models.SET_NULL, related_name='booked_by',null=True)




class PendingOffer(models.Model):
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE, related_name='pending_offer')
    created_at = models.DateTimeField(auto_now_add=True)





class AcceptedOffer(models.Model):
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE, related_name='accepted_offer')
    created_at = models.DateTimeField(auto_now_add=True)





class RejectedOffer(models.Model):
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE, related_name='rejected_offer')
    created_at = models.DateTimeField(auto_now_add=True)





class PendingBookingRequest(models.Model):
    booking_request = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='pending_booking_request')
    created_at = models.DateTimeField(auto_now_add=True)





class AcceptedBookingRequest(models.Model):
    booking_request = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='accepted_booking_request')
    created_at = models.DateTimeField(auto_now_add=True)




class RejectedBookingRequest(models.Model):
    booking_request = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='rejected_booking_request')
    created_at = models.DateTimeField(auto_now_add=True)





class Calendar(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    available_date = models.DateField()
