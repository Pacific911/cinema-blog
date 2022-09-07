from enum import unique
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
 

class Profile(models.Model):
    user_id = models.IntegerField(default=1)
    gender = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    profile_image = models.ImageField(upload_to="user_images/")


STATUS=((0,"Draft"),(1,"published"))
class Post(models.Model):
    title = models.CharField(max_length=200)
    tags= models.CharField(max_length=200)
    content=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.IntegerField(choices=STATUS, default=0)
    thumbnail = models.ImageField(upload_to='images/')

    class Meta:
        ordering=['-created_on']

    def _str_(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    profile = models.ImageField(upload_to='team')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def _str_(self):
        return self.name

class About(models.Model):
    content = models.TextField()
    profile = models.ImageField(upload_to='service')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def _str_(self):
        return self.content
