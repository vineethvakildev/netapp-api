from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class AllDevices(models.Model):

    host = models.GenericIPAddressField()
    device_type = models.CharField(max_length=20)
    device_params = models.CharField(max_length=20)
    platform = models.CharField(max_length=20, default='cisco_xr')
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    hostkey_verify = models.BooleanField(default=False)
    allow_agent = models.BooleanField(default=False)
    port = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(65535)])

    def __str__(self):
        return self.host

