from django.db import models
from django.utils import timezone
from phone_field import PhoneField


class Rehab(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone =  PhoneField(blank=True, help_text='Contact phone number')
    website = models.URLField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
