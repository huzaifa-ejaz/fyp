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
    path("patient/<int:pk>/view-logs", views.viewPatientLogs, name="view-logs"),
    path("patient/<int:pk>/log/<int:log_pk>/mark-read", views.markLogRead, name="mark-log"),
    path("view-unread-logs", views.viewUnreadLogs, name="view-unread-logs"),
    path("log/<int:log_pk>/mark-read", views.markUnreadLogRead, name="mark-unread-log"),
    path("item/view", views.viewItem, name="view-item"),
    path("item/<int:pk>/edit", views.updateItem, name="Rename-item"),
    path("item/<int:pk>/delete", views.deleteItem, name="Delete-item"),
    path("patient/<int:pk>/view-report", views.viewreport, name="view-report"),
    path("patient/<int:pk>/add-report", views.addreport, name="add-report"),
    path("make-track", views.makeTrack, name="make-track"),
    path("track/<int:track_pk>/add-remove-item", views.addRemoveItem, name="add-remove-item"),
    path("track/<int:track_pk>/item/<int:item_pk>/add", views.addItemToTrack, name="add-item"),
    path("track/<int:track_pk>/item/<int:item_pk>/remove", views.removeItemFromTrack, name="remove-item"),
    path("view-edit-tracks", views.getEditTracksPage, name="view-edit-tracks"),
    path("track/<int:track_pk>/rename", views.renameTrack, name="rename-track"),
    path("patient/<int:patient_pk>/choose-track", views.getTracksToAssign, name="choose-track"),
    path("patient/<int:patient_pk>/track/<int:track_pk>/assign", views.assignTracktoPatient, name="assign-track"),
    path("patient/<int:patient_pk>/patient_track/<int:patient_track_pk>/change-status", views.changeTrackStatus, name="change-status")




]




