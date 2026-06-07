import os

from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import Stage
# Create your models here.


ROLES = [
    ('admin','admin'),
    ('teacher','teacher'),
    ('assistant','assistant'),
    ('parent','parent'),
    ('student','student'),
]

def upload_path(instance,filename):
    return os.path.join('images','avatars',str(instance.username),filename)
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20,null=True,blank=True)
    birth_date = models.DateField(null=True,blank=True)
    parent_phone = models.CharField(max_length=20,null=True,blank=True)
    role = models.CharField(max_length=50,choices=ROLES,default="student")
    image = models.ImageField(upload_to=upload_path,blank=True,null=True)
    slogan = models.CharField(max_length=100, default="شاطر",null=True,blank=True)
    stage = models.ForeignKey(Stage,on_delete=models.SET_NULL,related_name="students",null=True,blank=True)

