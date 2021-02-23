from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Therapist
from django.contrib.auth import get_user_model
from django.urls import reverse






# Create your views here.

def index(request):
	users = get_user_model().objects.all()
	therapists = Therapist.objects.all()
	return render(request, "sehatagahiapp/index.html",{"my_users": users, "therapists": therapists})

def therapist_register(request):
	if request.method == 'POST':
		user = get_user_model().objects.create_user(username = request.POST["username"] , password = request.POST["password"]  , is_therapist = True)
		user.save()
		t = Therapist(user = user, name = request.POST["name"], mobile_no = request.POST["mobilenumber"] )
		t.save()
	    
		return HttpResponseRedirect(reverse("index"))
	return render(request, "sehatagahiapp/register.html")
