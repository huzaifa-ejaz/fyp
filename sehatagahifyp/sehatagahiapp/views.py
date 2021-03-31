from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import Item_form,Therapist_Register_form






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
        if therapist.user_ID == request.user:
            t = therapist

    return render(request, "sehatagahiapp/user.html", {"therapist": t})

def therapist_register(request):
    if request.method == 'POST':
        form=Therapist_Register_form(request.POST)
        if form.is_valid():
            user = get_user_model().objects.create_user(username = form.cleaned_data['Username'] , password = form.cleaned_data['Password']  , is_therapist = True)
            user.save()
            t = Therapist(user_ID = user, Name = form.cleaned_data['Name'], MobileNumber = form.cleaned_data['MobileNumber'],WorkEmail=form.cleaned_data['WorkEmail'],SecurityQs1=form.cleaned_data['SecurityQs1'],SecurityQs2=form.cleaned_data['SecurityQs2'] )
            t.save()
            return HttpResponseRedirect(reverse("therapist-login"))
    else:
        form=Therapist_Register_form()

    return render(request, "sehatagahiapp/register.html",{'form':form})



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

def ItemUpload_view(request):
    all_Item=Item.objects.all()
    therapists = Therapist.objects.all()
    if request.method=="POST":
        form=Item_form(request.POST,request.FILES)
        if form.is_valid():
            for t in therapists:
                if t.user_ID == request.user:
                    break;
            I=Item(user_ID=t,Name= form.cleaned_data['Name'],FilePath= form.cleaned_data['FilePath'],Type=form.cleaned_data['Type'])
            I.save()
            return HttpResponseRedirect(reverse("item-upload"))
    else:
        form=Item_form()
    return render(request,'sehatagahiapp/itemupload.html',{"form":form,"all":all_Item})
