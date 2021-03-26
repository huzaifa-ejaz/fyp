from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("therapist-register", views.therapist_register, name="therapist-register"),
    path("logout", views.logout_view, name="logout"),
    path("therapist-login", views.login_view, name="therapist-login"),

    #path("add-track", views.add_track, name="add-track"),
    path("item-upload", views.ItemUpload_view, name="itemupload")

]




