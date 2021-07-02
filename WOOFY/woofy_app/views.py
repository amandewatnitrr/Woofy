from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .form import RegisterForm,SigninForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings	
from django.contrib import messages
from .models import Userprofile

def home(request):
	return render(request,'woofy_app/home.html')

def main(request):
	return render(request,'woofy_app/main.html')

def signupuser(request):
	if request.method=='GET':
		return render(request, 'woofy_app/signupuser.html',{'form':RegisterForm()})
	else:	
		if request.POST['password']==request.POST['confirm_password']:
			check_mail_already_exist = User.objects.filter(email=request.POST['email'])
			if(check_mail_already_exist.exists()):
				messages.success(request,'Email already taken')
				return render(request, 'woofy_app/signupuser.html',{'form':RegisterForm(),'error':'Email already taken'})
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
			return redirect('home')
		else:
			messages.success(request,'passwords didnt matched')
			return render(request, 'woofy_app/signupuser.html',{'form':RegisterForm(),'error':'passwords didnt matched'})


@login_required
def logoutuser(request):
	if request.method=='POST':
		logout(request)
		return redirect('signupuser')


def loginuser(request):
	if request.method=='GET':
		return render(request, 'woofy_app/loginuser.html',{'form':SigninForm()})
	else:
		user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
		if user is None:
			messages.success(request,'username and password is incorrect')
			return render(request, 'woofy_app/loginuser.html',{'form':SigninForm(),'error':'username and password is incorrect'})
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
		form.save()
		return redirect('profileview')