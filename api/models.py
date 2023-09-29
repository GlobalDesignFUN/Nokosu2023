from django.db import models

# Create your models here.
class Profile(models.Model):
    

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField()

    def __str__(self):
        return self.name

class Info(models.Model):
    topic = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='static\img', blank=True, null=True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True)
    createdBy = models.ForeignKey()

    def __str__(self):
        return self.topic
    
    class Meta:
        ordering = ['-created']


