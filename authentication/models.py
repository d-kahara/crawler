from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """ Base class for all users"""
    is_verified = models.BooleanField(default=False,)
    # this is to track the changes on the model.

    class Types(models.TextChoices):
        """User types"""
        DEV = "DEV", "Dev"
        ADMIN = "ADMIN", "Admin"

    base_type = Types.ADMIN

    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )
    email = models.CharField(_("email of User"), unique=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.base_type
    
        return super().save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

""" ===================================== Proxy Model Managers ================= """
class DevManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.DEV)


""" ============================== Proxy Models =================================== """

class Dev(User):
    """class to create student objects & associated attributes"""
    base_type = User.Types.DEV
    objects = DevManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.DEV
            self.set_password(self.password)
        return super().save(*args, **kwargs)

    class Meta:
        proxy = True
