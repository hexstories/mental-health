from django.db import models


class Counselor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def total_appointments_completed(self):
        return self.appointment_set.filter(status=Appointment.Status.COMPLETED).count()
    
    @property
    def total_appointments_pending(self):
        return self.appointment_set.filter(status=Appointment.Status.PENDING).count()
    
    @property
    def total_appointments_cancelled(self):
        return self.appointment_set.filter(status=Appointment.Status.CANCELLED).count()

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending'
        COMPLETED = 'Completed'
        CANCELLED = 'Cancelled'

    counselor = models.ForeignKey('Counselor', on_delete=models.CASCADE)
    student = models.CharField(max_length=255)
    date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.student} - {self.counselor}"


# class BookingAnalytics(models.Model):
#     counselor = models.ForeignKey('Counselor', on_delete=models.CASCADE)
#     total_appointments = models.IntegerField(default=0)
#     completed_appointments = models.IntegerField(default=0)
#     pending_appointments = models.IntegerField(default=0)

#     def __str__(self):
#         return f"Analytics for {self.counselor}"
