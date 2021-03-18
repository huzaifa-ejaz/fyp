from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class User(AbstractUser):
    is_therapist = models.BooleanField('therapist status', default=False)
    is_patient = models.BooleanField('patient status', default=False)



class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64, null = True)
    mobile_no = models.CharField(max_length=11)
    
    def __str__(self):
        return f"{self.id}: Name: {self.name} Email: {self.email}"

# class Track(models.Model):
#     name = models.CharField(max_length=64)
    
# class Patient(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     name = models.CharField(max_length=64)
#     father_name = models.CharField(max_length=64)
#     gender = models.CharField(max_length=64)
#     dob = models.DateField()
#     mobile_no = models.CharField(max_length=11)
#     area = models.CharField(max_length=64)
#     condition_type = models.CharField(max_length=64) #To be seen later
#     condition_tone = models.CharField(max_length=64) #To be seen later
#     therapist = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True, related_name="patients")
#     tracks = models.ManyToManyField(Track, blank=True, related_name="patients")









