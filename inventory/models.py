from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

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


class Item(models.Model):
    class Unit(models.TextChoices):
        PCS = "pcs", "pcs"
        KG = "kg", "kg"
        G = "g", "g"
        L = "l", "L"
        ML = "ml", "mL"
        PACK = "pack", "pack"

    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name="items")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="items"
    )
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    unit = models.CharField(max_length=10, choices=Unit.choices, default=Unit.PCS)
    expiry_date = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["expiry_date", "name"]

    @property
    def is_expired(self):
        return self.expiry_date is not None and self.expiry_date < timezone.localdate()

    @property
    def is_expiring_soon(self):
        if self.expiry_date is None or self.is_expired:
            return False
        return self.expiry_date <= timezone.localdate() + timedelta(days=7)

    def __str__(self):
        return f"{self.name} in {self.storage.name}"