from django.db import models

# Create your models here.


class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    

class Conversation(models.Model):
    email = models.EmailField()
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.timestamp}"
