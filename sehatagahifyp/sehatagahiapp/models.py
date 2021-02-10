from django.db import models

# Create your models here.
class Therapist(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    mobile_no = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.id}: Name: {self.name} Email: {self.email}"

class Track(models.Model):
    name = models.CharField(max_length=64)
    
class Patient(models.Model):
    name = models.CharField(max_length=64)
    father_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=64)
    dob = models.DateField()
    mobile_no = models.CharField(max_length=11)
    condition_type = models.CharField(max_length=64)
    condition_tone = models.CharField(max_length=64)
    therapist = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True, related_name="patients")
    tracks = models.ManyToManyField(Track, blank=True, related_name="patients")









