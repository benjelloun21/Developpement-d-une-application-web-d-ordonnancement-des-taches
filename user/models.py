from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class profile(models.Model):
    staff=models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    adress=models.CharField(max_length=200)
    phone=models.CharField(max_length=20,null=True)
    image=models.ImageField(default='avatar.jpg',upload_to='profile_images')
    jobtitle =models.CharField(max_length=200,default='-')
    def __str__(self):
      return f'{self.staff.username}-profile'