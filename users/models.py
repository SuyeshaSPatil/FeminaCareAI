# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # Add additional fields here if needed, beyond what AbstractUser provides
    # Example: email = models.EmailField(_('email address'), unique=True) # AbstractUser already has email
    pass # For now, just inheriting is fine to make it swappable

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('admin', 'Admin'),
        # Add other roles as needed (e.g., 'doctor')
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='profile_pics/default.jpg')
    # Add other profile-specific fields

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.get_role_display()})"

    @property
    def is_patient(self):
        return self.role == 'patient'

    @property
    def is_admin(self):
        return self.role == 'admin'