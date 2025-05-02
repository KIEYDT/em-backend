from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, User




class Organizer(models.Model) :
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
    )
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )
    bio = models.TextField(
        blank=True,
        null=True,
    )
    attendance = models.IntegerField(
        default=0,
    )
    events = models.IntegerField(
        default=0,
    )

    def __str__(self):
        return self.user.username


class Guest(models.Model) :
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
    )
    phone_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    company = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    job_title = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username

    