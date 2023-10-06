from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='static\img\profile_pics', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Info(models.Model):
    topic = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='static\img\info', blank=True, null=True)
    group = models.TextField()
    createdBy = models.ForeignKey(Profile, on_delete=models.CASCADE,null=False)
    # 感情のカテゴリ 一番最初：感情（True = positive, False = negative） 2つ目:文化的 (True= 文化的, false = 文化的でない) 3つ目：フィジカル(True= フィジカルである, False = フィジカルでない)
    # Category for emotion 1st emotional(True = positive) and 2nd cultural, 3rd physical  
    emotion = models.BooleanField()
    cultural = models.BooleanField()
    physical = models.BooleanField()
    # Location data
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField()

    def __str__(self):
        return self.topic
    
    class Meta:
        ordering = ['-created']


