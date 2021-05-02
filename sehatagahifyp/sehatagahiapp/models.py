from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import file_size
from datetime import datetime, date


# Create your models here.
class User(AbstractUser):
    is_therapist = models.BooleanField('therapist status', default=False)
    is_patient = models.BooleanField('patient status', default=False)


    def  getTherapist(self):
        if  self.is_therapist:
            allTherapists = Therapist.objects.all()
            for therapist in allTherapists:
                if therapist.user == self:
                    return therapist
            return None
        return None

    def  getPatient(self):
        if  self.is_patient:
            allPatients = Patient.objects.all()
            for patient in allPatients:
                if patient.user_ID == self:
                    return patient
            return None
        return None



class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=64)
    MobileNumber = models.CharField(max_length=11)
    WorkEmail = models.CharField(max_length=64)
    SecurityQs1 = models.CharField(max_length=64)
    SecurityQs2 = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.id}: Name: {self.name} Email: {self.email}"

    def addTrack(self, name):
        track = Track(name = name, creator = self)
        track.save()
        return track

    def viewMyTracks(self):
        allTracks = Track.objects.all()
        myTracks = []
        for track in allTracks:
            if track.creator == self:
                myTracks.append(track)
        return myTracks

    def getMyPatients(self):
        allPatients = Patient.objects.all()
        myPatients = []
        for patient in allPatients:
            if patient.Therapist == self:
                myPatients.append(patient)
        return myPatients

    def getNumberOfUnreadLogs(self):
        patientList = self.getMyPatients()
        logs = PatientLog.objects.filter(user_ID__in=patientList,isRead = False)
        nUnreadLogs = logs.count()

        return nUnreadLogs





class Patient(models.Model):
    user_ID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Name = models.CharField(max_length=64)
    FatherName = models.CharField(max_length=64)
    DOB = models.DateField()
    Area = models.CharField(max_length=64)
    Gender = models.CharField(max_length=64)
    MobileNumber = models.CharField(max_length=11)
    ConditionTags = models.CharField(max_length=64)
    Therapist = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True, related_name="Patients")



class PatientLog(models.Model):
    user_ID = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, related_name="Log")
    Message = models.TextField(max_length=500)
    DateTimeAdded = models.DateTimeField(auto_now_add = True, blank = True, null=True)
    isRead = models.BooleanField(default=False)

class Patient_Data(models.Model):
    user_ID = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, related_name="Data")
    FilePath = models.CharField(max_length=64)

class Item(models.Model):
    user_ID = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True, related_name="Items")
    Name = models.CharField(max_length=64)
    FilePath = models.FileField(upload_to="Items/")
    Type= models.CharField(max_length=64)


class Track(models.Model):
    user_ID = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True, related_name="Track")
    Name = models.CharField(max_length=64)
    Items = models.ManyToManyField(Item)
class PatientTrack(models.Model):
    user_ID = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, related_name="PatientTrack")
    Track_ID = models.ForeignKey(Track, on_delete=models.SET_NULL, null=True, related_name="PatientTrack")
    Duration = models.IntegerField()
    Notes = models.CharField(max_length=1000)
    isActive = models.BooleanField(default=True)

class PatientProgress(models.Model):
    user_ID = models.ForeignKey(PatientTrack, on_delete=models.SET_NULL, null=True, related_name="PatientProgress")
    Progress = models.CharField(max_length=64)







