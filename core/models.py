from __future__ import annotations

import os
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


def donation_image_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/donations/<id>/<filename>
    return os.path.join('donations', str(instance.id), filename)


class User(AbstractUser):
    class Roles(models.TextChoices):
        DONOR = "donor", "Donor"
        RECEIVER = "receiver", "Receiver"

    role = models.CharField(max_length=20, choices=Roles.choices)
    contact_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r"^[0-9+\-]{6,15}$", "Enter a valid contact number.")],
        blank=True,
    )
    address = models.TextField(blank=True)

    @property
    def is_donor(self) -> bool:
        return self.role == self.Roles.DONOR

    @property
    def is_receiver(self) -> bool:
        return self.role == self.Roles.RECEIVER


class Donation(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        CLAIMED = "claimed", "Claimed"
        EXPIRED = "expired", "Expired"

    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donations")
    food_name = models.CharField(max_length=150)
    description = models.TextField()
    quantity = models.CharField(max_length=120)
    address = models.CharField(max_length=255)
    available_till = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-available_till", "status"]

    def __str__(self) -> str:
        return f"{self.food_name} ({self.donor.username})"

    @property
    def is_active(self) -> bool:
        return self.status == self.Status.AVAILABLE and self.available_till >= timezone.now()


class FoodRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name="requests")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="food_requests")
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("donation", "receiver")
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return f"Request by {self.receiver.username} for {self.donation.food_name}"


class Contact(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Contact message from {self.name}"
