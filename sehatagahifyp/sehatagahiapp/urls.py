from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("therapist-register", views.therapist_register, name="therapist-register"),
    path("logout", views.logout_view, name="logout"),
    path("login/<str:userType>", views.loginUser, name="login"),
    path("login-options", views.getLoginOptions, name="login-options"),
    path("item-upload", views.ItemUpload_view, name="item-upload"),
    path("add-patient", views.addPatient, name="add-patient"),
    path("therapist-dashboard", views.getTherapistDashboard, name="therapist-dashboard"),
    path("patient/<int:pk>", views.getTherapistPatientPage, name="therapist-patient-page"),
    path("patient/<int:pk>/edit", views.editPatient, name="edit-patient"),
    path("patient/<int:pk>/change-password", views.changePatientPassword, name="change-patient-password"),
    path("patient-login", views.loginUser, name="patient-login"),
    path("patient-dashboard", views.getPatientDashboard, name="patient-dashboard"),
    path("patient/add-log", views.addLog, name="add-log"),
    path("patient/<int:pk>/view-logs", views.viewPatientLogs, name="view-logs")
    


]




