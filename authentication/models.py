from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

class UserProfile(models.Model):
    # user contains username and password
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Officer(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    is_on_duty = models.BooleanField(default=False)
    supervisor_no = models.CharField(null=True, max_length=15)
    duty_coord_lat = models.FloatField(null=True, blank=True)
    duty_coord_long = models.FloatField(null=True, blank=True)
    radius_of_duty = models.FloatField(null=True, blank=True)
    duty_time_start = models.DateTimeField(null=True, blank=True)
    duty_time_end = models.DateTimeField(null=True, blank=True)

    def clean(self):
        # Check if the supervisor_no corresponds to an existing Supervisor
        if not Supervisor.objects.filter(user_profile__phone_no=self.supervisor_no).exists():
            raise ValidationError(f'Supervisor with phone number {self.supervisor_no} does not exist.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user_profile.user.username

class Supervisor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_profile.user.username
