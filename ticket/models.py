from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Ticket(models.Model) :
    class Status(models.TextChoices) :
        AVA = "available", _("Available")
        EXP = "expired", _("Expired")
        STUB = "stub", _("Stub")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ticket",
        blank=True,
        null=True,
    )
    # qr = models.ImageField() # FIXME: implement after image implementation
    was_created = models.DateTimeField(
        auto_created=True,
        null=True,
        editable=False,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
    )
    status = models.CharField(
        max_length=12,
        choices=Status,
        blank=True,
        null=True,
        default=Status.AVA,
    )

    def __str__(self):
        return f'{self.pk}'