from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    # path('google-token/', views.GoogleTokenCode.as_view(), name='google-token'),
    # path('facebook-token/', views.FacebookTokenCode.as_view(), name='facebook-token'),

]
