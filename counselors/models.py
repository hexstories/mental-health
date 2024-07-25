from django.db import models


class Counselor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    counselor = models.ForeignKey('Counselor', on_delete=models.CASCADE)
    student = models.CharField(max_length=255)
    date = models.DateTimeField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.student} - {self.counselor}"

class BookingAnalytics(models.Model):
    counselor = models.ForeignKey('Counselor', on_delete=models.CASCADE)
    total_appointments = models.IntegerField(default=0)
    completed_appointments = models.IntegerField(default=0)
    pending_appointments = models.IntegerField(default=0)

    def __str__(self):
        return f"Analytics for {self.counselor}"
