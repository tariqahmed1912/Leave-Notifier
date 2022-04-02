from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import pandas as pd
from django.contrib.auth.models import User
from django.contrib import messages
import datetime
import matplotlib.pyplot as plt
import numpy as np
from django.core.mail import send_mail
from Leave_Notifier import settings
from app1.models import UserDetails, FacultyDetails

# Create your views here.
def login(request):
    if request.user.is_anonymous == False:
        return redirect('/home')

    if request.method == "POST":
        user = request.POST['name']
        password = request.POST['pswd']

        user = authenticate(username = user, password=password)
        
        if user is not None:
            auth_login(request,user)

            return redirect('/home')
        else:
            return redirect('/')
    if request.user.is_anonymous:
        return render(request, 'login.html')
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

def home(request):
    if request.user.is_anonymous:
        return redirect('/')
    if request.user.user_details.role == "Faculty":
        if request.method == "POST":
            date = request.POST['date']
            no_of_days = request.POST['no_of_days']
            reason = request.POST['reason']
            print(type(no_of_days))
            new = FacultyDetails(user=request.user.username, dept=request.user.user_details.dept, date_of_leave = date, no_of_days=no_of_days, reason= reason)
            new.save()

            hod_name = UserDetails.objects.get(dept=request.user.user_details.dept, role="HOD").user.username
            hod_email = User.objects.get(username = hod_name).email

            faculty_email = request.user.email

            # For testing
            faculty_email = "tariqahmed1912@gmail.com"
            hod_email = "tariqahmed1912@gmail.com"
            content = "Greetings,\nI would like to get permission for leave for " + no_of_days + " days \n""Reason - " + reason
            subject = "Leave application from " + request.user.username
            send_mail(subject, content, faculty_email, [hod_email], fail_silently=False)
            
            return redirect('/')
        faculty_details = FacultyDetails.objects.filter(user=request.user.username).order_by('date_of_leave')[::-1]
        return render(request, 'faculty_home.html', {'faculty_details':faculty_details})
        #return render(request, 'faculty_home.html')

    if request.user.user_details.role == "HOD":
        if request.method=="POST":
            print(request.POST)
            name = request.POST['user']
            date_of_leave = request.POST['date_of_leave']
            
            print(date_of_leave, name)
            faculty_details = FacultyDetails.objects.filter(user=name, date_of_leave=date_of_leave)[0]
            faculty_details_history = FacultyDetails.objects.filter(user=faculty_details.user).order_by('date_of_leave')[::-1]
            
            total = 0
            for i in faculty_details_history:
                if i.permission == 0:
                    total += i.no_of_days

            return render(request, 'hod_check.html',{'faculty_details':faculty_details, 'faculty_details_history':faculty_details_history, 'total':total})

        faculty_details = FacultyDetails.objects.filter(dept=request.user.user_details.dept, permission=-1).order_by('date_of_leave')[::-1]
        return render(request, 'hod_home.html',{'faculty_details':faculty_details})



def check(request):
    if request.method == "POST":
        user = request.POST['user']
        date_of_leave = request.POST['date_of_leave']
        no_of_days = request.POST['no_of_days']
        if "accept" in request.POST:
            FacultyDetails.objects.filter(user=user, date_of_leave=date_of_leave, no_of_days=no_of_days).update(permission=0)
        elif "reject" in request.POST:
            FacultyDetails.objects.filter(user=user, date_of_leave=date_of_leave, no_of_days=no_of_days).update(permission=1)

        return redirect('/home')

# def form(request):
#     if request.method == "POST":
#         date = request.POST['date']
#         no_of_days = request.POST['no_of_days']
#         reason = request.POST['reason']
#         print(type(no_of_days))
#         new = FacultyDetails(user=request.user.username, dept=request.user.user_details.dept, date_of_leave = date, no_of_days=no_of_days, reason= reason)
#         new.save()

#         hod_name = UserDetails.objects.get(dept=request.user.user_details.dept, role="HOD").user.username
#         hod_email = User.objects.get(username = hod_name).email

#         faculty_email = request.user.email

#         # For testing
#         faculty_email = "tariqahmed1912@gmail.com"
#         hod_email = "tariqahmed1912@gmail.com"
#         content = "Greetings,\nI would like to get permission for leave for " + no_of_days + " days \n""Reason - " + reason
#         subject = "Leave application from " + request.user.username
#         send_mail(subject, content, faculty_email, [hod_email], fail_silently=False)
        
#         return redirect('/')

#     return render(request, 'faculty_home.html')

