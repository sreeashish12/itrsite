from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import ModelFormWithFileField,FileFieldForm
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login,authenticate, logout
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
import os
import PyPDF2
import spacy
import re
from spacy.matcher import Matcher
import pandas as pd 
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt
import smtplib
from . import resumeParser
from django.conf import settings

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("login")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("initialize")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	return redirect("login")

def start(request):
    try:
        for file in os.scandir(settings.MEDIA_ROOT):
            os.remove(file.path)
        #os.chdir("..")
    except:
        pass
    # Folder Path
    #path = "media"

    # Change the directory
    os.chdir(settings.MEDIA_ROOT)

    return render(request,'home.html',{'form':FileFieldForm()})

def home(request):
    return render(request,'home.html',{'form':FileFieldForm()})

def upload(request):
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            # file is saved
            for f in files:
                file_instance = ModelFormWithFileField(file_field=f)
                file_instance.save()
                resumeParser.ResumeParser()
        return HttpResponseRedirect('/table')
    else:
        form = FileFieldForm()
    return render(request, 'upload.html', {'form': form})
    
def table(request):
    df = pd.read_csv('result.csv')
    ctx ={}
    ctx['header'] = ['Name','DOB','Gender','Email ID','Phone Number','Current Position','Current Company','Current Location','Experience','Salary','Highest Degree','Notice Period','Pref Location','Key Skills']
    ctx['rows'] = []
    for i in range(len(df)):
        ctx['rows'].append({'Name':df.iloc[i]['Name'],
                            'DOB':df.iloc[i]['DOB'],
                            'Gender':df.iloc[i]['Gender'],
                            'Email':df.iloc[i]['Email ID'],
                            'Phone':df.iloc[i]['Phone Number'],
                            'Position':df.iloc[i]['Current Position'],
                            'Company':df.iloc[i]['Current Company'],
                            'Location':df.iloc[i]['Current Location'],
                            'Salary':df.iloc[i]['Salary'],
                            'Experience':df.iloc[i]['Experience'],
                            'Degree':df.iloc[i]['Highest Degree'],
                            'Notice':df.iloc[i]['Notice Period'],
                            'Pref':df.iloc[i]['Pref Location'],
                            'Key':df.iloc[i]['Key Skills']
                            })
    
    return render(request,'table.html',ctx)

def stats(request):
    df=pd.read_csv('result.csv')
    plt.hist(df['Current Position'])
    plt.xlabel("Current Position")
    plt.ylabel("No. of applicants")
    plt.title("Current Position Statistics")
    plt.show()
    plt.savefig('stat.png')
    return render(request,'stat.html')

def send(request,phone):
    try:
        phone = int(phone)
    except ValueError as e:
        pass
    row_index=0
    df = pd.read_csv('result.csv')
    for i in range(len(df)):
        if phone == df.iloc[i]['Phone Number']:
            print(df.iloc[i]['Name'])
            row_index=i
            break
    name = df.iloc[i]['Name']
    emailID = df.iloc[i]['Email ID']
    print(name,emailID)
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    email = 'xyz@gmail.com'
    password = '0000000'
    smtp.login(email,password)
    msg = MIMEMultipart()
    msg['Subject'] = "Shortlisted"
    msg.attach(MIMEText("Hello " + name + ",\n" + "You have been short listed for the interviews"))
    smtp.sendmail(from_addr=email,
                    to_addrs=emailID, msg=msg.as_string())
    smtp.quit()
    return render(request,'sendMail.html',{'name':name})
