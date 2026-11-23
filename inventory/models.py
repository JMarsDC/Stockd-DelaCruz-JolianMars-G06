from django.conf import settings
from django.db import models


class Storage(models.Model):
    class StorageType(models.TextChoices):
        PANTRY = "pantry", "Pantry"
        FRIDGE = "fridge", "Refrigerator"
        FREEZER = "freezer", "Freezer"
        SHELF = "shelf", "Store shelf"
        OTHER = "other", "Other"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="storages",
    )
    name = models.CharField(max_length=100)
    storage_type = models.CharField(
        max_length=20, choices=StorageType.choices, default=StorageType.PANTRY
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"], name="unique_storage_name_per_owner"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.owner.username})"