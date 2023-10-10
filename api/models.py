from django.db import models
from django.contrib.auth.models import User

Default_Profile_Image = 'static\img\profile_pics\default.png'

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='static\img\profile_pics', default=Default_Profile_Image)

    def __str__(self):
        return '{}_{}'.format(self.id,self.user.username) if self.user else 'User Not Found'        

class Info(models.Model):
    topic = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='static\img\info', blank=False, null=False)
    group = models.TextField()
    createdBy = models.ForeignKey(Profile, on_delete=models.CASCADE,null=False)
    # Category data 
    emotion = models.BooleanField()
    cultural = models.BooleanField()
    physical = models.BooleanField()
    # Location data
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField()

    def __str__(self):
        return '{}_{}'.format(self.id, self.topic)
    
    class Meta:
        ordering = ['-created']


