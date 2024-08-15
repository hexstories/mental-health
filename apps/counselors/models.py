from django.db import models
from ..student.models import User

class Counselor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=255, blank=True)
    office_location = models.CharField(max_length=255, blank=True)
    research_areas = models.TextField(blank=True)
    qualifications = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='counselors/', blank=True, null=True)
    cv_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    

