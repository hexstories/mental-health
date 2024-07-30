from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _





class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        if not username:
            username = email.split("@")[0][:15]
        user = self.create_user(
            email, username=username, password=password, **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, models.Model):
    email = models.EmailField(
        _("Email address"),
        unique=True,
        validators=[MinLengthValidator(8)],
    )
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into the admin site"),
    )
    password = models.CharField(
        _("Password"),
        blank=False,
        max_length=128,
        validators=[MinLengthValidator(8)],
    )
    is_verified = models.BooleanField(_("Is Verified"), default=False)
    deleted = models.BooleanField(_("Deleted"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["created_at"]

    def _str_(self):
        return self.email

    def get_short_name(self):
        return self.email