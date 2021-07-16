from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .form import RegisterForm,SigninForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings	
from django.contrib import messages
from .models import Userprofile
import random
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDQL1f2c5PRaj_1xXxMpdczT8m_bXZ-flM",
    "authDomain": "bmp180-1569c.firebaseapp.com",
    "databaseURL": "https://bmp180-1569c-default-rtdb.firebaseio.com",
    "projectId": "bmp180-1569c",
    "storageBucket": "bmp180-1569c.appspot.com",
    "messagingSenderId": "861317072378",
    "appId": "1:861317072378:web:1dcd26ae45e21b9b549043",
    "measurementId": "G-KS2RHXGSF9"
  };
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
database=firebase.database()

def home(request):
	return render(request,'woofy_app/home.html')

@login_required
def main(request):
	username=request.user.username
	oxysat = database.child('main_test').child(username).child('oxysat').get().val()
	pressure = database.child('main_test').child(username).child('pressure').get().val()
	temperature = database.child('main_test').child(username).child('temp').get().val()
	return render(request,'woofy_app/main.html',{'oxysat':oxysat,'pressure':pressure,'temperature':temperature})

def signupuser(request):
	if request.POST['password']==request.POST['confirmpassword']:
		check_mail_already_exist = User.objects.filter(email=request.POST['email'])
		if(check_mail_already_exist.exists()):
			messages.success(request,'Email already taken')
			return render(request, 'woofy_app/home.html',{'error':'Email already taken'})
		user = User.objects.create_user(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'])
		user.save()
		email_message = request.POST['email']
		send_mail(
			'Welcome To Woofy!',
			'We urge to serve you the best way possible!',
			'dracielraven589@gmail.com',
			[email_message],
			fail_silently=False
			)
		login(request,user)
		user_profile = Userprofile.objects.create(user=request.user,childs_name=request.POST['username'],email=request.POST['email'])
		user_profile.save()
		username=request.POST['username']
		oxysat = random.randint(0,9)
		pressure = random.randint(0,9)
		temp = random.randint(0,9)
		data = {
			"oxysat":oxysat,
			"pressure":pressure,
			"temp":temp
		}
		database.child("main_test").child(username).set(data)
		return redirect('main')
	else:
		messages.success(request,'passwords didnt matched')
		return redirect('home')


@login_required
def logoutuser(request):
	if request.method=='POST':
		logout(request)
		return redirect('home')


def loginuser(request):
	user = authenticate(request, username=request.POST['name'],password=request.POST['passwrd'])
	if user is None:
		messages.success(request,'username and password is incorrect')
		return redirect('home')
	else:
		login(request,user)
		return redirect('main')


@login_required
def profileview(request):
	show = Userprofile.objects.get(user=request.user)
	return render(request,'woofy_app/profile.html',{'profile':show})


@login_required
def profiledit(request):
	show = Userprofile.objects.get(user=request.user)
	if request.method=='GET':
		form = ProfileForm(instance=show)	
		return render(request,'woofy_app/profileedit.html',{'profile':show,'form':form})
	else:
		form = ProfileForm(request.POST, request.FILES, instance=show)
		if(form.is_valid()):
			form.save()
			return redirect('profileview')
		else:
			return redirect('profileview')
