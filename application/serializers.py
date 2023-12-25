from rest_framework import serializers
from . import models


class CreateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ['name', 'about', 'works_done', 'contacts', 'email']


class PostReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['rating', 'comment', 'team']


class SearchTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ['name', 'about', 'works_done', 'contacts']


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ['name', 'about', 'works_done', 'contacts', 'email']


class BookTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = ['team', 'solo_user', 'booking_date', 'description']


class TeamReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['rating', 'comment', 'createdat']



class AcceptAndRejectBookingRequestSerializer(serializers.Serializer):
    booking_request_id = serializers.IntegerField()
    answer = serializers.ChoiceField(choices=['accepted', 'rejected'])



class SendOfferToSoloUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offer
        fields = ['accepted_booking_request', 'amount', 'message']


class AcceptAndRejectOfferSerializer(serializers.Serializer):
    offer_id = serializers.IntegerField()
    answer = serializers.ChoiceField(choices=['accepted', 'rejected'])
