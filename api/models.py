from django.db import models

# Create your models here.

class Info(models.Model):

    topic = models.TextField()  #title a
    description = models.TextField()    #description of post
    created = models.DateTimeField(auto_now_add=True) #time 
    #photo link
    photo = models.ImageField(upload_to='static\img', blank=True, null=True)
    #name of the group 
    group = models.TextField()

    #感情のカテゴリ 一番最初：感情（True = positive, False = negative） 2つ目:文化的 (True= 文化的, false = 文化的でない) 3つ目：フィジカル(True= フィジカルである, False = フィジカルでない)
    #category for emotion 1st emotional(True = positive) and 2nd cultural, 3rd physical  
    category = [models.BooleanField()]*3

    #場所　1st latitude 2nd altitude 3rd address 4th name of the place 
    location = [models.IntegerField(), models.IntegerField(), models.TextField(), models.TextField()]
    #user id
    user_id = models.TextField()


    def __str__(self):
        return self.topic
    
    class Meta:
        ordering = ['-created']