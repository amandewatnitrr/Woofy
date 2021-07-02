from django.db import models
from django.contrib.auth.models import User

class Userprofile(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)	
	childs_name= models.CharField(max_length=100,blank=True)
	mothers_name= models.CharField(max_length=100,blank=True)
	age = models.IntegerField(blank=True,null=True)
	birth_date = models.DateField(null=True,blank=True)	
	phone_number = models.BigIntegerField(blank=True,null=True)
	email = models.EmailField(max_length=100,blank=True,null=True)
	address = models.TextField(max_length=400,blank=True,null=True)
	profile_picture = models.ImageField(upload_to='woofy_app/profile_image', blank=True,null=True)
    
	def __str__(self):
		return self.childs_name

	@property	
	def get_photo_url(self):	
		if self.profile_picture and hasattr(self.profile_picture,'url'):
			return self.profile_picture.url
		else:
			return "media/woofy_app/image/chacha.jpg"
