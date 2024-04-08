from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

from . import views
from . import auth


urlpatterns = [
    path('auth/register/', auth.Register.as_view(), name='register'),
    path('auth/login/', auth.LoginView.as_view(), name='login'),
    path('auth/logout/', auth.LogoutView.as_view(), name='logout'),
    path('auth/changepassword/', auth.ChangePasswordView.as_view(), name='changepassword'),
    # path('users/', views.UserViewSet.as_view(), name='users'),
    # path('groups/', views.GroupViewSet.as_view(), name='groups'),
    path('cuisines/', views.CuisineView.as_view(), name='cuisines'),
    path('userpost/', views.UserPostView.as_view(), name='userpost'),
    path('reviews/<int:cuisine_id>/',
         views.UserReviewClass.as_view(), name='review'),
    path('meals/', views.MealView.as_view(), name='meals'),
    path('location/', views.LocationDetailView.as_view(), name='location'),
    path("cuisines/<int:cuisine_id>/menu/", views.CuisineBasedMenuView.as_view(), name  = 'restaurant menu'),
    path("cuisines/<int:cuisine_id>/", views.GetSpecificCuisineView.as_view(), name = 'cuisine')   
]

urlpatterns = format_suffix_patterns(urlpatterns)