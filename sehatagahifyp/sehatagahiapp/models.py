from django.db import models
from django.contrib.auth.models import AbstractUser



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



class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64, null = True)
    mobile_no = models.CharField(max_length=11)
    
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

class Track(models.Model):
    name = models.CharField(max_length=64)
    creator = models.ForeignKey(Therapist, on_delete = models.DO_NOTHING)
    










