from django.db import models

# Create your models here.

class Info(models.Model):
    topic = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic
    
    class Meta:
        ordering = ['-created']