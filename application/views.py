from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . import models
from . import serializers
from Users.models import CustomUser, SoloUser, TeamUser
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated




class CreateTeamView(APIView):
    def post(self, request, format=None):
        print(request.user.user_type)
        print(type(request.user))
        try:
            user = models.TeamUser.objects.get(email=request.user.email)
        except models.TeamUser.DoesNotExist:
            return Response({'detail':'You dont have permission to create a team:'}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.CreateTeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PostReviewView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error':'Authentication credentials were not provided'}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        if user.user_type != 'Solo':
            return Response({'error':'You dont have permission to post reviews.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.PostReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save()
            team = review.team
            return Response(serializers.PostReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SearchTeamView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        get_data = request.query_params
        all_teams = models.Team.objects.all()
        if get_data:
            if get_data.get('name', ''):
                team = models.Team.objects.filter(name__icontains=get_data['name'])
                serializer = serializers.SearchTeamSerializer(team, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif get_data.get('all', ''):
                fields = [f for f in models.Team._meta.fields if isinstance(f, CharField)]
                queries = [Q(**{f.name + '__icontains': get_data.get('all')}) for f in fields]
                qs = Q()
                for query in queries:
                    qs = qs | query
                team = models.Team.objects.filter(qs)
                serializer = serializers.SearchTeamSerializer(team, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif get_data.get('works_done', '') and get_data.get('contacts', ''):
                works_done_value = get_data.get('works_done')
                contacts_value = get_data.get('contacts')
                team = models.Team.objects.filter(works_done=works_done_value, contacts__icontains=contacts_value)
                serializer = serializers.SearchTeamSerializer(team, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message':'No search criteria provided'}, status=status.HTTP_400_BAD_REQUEST)



class TeamListView(APIView):
    def get(self, request, format=None):
        teams = models.Team.objects.all()
        serializer = serializers.TeamListSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamDetailView(APIView):
    def get(self, request, pk):
        try:
            team = models.Team.objects.get(id=pk)
            serializer = serializers.TeamListSerializer(team)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Team.DoesNotExist:
            return Response({'error':'Team does not exist'}, status=status.HTTP_404_NOT_FOUND)



class TeamReviewsView(APIView):
    def get(self, request, pk):
        try:
            team = models.Team.objects.get(id=pk)
            reviews = models.Review.objects.filter(team=team)
            serializer = serializers.TeamReviewSerializer(reviews, many=True)

            if not reviews:
                return Response({'message':'No reviews yet'}, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Team.DoesNotExist:
            return Response({'error':'Team does not exist'}, status=status.HTTP_404_NOT_FOUND)




class BookingRequestTeamView(APIView):
    def post(self, request):
        solo_user = request.user
        print(request.user.user_type)
        if solo_user.user_type != 'Solo':
            return Response({'message': 'You dont have permission to send Booking request'}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.BookTeamSerializer(data=request.data)
        if serializer.is_valid():
            team_id = serializer.validated_data['team'].id
            booking_date = serializer.validated_data['booking_date']
            description = serializer.validated_data['description']

            if models.Booking.objects.filter(team_id=team_id, booking_date=booking_date).exists():
                return Response({'detail': 'The chosen day is not available. Please choose another day'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                team = models.Team.objects.get(id=team_id)
                team_email = team.email

                if not isinstance(solo_user, models.SoloUser):
                    solo_user = models.SoloUser.objects.get(email=solo_user.email)

                booking = serializer.save(team=team, solo_user=solo_user)


                pending_booking_request = models.PendingBookingRequest.objects.create(booking_request=booking)
                pending_booking_request.save()

                send_mail(
                    'Booking Request',
                    f'You have a booking request from {request.user.username} for {booking_date}. Description: {description}',
                    'rterhovhannisyan7777@gmail.com',
                    [team_email],
                    fail_silently=False,
                )

                return Response({'detail': 'Booking request sent successfully'}, status=status.HTTP_201_CREATED)

            except models.Team.DoesNotExist:
                return Response({'detail': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AcceptAndRejectBookingView(APIView):
    def post(self, request):
        team_user = request.user
        if team_user.user_type != 'Team':
            return Response({'message': 'You dont have permission to accept the booking request'}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.AcceptAndRejectBookingRequestSerializer(data=request.data)
        if serializer.is_valid():
            booking_request_id = serializer.validated_data['booking_request_id']
            answer = serializer.validated_data['answer']

            try:
                pending_booking_request = models.PendingBookingRequest.objects.get(id=booking_request_id)

                if answer == 'accepted':
                    accepted_booking_request = models.AcceptedBookingRequest.objects.create(
                        booking_request=pending_booking_request.booking_request
                    )
                    pending_booking_request.delete()

                    return Response({'detail':'Booking request accepted.'}, status=status.HTTP_200_OK)

                elif answer == 'rejected':
                    rejected_booking_request = models.RejectedBookingRequest.objects.create(
                        booking_request=pending_booking_request.booking_request
                    )
                    pending_booking_request.delete()

                    return Response({'detail':'Booking request rejected'}, status=status.HTTP_200_OK)

                else:
                    return Response({'detail':'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


            except models.Booking.DoesNotExist:
                return Response({'detail': 'Booking request not found'}, status=status.HTTP_404_NOT_FOUND)
            except models.PendingBookingRequest.DoesNotExist:
                return Response({'detail': 'PendingBookingRequest not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SendOfferToSoloUserView(APIView):
    def post(self, request):
        team_user = request.user
        if team_user.user_type != 'Team':
            return Response({'message':'You dont have permission to send offer'}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.SendOfferToSoloUserSerializer(data=request.data)
        if serializer.is_valid():
            accepted_booking_request = serializer.validated_data['accepted_booking_request'].id
            amount = serializer.validated_data['amount']
            message = serializer.validated_data['message']

            try:
                accepted_booking_request = models.AcceptedBookingRequest.objects.get(id=accepted_booking_request)
                solo_user = accepted_booking_request.booking_request.solo_user


                offer = models.Offer.objects.create(
                    accepted_booking_request=accepted_booking_request,
                    amount=amount,
                    message=message,
                    solo_user=solo_user
                )

                pending_offer = models.PendingOffer.objects.create(offer=offer)


                send_mail(
                    'New Offer',
                    f'You have a new offer from {team_user.username} for your booking request. Price: {amount}, Message: {message}',
                    'rterhovhannisyan7777@gmail.com',
                    [solo_user.email],
                    fail_silently=False,
                )

                return Response({'detail': 'Offer sent successfully'}, status=status.HTTP_201_CREATED)

            except models.AcceptedBookingRequest.DoesNotExist:
                return Response({'detail': 'Booking request not found or not accepted'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class AcceptAndRejectOfferView(APIView):
    def post(self, request):
        solo_user = request.user
        if solo_user.user_type != 'Solo':
            return Response({'message':'You dont have permission to do this'}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.AcceptAndRejectOfferSerializer(data=request.data)
        if serializer.is_valid():
            offer_id = serializer.validated_data['offer_id']
            answer = serializer.validated_data['answer']

            try:
                pending_offer = models.PendingOffer.objects.get(id=offer_id)

                if answer == 'accepted':
                    accepted_offer = models.AcceptedOffer.objects.create(
                        offer = pending_offer.offer
                    )
                    pending_offer.delete()

                    return Response({'detail':'Offer accepted.'}, status=status.HTTP_200_OK)

                elif answer == 'rejected':
                    rejected_offer = models.RejectedOffer.objects.create(
                        offer = pending_offer.offer
                    )
                    pending_offer.delete()

                    return Response({'detail':'Offer rejected'},  status=status.HTTP_200_OK)

                else:
                    return Response({'detail':'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

            except models.Offer.DoesNotExist:
                return Response({'detail': 'Offer not found'}, status=status.HTTP_404_NOT_FOUND)
            except models.PendingOffer.DoesNotExist:
                return Response({'detail': 'PendingOffer not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
