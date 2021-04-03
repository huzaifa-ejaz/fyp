from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("therapist-register", views.therapist_register, name="therapist-register"),
    path("logout", views.logout_view, name="logout"),
    path("therapist-login", views.loginUser, name="therapist-login"),
    path("login-options", views.getLoginOptions, name="login-options"),
    path("item-upload", views.ItemUpload_view, name="itemupload"),
    path("add-patient", views.addPatient, name="add-patient"),
    path("therapist-dashboard", views.getTherapistDashboard, name="therapist-dashboard")

]




