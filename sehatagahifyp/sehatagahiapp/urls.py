from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("therapist-register", views.therapist_register, name="therapist-register")
]




