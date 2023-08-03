from django.db import models
from django.contrib.auth.models import User


class Asset(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('two wheeler', 'Two Wheeler'),
        ('three wheeler', 'Three Wheeler'),
        ('four wheeler', 'Four Wheeler'),
        ('heavy vehicle', 'Heavy Vehicle')
    ]
    vehicle_type = models.CharField(
        max_length=20, choices=VEHICLE_TYPE_CHOICES, null=True, blank=True)
    vehicle_number = models.CharField(max_length=20, null=True, blank=True)
    lat = models.CharField(max_length=20, null=True, blank=True)
    long = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    user_photo = models.ImageField(
        upload_to='vehicle_photo/', null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.vehicle_number


class Alert(models.Model):
    alert_type = models.CharField(max_length=50, null=True, blank=True)
    value = models.CharField(max_length=50, null=True, blank=True)
    alert_condition = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ManyToManyField(Asset)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.alert_type


class Rule(models.Model):
    RULE_CHOICES = (
        ('temperature', 'Temperature'),
        ('speed', 'Speed'),
        ('fuel', 'Fuel')
    )
    condition = models.CharField(choices=RULE_CHOICES, max_length=50, blank=True, null=True)
    value = models.CharField(max_length=50, blank=True, null=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
