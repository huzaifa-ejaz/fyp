from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("therapist-register", views.therapist_register, name="therapist-register"),
    path("logout", views.logout_view, name="logout"),
    path("therapist-login", views.loginUser, name="therapist-login"),
    path("login-options", views.getLoginOptions, name="login-options"),
    path("item-upload", views.ItemUpload_view, name="item-upload"),
    path("add-patient", views.addPatient, name="add-patient"),
    path("therapist-dashboard", views.getTherapistDashboard, name="therapist-dashboard"),
    path("view-item", views.viewItem, name="view-item"),
    path("Rename-item", views.updateItem, name="Rename-item"),
    path("Delete-item", views.deleteItem, name="Delete-item")

]




