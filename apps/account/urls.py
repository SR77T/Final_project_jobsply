from django.urls import path
from . import views

urlpatterns = [
    path("user-register", views.UserRegisterView.as_view(), name = "user_register"),
    path("user-login", views.UserLoginView.as_view(), name = "user_login"),
    path("user-logout/", views.user_Logout, name = "user_Logout"),
    path("update-profile/<int:pk>/", views.UserProfileUpdateView.as_view(), name="update_profile"),
    path("activate/<str:username>/<str:key>/", views.UserAccountActivationView.as_view(), name = "account_activation"),
    path("resend-activation/<int:id>/", views.ResendEmailActivation.as_view(), name = "resend_ac_activation"),
    path("user-profile/<int:pk>/", views.UserProfileView.as_view(), name = "user_profile"),
    


    

    



]

