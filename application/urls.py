from django.urls import path
from . import views

urlpatterns = [
    path('createteam/', views.CreateTeamView.as_view(), name='create-team'),
    path('postreview/', views.PostReviewView.as_view(), name='post-review'),
    path('searchteam/', views.SearchTeamView.as_view(), name='search-team'),
    path('teamlist/', views.TeamListView.as_view(), name = 'team-list'),
    path('teamdetails/<int:pk>/', views.TeamDetailView.as_view(), name = 'team-details'),
    path('teamreviews/<int:pk>/', views.TeamReviewsView.as_view(), name = 'teamreviews'),
    path('bookrequest/', views.BookingRequestTeamView.as_view(), name = 'book-request'),
    path('acceptandrejectbookingrequest/', views.AcceptAndRejectBookingView.as_view(), name = 'acceptandreject-bookingrequest'),
    path('sendoffer/', views.SendOfferToSoloUserView.as_view(), name = 'send-offer'),
    path('acceptandrejectoffer/', views.AcceptAndRejectOfferView.as_view(), name= 'acceptandreject-offer')
]
