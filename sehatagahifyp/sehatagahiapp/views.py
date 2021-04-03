from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Therapist, Item
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import Item_form, LoginForm




therapistOptions = {
    'add-patient' : "Add New Patient"
}

# Create your views here.

# def index(request):
# 	users = get_user_model().objects.all()
# 	therapists = Therapist.objects.all()
# 	return render(request, "sehatagahiapp/index.html",{"my_users": users, "therapists": therapists})

def index(request):
    # If no user is signed in, return to login page:
    if not request.user.is_authenticated:
        return render(request, "sehatagahiapp/base-index.html")
    therapist = request.user.getTherapist()

    return render(request, "sehatagahiapp/user.html", {"therapist": therapist})

def therapist_register(request):
    if request.method == 'POST':
        user = get_user_model().objects.create_user(username = request.POST["username"] , password = request.POST["password"]  , is_therapist = True)
        user.save()
        t = Therapist(user = user, Name = request.POST["name"], MobileNumber = request.POST["mobilenumber"] )
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
    form = LoginForm()
    return render(request, "sehatagahiapp/therapist-login.html", {
                "message": "Logged Out",
                "form" : form
            })



def ItemUpload_view(request):
    all_Item=Item.objects.all()
    if request.method=="POST":
        print("request agai bhai")
        form=Item_form(user=request.user,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            print("saved")
            return HttpResponse("<h1>Uploaded!</h1>")
    else:
        form=Item_form(user=request.user)
    return render(request,'sehatagahiapp/itemupload.html',{"form":form,"all":all_Item})

def getLoginOptions(request):
    return render(request, 'sehatagahiapp/login-options.html')

def loginUser(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Check if username and password are correct, returning User object if so
            user = authenticate(request, username=username, password=password)

            # If user object is returned, log in and route to index page:
            if user:
                login(request, user)
                if user.is_therapist:
                    return HttpResponseRedirect(reverse("therapist-dashboard"))
                elif user.is_patient:
                    return HttpResponseRedirect(reverse("index"))
            # Otherwise, return login page again with new context
            else:
                return render(request, "sehatagahiapp/therapist-login.html", {
                    "message": "Invalid Credentials",
                    "form" : form
                })
            # redirect to a new URL:
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'sehatagahiapp/therapist-login.html', {'form': form})

def getTherapistDashboard(request):
    user = request.user
    therapist = user.getTherapist()
    patientList = therapist.getMyPatients()
    context = {
        "name": therapist.Name,
        "sidebarOptions" : therapistOptions,
        "heading" : "My Patients",
        "patients" : patientList
    }
                    
    return render(request, "sehatagahiapp/therapist-dashboard.html", context)

def addPatient(request):
    return HttpResponse("Add a patient: Work on Page in progress!")