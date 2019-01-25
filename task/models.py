from django.db import models

# Create your models here.
class Task (models.Model):
    titel = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    taskuserid = models.IntegerField(default=0)

    def __str__(self):
        return self.titel