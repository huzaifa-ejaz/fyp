from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
import os


# The sidebar options defined in a dictionary with the URL name as the key

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
therapistOptions = {
    'add-patient' : "Add New Patient",
    'item-upload' : "Upload an Item",
    'view-item' : "View/Edit Item",
    'therapist-dashboard' : "Return to Dashboard"

}
therapistOptions = {
    'add-patient' : "Add New Patient",
    'item-upload' : "Upload an Item",
    'therapist-dashboard' : "Return to Dashboard"
}

therapistPatientOptions = {
    'edit-patient' : "Edit Patient Details",
    'therapist-patient-page' : "Return to Patient's Page",
    'change-patient-password' : "Change Patient's Password"
}

patientOptions = {
    'add-log' : "اہم واقعہ نوٹ کریں"
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

    return render(request, "sehatagahiapp/base-index.html")

def therapist_register(request):
    if request.method == 'POST':
        form=Therapist_Register_form(request.POST)
        if form.is_valid():
            user = get_user_model().objects.create_user(username = form.cleaned_data['Username'] , password = form.cleaned_data['Password']  , is_therapist = True)
            user.save()
            t = Therapist(user = user, Name = form.cleaned_data['Name'], MobileNumber = form.cleaned_data['MobileNumber'],WorkEmail=form.cleaned_data['WorkEmail'],SecurityQs1=form.cleaned_data['SecurityQs1'],SecurityQs2=form.cleaned_data['SecurityQs2'] )
            t.save()
            return HttpResponseRedirect(reverse("therapist-login"))
    else:
        form=Therapist_Register_form()

    return render(request, "sehatagahiapp/register.html",{'form':form})



# def login_view(request):
#     if request.method == "POST":
#         # Accessing username and password from form data
#         username = request.POST["username"]
#         password = request.POST["password"]

#         # Check if username and password are correct, returning User object if so
#         user = authenticate(request, username=username, password=password)

#         # If user object is returned, log in and route to index page:
#         if user:
#             login(request, user)
#             return HttpResponseRedirect(reverse("index"))
#         # Otherwise, return login page again with new context
#         else:
#             return render(request, "sehatagahiapp/therapist-login.html", {
#                 "message": "Invalid Credentials"
#             })
#     return render(request, "sehatagahiapp/therapist-login.html")


def logout_view(request):

    logout(request)
    form = LoginForm()
    return render(request, "sehatagahiapp/login.html", {
                "message": "Logged Out",
                "form" : form,
                "userType" : "User"
            })



def ItemUpload_view(request):
    all_Item=Item.objects.all()
    therapist = request.user.getTherapist()
    if request.method=="POST":
        form=Item_form(request.POST,request.FILES)
        if form.is_valid():
            
            I=Item(user_ID=therapist,Name= form.cleaned_data['Name'],FilePath= form.cleaned_data['FilePath'],Type=form.cleaned_data['Type'])
            I.save()
            return HttpResponseRedirect(reverse("item-upload"))
    else:
        form=Item_form()
    context = {
        'heading' : 'Upload an Item',
        'name': therapist.Name,
        'sidebarOptions' : therapistOptions,
        'form' : form,
        'all' : all_Item
    }
    return render(request,'sehatagahiapp/itemupload.html',context)






def getLoginOptions(request):
    return render(request, 'sehatagahiapp/login-options.html')

def loginUser(request, userType):
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

            # If user object is returned, log in and route to user dashboard page ensuring the user has come from the right URL:
            if user:
                if userType == 'Therapist' and user.is_therapist:
                    login(request, user)
                    return HttpResponseRedirect(reverse("therapist-dashboard"))
                elif  userType == 'Caregiver' and user.is_patient:
                    login(request, user)
                    return HttpResponseRedirect(reverse("patient-dashboard"))
                else:
                    return render(request, "sehatagahiapp/login.html", {
                    "userType" : userType,
                    "message": "Invalid Login!",
                    "form" : form
                })

            # Otherwise, return login page again with new context
            else:
                return render(request, "sehatagahiapp/login.html", {
                    "userType" : userType,
                    "message": "Invalid Credentials",
                    "form" : form
                })


    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'sehatagahiapp/login.html', {
        'form': form,
        'userType': userType
        })

@login_required
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

@login_required
def addPatient(request):
    therapist = request.user.getTherapist()
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            user = get_user_model().objects.create_user(username = form.cleaned_data['username'] , password = form.cleaned_data['password']  , is_patient = True)
            user.save()
            patient = Patient(
                user_ID = user,
                Name = form.cleaned_data['name'],
                FatherName = form.cleaned_data['fatherName'],
                DOB=form.cleaned_data['dob'],
                Area=form.cleaned_data['area'],
                Gender=form.cleaned_data['gender'],
                MobileNumber = form.cleaned_data['mobileNumber'],
                ConditionTags = form.cleaned_data['condition'],
                Therapist = therapist )
            patient.save()
            return HttpResponseRedirect(reverse('therapist-dashboard'))
    else:
        form = PatientRegisterForm()
    context = {
        'heading' : 'Create a Patient',
        'name': therapist.Name,
        'sidebarOptions' : therapistOptions,
        'form' : form
    }
    return render(request, "sehatagahiapp/patient-register.html",context)

@login_required
def getTherapistPatientPage(request,pk):
    therapist = request.user.getTherapist()
    patient = Patient.objects.get(pk=pk)
    context = {
        'heading' : patient.Name,
        'sidebarOptions' : therapistPatientOptions,
        'name' : therapist.Name,
        'patient' : patient
    }
    return render(request, "sehatagahiapp/therapist-patient-page.html", context)

@login_required
def editPatient(request,pk):
    therapist = request.user.getTherapist()
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = PatientEditForm(request.POST)
        if form.is_valid():
            patient.Name = form.cleaned_data['name']
            patient.FatherName = form.cleaned_data['fatherName']
            patient.DOB = form.cleaned_data['dob']
            patient.Area = form.cleaned_data['area']
            patient.Gender = form.cleaned_data['gender']
            patient.MobileNumber = form.cleaned_data['mobileNumber']
            patient.ConditionTags = form.cleaned_data['condition']

            patient.save()

            context = {
                'form' : form,
                'name' : therapist.Name,
                'heading': 'Edit Patient Details',
                'sidebarOptions' : therapistPatientOptions,
                'patient': patient,
                'message' : "Patient Details has been successfully updated!"
            }

            return render(request,'sehatagahiapp/edit-patient.html', context)
    else:
        form = PatientEditForm(initial = {
            'name': patient.Name,
            'fatherName' : patient.FatherName,
            'dob' : patient.DOB,
            'area' : patient.Area,
            'gender' : patient.Gender,
            'mobileNumber' : patient.MobileNumber,
            'condition' : patient.ConditionTags

        })

    context = {
        'form' : form,
        'name' : therapist.Name,
        'heading': 'Edit Patient Details',
        'patient' : patient,
        'sidebarOptions' : therapistPatientOptions
    }

    return render(request, 'sehatagahiapp/edit-patient.html',context)

@login_required
def changePatientPassword(request,pk):
    therapist = request.user.getTherapist()
    patient = get_object_or_404(Patient,pk=pk)
    patientUser = User.objects.get(id = patient.user_ID.id)

    if request.method == 'POST':
       form =  PatientPasswordChangeForm(request.POST)
       if form.is_valid():
           patientUser.set_password(form.cleaned_data['password'])
           patientUser.save()
           context = {
               'form' : form,
               'name' : therapist.Name,
               'heading': 'Change Patient\'s Password',
               'patient' : patient,
               'sidebarOptions' : therapistPatientOptions,
               'message' : 'Patient\'s password has been changed!'
           }
           return render (request,'sehatagahiapp/patient-password-change.html',context)
    else:
        form  = PatientPasswordChangeForm(initial = {
            'username' : patientUser.username
        })
    context = {
        'form' : form,
        'name' : therapist.Name,
        'heading': 'Change Patient\'s Password',
        'patient' : patient,
        'sidebarOptions' : therapistPatientOptions
    }
    return render (request,'sehatagahiapp/patient-password-change.html',context)

@login_required
def getPatientDashboard(request):
    user = request.user
    patient = user.getPatient()
    context = {
        "name": patient.Name,
        "sidebarOptions" : patientOptions,
        "heading" : "میرا ٹریک",
        "patient" : patient
    }

    return render(request, "sehatagahiapp/patient-dashboard.html", context)

@login_required
def addLog(request):
    return HttpResponse("Work in progress on this page!")

def viewItem(request):
    all_Item = Item.objects.all()
    therapist = request.user.getTherapist()
    form = Item_Rename_form()
    context = {
        'heading': 'Item View/Edit',
        'name': therapist.Name,
        'sidebarOptions': therapistOptions,
        'form': form,
        'all': all_Item,
        'therapistid':therapist.id
    }
    return render(request, 'sehatagahiapp/Item-view.html', context)


def updateItem(request):
    all_Item = Item.objects.all()
    therapist = request.user.getTherapist()
    if request.method == "POST":
        form = Item_Rename_form(request.POST)
        if form.is_valid():
            renameitem = request.POST['Item']
            instance = Item.objects.get(id=renameitem)
            instance.Name = form.cleaned_data['ReName']
            instance.save()
            return HttpResponseRedirect(reverse("view-item"))
        else:
            renameitem = request.POST['Item']
            instance = Item.objects.get(id=renameitem)
    else:
        form = Item_Rename_form()

    context = {
        'heading': 'Item View/Edit',
        'name': therapist.Name,
        'sidebarOptions': therapistOptions,
        'form': form,
        'all': all_Item,
        'therapistid': therapist.id
    }
    if request.method=="POST":
        context = {
            'heading': 'Item View/Edit',
            'name': therapist.Name,
            'sidebarOptions': therapistOptions,
            'form': form,
            'all': all_Item,
            'therapistid': therapist.id,
            'message':"Could Not Re-Name the Item"+': '+instance.Name
        }
    return render(request, 'sehatagahiapp/Item-view.html', context)


def deleteItem(request):
    all_Item = Item.objects.all()
    therapist = request.user.getTherapist()
    if request.method == "POST":
        delitem = request.POST['Item']
        deleteitem=Item.objects.filter(id=delitem)
        os.remove(os.path.join(BASE_DIR,str(deleteitem[0].FilePath)))
        deleteitem.delete()

        return HttpResponseRedirect(reverse("view-item"))
    else:
        form = Item_Rename_form()

    context = {
        'heading': 'Item View/Edit',
        'name': therapist.Name,
        'sidebarOptions': therapistOptions,
        'form': form,
        'all': all_Item,
        'therapistid': therapist.id
    }
    return render(request, 'sehatagahiapp/Item-view.html', context)

