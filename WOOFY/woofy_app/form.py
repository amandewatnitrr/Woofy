from django.forms import ModelForm
from django import forms


class RegisterForm(forms.Form):
	username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control user', 'placeholder': 'Your Name Goes Here...'}))
	email = forms.EmailField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control mail', 'placeholder': 'A Valid Email Address'}))
	password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control pass', 'placeholder': 'Enter A Strong Password'}))
	confirm_password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control confpass', 'placeholder': 'Cross-check Your Password'}))

class SigninForm(forms.Form):
	username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control user', 'placeholder': 'Your Name Goes Here...'}))
	password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control pass', 'placeholder': 'Enter Your Password'}))
