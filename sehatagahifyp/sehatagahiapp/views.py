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
from django.db.models import Q
from datetime import date
import pandas as pd
# The sidebar options defined in a dictionary with the URL name as the key

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
therapistOptions = {
    'add-patient' : "Add New Patient",
    'item-upload' : "Upload an Item",
    'view-item' : "View/Edit Item",
    'therapist-dashboard' : "Return to Dashboard",
    'make-track': "Make a Track",
    'view-edit-tracks' : "View/Edit My Tracks"


}


therapistPatientOptions = {
    'edit-patient' : "Edit Patient Details",
    'therapist-patient-page' : "Return to Patient's Page",
    'change-patient-password' : "Change Patient's Password",
    'view-logs' : "View Patient's Logs",
    'view-report':"View Reports",
    'choose-track' : "Assign a Track to Patient"
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
            return HttpResponseRedirect(reverse("login-options"))
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
    return render(request, "sehatagahiapp/login-options.html", {
                "message": "Logged Out"
            })



def ItemUpload_view(request):
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
        'nUnread' : therapist.getNumberOfUnreadLogs()
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
        "patients" : patientList,
        "nUnread" : therapist.getNumberOfUnreadLogs()
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
        'nUnread' : therapist.getNumberOfUnreadLogs(),
        'form' : form
    }
    return render(request, "sehatagahiapp/patient-register.html",context)

@login_required
def getTherapistPatientPage(request,pk):
    today=date.today()
    therapist = request.user.getTherapist()
    try:
        patient = Patient.objects.get(pk=pk, Therapist = therapist)
    except Patient.DoesNotExist:
        patient = None
    
    if patient == None:
        return HttpResponseRedirect(reverse('access-restricted'))
    
    patientTracks = PatientTrack.objects.filter(user_ID = patient)

    datframelist = list()
    tracknames = list()
    for pt in patientTracks:
        tracknames.append(pt.Track_ID.Name)
        items = pt.Track_ID.Items.all()
        index = list()
        for i in items:
            index.append(i.pk)
        columnrange = ((today - pt.Date_Assign).days) // 7
        df = pd.DataFrame(index=index, columns=range(0, columnrange + 1, 1))
        patprog = PatientProgress.objects.filter(PTrack_ID=pt)
        for progress in patprog:
            df.loc[progress.Item_No, progress.Week] = progress.Done_Time
        datframelist.append(df)

    htmltable = list()
    for df in datframelist:
        df.rename(columns=lambda x: "Week " + str(x), inplace=True)
        # df.index=range(0,len(index)+1,1)
        df.rename(index=lambda x: "Item " + str(x), inplace=True)
        htmltable.append(df.to_html(justify='justify-all', classes='table table-striped table-hover table-bordered'))
    
    name_table = zip(tracknames,htmltable)
    context = {
        'heading' : patient.Name,
        'sidebarOptions' : therapistPatientOptions,
        'name' : therapist.Name,
        'nUnread' : therapist.getNumberOfUnreadLogs(),
        'patient' : patient,
        'patientTracks' : patientTracks,
        'name_table':name_table
    }
    return render(request, "sehatagahiapp/therapist-patient-page.html", context)

def restrictAccess(request):
    if request.user.is_therapist:
        therapist = request.user.getTherapist()
        context = {
            'name' : therapist.Name,
            'sidebarOptions' : therapistOptions,
            'nUnread' : therapist.getNumberOfUnreadLogs()
        }
        return render(request, 'sehatagahiapp/restrict-access.html', context)
    else: #When the logged in user is a patient
        patient = request.user.getPatient()
        return HttpResponseRedirect(reverse('patient-dashboard'))

@login_required
def editPatient(request,pk):
    therapist = request.user.getTherapist()
    try:
        patient = Patient.objects.get(pk=pk, Therapist = therapist)
    except Patient.DoesNotExist:
        patient = None
    
    if patient == None:
        return HttpResponseRedirect(reverse('access-restricted'))

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
        'sidebarOptions' : therapistPatientOptions,
        'nUnread' : therapist.getNumberOfUnreadLogs()
    }

    return render(request, 'sehatagahiapp/edit-patient.html',context)

@login_required
def changePatientPassword(request,pk):
    therapist = request.user.getTherapist()
    try:
        patient = Patient.objects.get(pk=pk, Therapist = therapist)
    except Patient.DoesNotExist:
        patient = None
    
    if patient == None:
        return HttpResponseRedirect(reverse('access-restricted'))
    
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
               'nUnread' : therapist.getNumberOfUnreadLogs(),
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
        'sidebarOptions' : therapistPatientOptions,
        'nUnread' : therapist.getNumberOfUnreadLogs()
    }
    return render (request,'sehatagahiapp/patient-password-change.html',context)

@login_required
def getPatientDashboard(request):
    user = request.user
    patient = user.getPatient()
    today = date.today()
    #today = date(2021, 5, 18)
    patientTracks = PatientTrack.objects.filter(user_ID = patient, isActive = True)
    datframelist=list()
    tracknames = list()
    for pt in patientTracks:
        tracknames.append(pt.Track_ID.Name)
        items=pt.Track_ID.Items.all()
        index=list()
        for i in items:
            index.append(i.pk)
        columnrange = ((today - pt.Date_Assign).days) // 7
        df=pd.DataFrame(index=index , columns=range(0,columnrange+1,1))
        patprog = PatientProgress.objects.filter(PTrack_ID=pt)
        for progress in patprog:
            df.loc[progress.Item_No,progress.Week]=progress.Done_Time
        datframelist.append(df)

    htmltable=list()
    for df in datframelist:
        df.rename(columns=lambda x: "Week "+str(x), inplace=True)
        #df.index=range(0,len(index)+1,1)
        df.rename(index=lambda x: "Item " + str(x), inplace=True)
        htmltable.append(df.to_html(justify='justify-all',classes='table table-striped table-hover table-bordered'))

    name_table_list = zip(tracknames,htmltable)

    context = {
        "name": patient.Name,
        "sidebarOptions" : patientOptions,
        "patient" : patient,
        "patientTracks" : patientTracks,
        "name_table": name_table_list
    }

    return render(request, "sehatagahiapp/patient-dashboard.html", context)

@login_required
def addLog(request):
    user = request.user
    patient = user.getPatient()

    if request.method == 'POST':
        form = PatientLogForm(request.POST)
        if form.is_valid():
            log = PatientLog(
                user_ID = patient,
                Message = form.cleaned_data['message']
            )
            log.save()
            newForm = PatientLogForm()
            logs = PatientLog.objects.filter(user_ID = patient)
            lifoLogs = list(reversed(logs))
            context = {
                "name": patient.Name,
                "sidebarOptions": patientOptions,
                "heading": "اہم واقعات",
                "patient" : patient,
                "message": "اہم واقعہ محفوظ کرلیا گیا ہے",
                "form": newForm,
                "logs" : lifoLogs
            }
            return render(request, "sehatagahiapp/patient-add-log.html", context)
    else:
        form = PatientLogForm()
        logs = PatientLog.objects.filter(user_ID = patient)
        lifoLogs = list(reversed(logs))
        context = {
                "name": patient.Name,
                "sidebarOptions": patientOptions,
                "heading": "اہم واقعات",
                "patient" : patient,
                "form": form,
                "logs": lifoLogs
            }

    return render(request, "sehatagahiapp/patient-add-log.html", context)

@login_required
def viewPatientLogs(request,pk):
    therapist = request.user.getTherapist()
    try:
        patient = Patient.objects.get(pk=pk, Therapist = therapist)
    except Patient.DoesNotExist:
        patient = None
    
    if patient == None:
        return HttpResponseRedirect(reverse('access-restricted'))
    patientLogs = PatientLog.objects.filter(user_ID = patient)
    lifoLogs = list(reversed(patientLogs))
    context ={
        "name" : therapist.Name,
        "nUnread" : therapist.getNumberOfUnreadLogs,
        "sidebarOptions" : therapistPatientOptions,
        "logs" : lifoLogs,
        "patient" : patient
    }

    return render(request, "sehatagahiapp/therapist-view-patient-log.html", context)

@login_required
def markLogRead(request,pk,log_pk):
    # This methods marks the log as read and redirects to the specific patient's logs page
    therapist = request.user.getTherapist()
    try:
        patient = Patient.objects.get(pk=pk, Therapist = therapist)
    except Patient.DoesNotExist:
        patient = None
    
    if patient == None:
        return HttpResponseRedirect(reverse('access-restricted'))
    log = get_object_or_404(PatientLog,pk=log_pk)
    log.isRead = True
    log.save()

    return HttpResponseRedirect(reverse('view-logs', kwargs = { 'pk' : pk}))

@login_required
def viewUnreadLogs(request):
    therapist = request.user.getTherapist()
    patientList = therapist.getMyPatients()
    logs = PatientLog.objects.filter(user_ID__in=patientList,isRead = False)
    lifoLogs = list(reversed(logs))

    context = {
        'name':therapist.Name,
        'sidebarOptions': therapistOptions,
        'nUnread' : therapist.getNumberOfUnreadLogs(),
        'heading' : 'Unread Patient Logs',
        'logs' : lifoLogs
    }

    return render(request, 'sehatagahiapp/therapist-view-unread-logs.html', context)

@login_required
def markUnreadLogRead(request,log_pk):
    # This method marks the log as read and redirects to the unread logs page
    log = get_object_or_404(PatientLog,pk=log_pk)
    therapist = request.user.getTherapist()
    if therapist != log.user_ID.Therapist:
        return HttpResponseRedirect(reverse('access-restricted'))

    log.isRead = True
    log.save()

    return HttpResponseRedirect(reverse('view-unread-logs'))

#*******************************************************need to set url restrictions for below views****************

@login_required
def viewItem(request):
    therapist = request.user.getTherapist()
    all_Item = Item.objects.filter(user_ID = therapist)
    
    context = {
        'heading': 'Item View/Edit',
        'name': therapist.Name,
        'sidebarOptions': therapistOptions,
        'all': all_Item,
        'therapistid':therapist.id
    }
    return render(request, 'sehatagahiapp/Item-view.html', context)

@login_required
def updateItem(request,pk):
    
    therapist = request.user.getTherapist()
    instance = Item.objects.get(pk=pk)
    if instance.user_ID != therapist:
        return HttpResponseRedirect(reverse('access-restricted'))
    if request.method == "POST":
        form = Item_Rename_form(request.POST)
        if form.is_valid():
            instance = Item.objects.get(pk=pk)
            instance.Name = form.cleaned_data['ReName']
            instance.save()
            return HttpResponseRedirect(reverse("view-item"))
    else:
        form = Item_Rename_form()

    context = {
        'heading': 'Item Edit',
        'name': therapist.Name,
        'sidebarOptions': therapistOptions,
        'form': form,
        'itempk':pk
    }
    return render(request, 'sehatagahiapp/Item-Update.html', context)

@login_required
def deleteItem(request,pk):
    therapist = request.user.getTherapist()
    deleteitem=Item.objects.get(pk=pk)
    if deleteitem.user_ID != therapist:
        return HttpResponseRedirect(reverse('access-restricted'))
    os.remove(os.path.join(BASE_DIR,str(deleteitem.FilePath)))
    deleteitem.delete()

    context = {
        'heading': 'Item View/Edit',
        'name': therapist.Name,
        'sidebarOptions': therapistOptions,
        'all': all_Item,
        'therapistid': therapist.id
    }
    return render(request, 'sehatagahiapp/Item-view.html', context)

def viewreport(request,pk):
    therapist = request.user.getTherapist()
    patient = get_object_or_404(Patient, pk=pk)
    if patient.Therapist != therapist:
        return HttpResponseRedirect(reverse('access-restricted'))
    patientreport = Patient_Data.objects.filter(user_ID=patient)
    liforeports = list(reversed(patientreport))
    context = {
        'heading': 'View Report',
        "name": therapist.Name,
        "nUnread": therapist.getNumberOfUnreadLogs,
        "sidebarOptions": therapistPatientOptions,
        "reports": liforeports,
        "patient": patient
    }
    return render(request, 'sehatagahiapp/view-report.html',context)

def addreport(request,pk):
    therapist = request.user.getTherapist()
    patient = get_object_or_404(Patient, pk=pk)
    if patient.Therapist != therapist:
        return HttpResponseRedirect(reverse('access-restricted'))
    if request.method == "POST":
        form = AddReportForm(request.POST, request.FILES)
        if form.is_valid():
            pd = Patient_Data(user_ID=patient, Name=form.cleaned_data['Name'], FilePath=form.cleaned_data['FilePath'])
            pd.save()
            return HttpResponseRedirect(reverse("view-report",kwargs={'pk':pk}))
    else:
        form = AddReportForm()
    context = {
        'heading': 'Add Report',
        "name": therapist.Name,
        "nUnread": therapist.getNumberOfUnreadLogs,
        "sidebarOptions": therapistPatientOptions,
        "patient": patient,
        "form": form
    }
    return render(request, 'sehatagahiapp/add-report.html', context)

@login_required
def makeTrack(request):
    therapist = request.user.getTherapist()

    if request.method == "POST":
        form = TrackNameForm(request.POST)
        if form.is_valid():
            track = Track(user_ID = therapist, Name= form.cleaned_data['trackName'])
            track.save()
            track_pk = track.id
            return HttpResponseRedirect(reverse('add-remove-item',kwargs = { 'track_pk' : track_pk }))
    else:
        form = TrackNameForm()

    context = {
        'heading': 'Make a Track',
        'name': therapist.Name,
        'sidebarOptions': therapistOptions,
        'form' : form
    }

    return render(request, 'sehatagahiapp/therapist-track-name.html', context)

@login_required
def addRemoveItem(request, track_pk):
    therapist = request.user.getTherapist()
    track = get_object_or_404(Track, pk=track_pk)
    if track.user_ID != therapist:
        return HttpResponseRedirect(reverse('access-restricted'))
    trackItems = track.Items.all()
    items = Item.objects.exclude(track = track_pk)
    query = request.GET.get("q")
    if query:
        items = items.filter(
        Q(Name__icontains=query)
        )
    context = {
        'heading': f'Track : {track.Name}',
        'name': therapist.Name,
        'sidebarOptions': therapistOptions,
        'trackItems' : trackItems,
        'items' : items,
        'track_pk' : track_pk
    }
    return render(request, 'sehatagahiapp/therapist-add-remove-items.html', context)

@login_required
def addItemToTrack(request,track_pk,item_pk):
    therapist = request.user.getTherapist()
    track = get_object_or_404(Track, pk = track_pk)
    if track.user_ID != therapist:
        return HttpResponseRedirect(reverse('access-restricted'))
    item = get_object_or_404(Item, pk = item_pk)
    track.Items.add(item)
    return HttpResponseRedirect(reverse('add-remove-item', kwargs = { 'track_pk' : track_pk }))

@login_required
def removeItemFromTrack(request,track_pk,item_pk):
    therapist = request.user.getTherapist()
    track = get_object_or_404(Track, pk = track_pk)
    if track.user_ID != therapist:
        return HttpResponseRedirect(reverse('access-restricted'))
    item = get_object_or_404(Item, pk = item_pk)
    track.Items.remove(item)
    return HttpResponseRedirect(reverse('add-remove-item', kwargs = { 'track_pk' : track_pk }))

@login_required
def getEditTracksPage(request):
    therapist = request.user.getTherapist()
    therapistTracks = Track.objects.filter(user_ID = therapist)

    context = {
        'heading': "My Tracks",
        'name': therapist.Name,
        'sidebarOptions': therapistOptions,
        'myTracks' : therapistTracks
    }

    return render(request, 'sehatagahiapp/therapist-view-edit-tracks.html', context)

@login_required
def renameTrack(request,track_pk):
    therapist = request.user.getTherapist()
    track = get_object_or_404(Track, pk = track_pk)
    if track.user_ID != therapist:
        return HttpResponseRedirect(reverse('access-restricted'))
    if request.method == 'POST':
        form = TrackNameForm(request.POST)
        if form.is_valid():
            track.Name = form.cleaned_data['trackName']
            track.save()

            return HttpResponseRedirect(reverse('view-edit-tracks'))
    else:
        form = TrackNameForm( initial = {
            'trackName' : track.Name
        })

    context = {
        'heading': "Rename Track",
        'name': therapist.Name,
        'sidebarOptions': therapistOptions,
        'track' : track,
        'form' : form
    }

    return render(request, 'sehatagahiapp/therapist-rename-track.html', context)

@login_required
def getTracksToAssign(request, patient_pk):
    therapist = request.user.getTherapist()
    patient = get_object_or_404(Patient, pk = patient_pk)
    if patient.Therapist != therapist:
        return HttpResponseRedirect(reverse('access-restricted'))
    all_tracks = Track.objects.all()

    context = {
        'heading': "Choose Track",
        'name': therapist.Name,
        'sidebarOptions': therapistPatientOptions,
        'tracks' : all_tracks,
        'patient_pk' : patient_pk
    }

    return render(request, 'sehatagahiapp/therapist-choose-track.html', context)

@login_required
def assignTracktoPatient(request,patient_pk,track_pk):
    therapist = request.user.getTherapist()
    track = get_object_or_404(Track, pk = track_pk)
    trackItems = track.Items.all()
    patient = get_object_or_404(Patient, pk = patient_pk)
    if patient.Therapist != therapist:
        return HttpResponseRedirect(reverse('access-restricted'))

    if request.method == 'POST':
        form = TrackAssignForm(request.POST)

        if form.is_valid():
            patient_track = PatientTrack(
                user_ID = patient,
                Track_ID = track,
                Duration = form.cleaned_data['duration'],
                Notes = form.cleaned_data['notes']
            )

            patient_track.save()

            return HttpResponseRedirect(reverse('therapist-patient-page', kwargs = {"pk" : patient_pk }))
    else:
        form = TrackAssignForm()
    context = {
        'heading': "Assign Track",
        'name': therapist.Name,
        'sidebarOptions': therapistPatientOptions,
        'patient' : patient,
        'track' : track,
        'trackItems' : trackItems,
        'form' : form
    }

    return render(request, 'sehatagahiapp/therapist-assign-track.html', context)

@login_required
def changeTrackStatus(request,patient_pk,patient_track_pk):
    therapist = request.user.getTherapist()
    patient = get_object_or_404(Patient, pk=patient_pk)
    if patient.Therapist != therapist:
        return HttpResponseRedirect(reverse('access-restricted'))
    patientTrack = get_object_or_404(PatientTrack, pk = patient_track_pk)
    if patientTrack.isActive:
        patientTrack.isActive = False
    else:
        patientTrack.isActive = True
    patientTrack.save()

    return HttpResponseRedirect(reverse('therapist-patient-page', kwargs = { 'pk' : patient_pk }))


def updatePatientProgress(request,item_pk,pt_pk):
    patient = request.user.getPatient()
    patrack = get_object_or_404(PatientTrack, pk=pt_pk)
    if patrack.user_ID != patient:
        return HttpResponseRedirect(reverse('access-restricted'))
    today = date.today()
    #today=date(2021, 5, 30)
    weekno=((today-patrack.Date_Assign).days)//7
    patprog = PatientProgress.objects.filter(PTrack_ID=patrack)
    if len(patprog)==0:
        P=PatientProgress(PTrack_ID=patrack,Week=weekno,Item_No=item_pk,Done_Time=1)
        P.save()
    else:
        try:
            record=PatientProgress.objects.get(PTrack_ID=patrack ,Week=weekno, Item_No=item_pk)
            record.Done_Time=record.Done_Time+1
            record.save()
        except PatientProgress.DoesNotExist:
            P = PatientProgress(PTrack_ID=patrack, Week=weekno, Item_No=item_pk, Done_Time=1)
            P.save()

    return HttpResponseRedirect(reverse('patient-dashboard'))

def viewVideoItem(request,item_pk):
    therapist = request.user.getTherapist()
    video = get_object_or_404(Item, pk = item_pk)

    context = {
        'heading' : f'View: {video.Name}',
        'name' : therapist.Name,
        'sidebarOptions' : therapistOptions,
        'video' : video
    }
    
    return render(request, 'sehatagahiapp/therapist-view-video.html', context)


