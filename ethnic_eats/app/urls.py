from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

from . import views
from . import auth
from . import userpost, reviews, reservations, gemini
from . import inquiries
from . import resetpassword
from . import rating


urlpatterns = [
    path('auth/register/', auth.Register.as_view(), name='register'),
    path('auth/login/', auth.LoginView.as_view(), name='login'),
    path('auth/logout/', auth.LogoutView.as_view(), name='logout'),
    path('auth/user/', auth.UserInfoView.as_view(), name= 'userinfo'),
    path('cuisines/', views.CuisineView.as_view(), name='cuisines'),
        path('cuisines/owner/', views.CuisineOwnerView.as_view(), name='cuisines_owner'),
    path('userpost/', userpost.UserPostView.as_view(), name='userpost'),
    path('reviews/<int:cuisine_id>/',
         reviews.UserReviewClass.as_view(), name='review'),
    path('reviews/', reviews.GetAllReviews.as_view(), name='all reviews'),
    path('meals/', views.MealView.as_view(), name='meals'),
    path('location/', views.LocationDetailView.as_view(), name='location'),
    path("cuisines/<int:cuisine_id>/menu/", views.CuisineBasedMenuView.as_view(), name  = 'restaurant menu'),
    path("cuisines/<int:cuisine_id>/", views.GetSpecificCuisineView.as_view(), name = 'cuisine'),
    path("reservation/user/", reservations.ReservationViewForUser.as_view(), name='reservationforuser'),
    path("reservation/cuisine/<int:cuisine_id>/", reservations.ReservationViewForCuisine.as_view(), name="rservationforcuisine"),
    path("reservation/delete/<int:reservation_id>/", reservations.DeleteReservationView.as_view(), name="deletereservation"),
    path("", views.greetings, name='gretings'),
    path('talk_to_us/', inquiries.InquiryView.as_view(), name = "talk to us"),
    path('reset-request/', resetpassword.PasswordResetRequestView.as_view(), name='reset_request'),
    path('reset-password/<str:uidb64>/<str:token>/', resetpassword.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('meal/<int:meal_id>/', views.SpecificMealView.as_view(), name='meal view'),
    path('gemini/trending-foods/', gemini.TrendingFoods.as_view(), name="Trending foods"),
    path('rated-foods/', rating.HighlyRatedFoods.as_view(), name="recommended foods")
]

urlpatterns = format_suffix_patterns(urlpatterns)