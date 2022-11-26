from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from rest_framework.authtoken.models import Token

User = get_user_model()
class MessageUser(models.Model):
    massageUser = models.ForeignKey(User,on_delete=models.CASCADE,unique=True)
    
    
    def __str__(self):
        return self.massageUser.username


class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    receiver= models.IntegerField(default="")
    subject= models.CharField(max_length=50)
    message = models.TextField(max_length=300)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):return str(self.sender.id) + " to id user: " + str(self.receiver) + " the subject is: " + self.subject