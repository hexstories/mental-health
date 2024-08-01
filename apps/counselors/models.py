from django.db import models

class Counselor(models.Model):
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
    
#     @property
#     def total_appointments_completed(self):
#         return self.appointment_set.filter(status=Appointment.Status.COMPLETED).count()
    
#     @property
#     def total_appointments_pending(self):
#         return self.appointment_set.filter(status=Appointment.Status.PENDING).count()
    
#     @property
#     def total_appointments_cancelled(self):
#         return self.appointment_set.filter(status=Appointment.Status.CANCELLED).count()

# class Appointment(models.Model):
#     class Status(models.TextChoices):
#         PENDING = 'Pending'
#         COMPLETED = 'Completed'
#         CANCELLED = 'Cancelled'

    # counselor = models.ForeignKey('Counselor', on_delete=models.CASCADE)
    # student = models.CharField(max_length=255)
    # date = models.DateTimeField()
    # status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)

    


