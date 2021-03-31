from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import file_size


# Create your models here.
class User(AbstractUser):
    is_therapist = models.BooleanField('therapist status', default=False)
    is_patient = models.BooleanField('patient status', default=False)



class Therapist(models.Model):
    user_ID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Name = models.CharField(max_length=64)
    MobileNumber = models.CharField(max_length=11)
    WorkEmail = models.CharField(max_length=64)
    SecurityQs1 = models.CharField(max_length=64)
    SecurityQs2 = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.id}: Name: {self.name} Email: {self.email}"


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
    Message = models.CharField(max_length=64)
    Time = models.CharField(max_length=64)

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
    Duration = models.CharField(max_length=64)
    Notes = models.CharField(max_length=64)

class PatientProgress(models.Model):
    user_ID = models.ForeignKey(PatientTrack, on_delete=models.SET_NULL, null=True, related_name="PatientProgress")
    Progress = models.CharField(max_length=64)







