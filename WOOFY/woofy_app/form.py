from django.forms import ModelForm
from django import forms
from .models import Userprofile

class RegisterForm(forms.Form):
	username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control user', 'placeholder': 'Your Name Goes Here...'}))
	email = forms.EmailField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control mail', 'placeholder': 'A Valid Email Address'}))
	password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control pass', 'placeholder': 'Enter A Strong Password'}))
	confirm_password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control confpass', 'placeholder': 'Cross-check Your Password'}))

class SigninForm(forms.Form):
	username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control user', 'placeholder': 'Your Name Goes Here...'}))
	password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control pass', 'placeholder': 'Enter Your Password'}))

class DateInput(forms.DateInput):
	input_type = 'date'

class DateForm(forms.Form):
	my_date_field = forms.DateField(widget=DateInput)

class ProfileForm(ModelForm):
	class Meta:
		model = Userprofile
		fields = ['childs_name','mothers_name','age','birth_date','phone_number','email','address','profile_picture']
		widgets = {'my_date_field':DateInput()}

