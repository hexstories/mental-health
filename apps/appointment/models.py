from django.db import models
from ..student.models import User
from django.utils.translation import gettext_lazy as _
from ..counselors.models import Counselor
from django.core.exceptions import ValidationError
from django.utils import timezone

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")

    @property
    def is_completed(self):
        return self.status == "completed"

    @classmethod
    def count_total_appointments(cls, user):
        if hasattr(user, "counselor"):
            return cls.objects.filter(counselor=user.counselor).count()
        return cls.objects.filter(user=user).count()

    @classmethod
    def count_completed_appointments(cls, user):
        if hasattr(user, "counselor"):
            return cls.objects.filter(counselor=user.counselor, status="completed").count()
        return cls.objects.filter(user=user, status="completed").count()

    def clean(self):
        if self.date < timezone.now():
            raise ValidationError(_("Appointment date must be in the future."))

    def __str__(self):
        return f"Appointment with {self.counselor.name} on {self.date.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ["date"]
