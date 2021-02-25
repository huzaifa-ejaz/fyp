from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Therapist
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout







# Create your views here.

# def index(request):
# 	users = get_user_model().objects.all()
# 	therapists = Therapist.objects.all()
# 	return render(request, "sehatagahiapp/index.html",{"my_users": users, "therapists": therapists})

def index(request):
    # If no user is signed in, return to login page:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("therapist-login"))
    therapists = Therapist.objects.all()
    t = None
    for therapist in therapists:
        if therapist.user == request.user:
            t = therapist

    return render(request, "sehatagahiapp/user.html", {"therapist": t})

def therapist_register(request):
    if request.method == 'POST':
        user = get_user_model().objects.create_user(username = request.POST["username"] , password = request.POST["password"]  , is_therapist = True)
        user.save()
        t = Therapist(user = user, name = request.POST["name"], mobile_no = request.POST["mobilenumber"] )
        t.save()
        return HttpResponseRedirect(reverse("therapist-login"))
    return render(request, "sehatagahiapp/register.html")



def login_view(request):
    if request.method == "POST":
        # Accessing username and password from form data
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if username and password are correct, returning User object if so
        user = authenticate(request, username=username, password=password)

        # If user object is returned, log in and route to index page:
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # Otherwise, return login page again with new context
        else:
            return render(request, "sehatagahiapp/therapist-login.html", {
                "message": "Invalid Credentials"
            })
    return render(request, "sehatagahiapp/therapist-login.html")


def logout_view(request):
    logout(request)
    return render(request, "sehatagahiapp/therapist-login.html", {
                "message": "Logged Out"
            })


