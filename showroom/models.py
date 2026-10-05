from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver


class Vehicle(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        IN_PROCESS = "IN_PROCESS", "In process"
        DELIVERED = "DELIVERED", "Delivered"

    bmw_id = models.CharField(
        "BMW ID",
        max_length=32,
        unique=True
    )

    model = models.CharField(
        max_length=120
    )

    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100),
        ],
    )

    variant = models.CharField(
        max_length=120,
        blank=True
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    image = models.ImageField(
        upload_to="vehicles/",
        blank=True,
        null=True
    )

    customer_name = models.CharField(
        max_length=120,
        blank=True
    )

    registration_number = models.CharField(
        max_length=32,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ("-created_at", "-pk")
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return f"{self.bmw_id} — {self.model} ({self.year})"


# ==========================================================
# IMAGE REPLACED OR CLEARED DURING EDIT
# ==========================================================

@receiver(pre_save, sender=Vehicle)
def delete_old_vehicle_image(sender, instance, **kwargs):

    # New vehicle — nothing to remove
    if not instance.pk:
        return

    try:
        old_vehicle = Vehicle.objects.get(pk=instance.pk)
    except Vehicle.DoesNotExist:
        return

    old_image = old_vehicle.image
    new_image = instance.image

    old_name = old_image.name if old_image else ""
    new_name = new_image.name if new_image else ""

    # Image was replaced OR cleared
    if old_name and old_name != new_name:
        old_image.delete(save=False)


# ==========================================================
# VEHICLE DELETED → DELETE ITS IMAGE
# ==========================================================

@receiver(post_delete, sender=Vehicle)
def delete_vehicle_image(sender, instance, **kwargs):

    if instance.image:
        instance.image.delete(save=False)