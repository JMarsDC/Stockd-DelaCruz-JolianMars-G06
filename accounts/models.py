from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        USER = "customer", "Customer"
        ADMIN = "admin", "Admin"
    
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length = 10,
        choices = Role.choices,
        default = Role.USER
    )
    contact_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"