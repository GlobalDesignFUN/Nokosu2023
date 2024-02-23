from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

Default_Profile_Image = 'static\img\profile_pics\default.png'

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='static\img\profile_pics', default=Default_Profile_Image)
    url = models.TextField(blank=True)

    def __str__(self):
        return '{}_{}'.format(self.id,self.user.username) if self.user else 'User Not Found'        

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    createdBy = models.ForeignKey(Profile, on_delete=models.CASCADE,null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Info(models.Model):
    topic = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='static\img\info', blank=False, null=False)
    url = models.TextField(blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=False)
    createdBy = models.ForeignKey(Profile, on_delete=models.CASCADE,null=False)
    # Category data 
    positive = models.IntegerField(validators=[MinValueValidator(-10), MaxValueValidator(10)])
    emotion = models.IntegerField(validators=[MinValueValidator(-10), MaxValueValidator(10)])
    cultural = models.IntegerField(validators=[MinValueValidator(-10), MaxValueValidator(10)])
    physical = models.IntegerField(validators=[MinValueValidator(-10), MaxValueValidator(10)])
    tags = models.TextField(blank=True)
    # Location data
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField()

    def __str__(self):
        return '{}_{}'.format(self.id, self.topic)
    
    class Meta:
        ordering = ['-created']