from django.db import models
from django.core.validators import RegexValidator

class SiteInfo(models.Model):
    description = models.TextField()
    contact_number = models.CharField(max_length=20)
    office_location = models.CharField(max_length=200)
    office_visit_info = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex="^[A-Za-z\s'-]+$",
                message='Full name must contain only letters'
            )
        ]
    )
    email = models.EmailField(
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._%+-]+@st\.knust\.edu\.gh$',
                message='Email must be a valid KNUST student email'
            )
        ]
    )
    phone_number = models.CharField(max_length=15)
    booking_date = models.DateField()
    message = models.TextField()

    def __str__(self):
        return self.full_name
    

