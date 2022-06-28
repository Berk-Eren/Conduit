from .views import *
from django.urls import path


app_name = "user"

user_detail_update = UserDetailUpdateView.as_view()
user_authentication = UserAuthenticationView.as_view()
user_registration = UserRegistrationView.as_view()


profile_detail = ProfileViewFollowUnfollowView.as_view()
profile_update = ProfileViewFollowUnfollowView.as_view()

urlpatterns = [
    path(r'user/', user_detail_update),
    path(r'users/login/', user_authentication),
    path(r'users/', user_registration)
]

urlpatterns += [
    path(r"profiles/<str:username>/", profile_detail),
    path(r"profiles/<str:username>/follow/", profile_update),
]