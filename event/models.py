from hashids import Hashids

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User

from users.models import Organizer, Guest
from ticket.models import Ticket


class Location(models.Model) :
    location = models.TextField()
    lat = models.FloatField()
    long = models.FloatField()

    def __str__(self) :
        return self.location


# FIXME: calendar, location field
class Event(models.Model) :
    class Theme(models.TextChoices) :
        CLASSIC = "classic", _("Classic")

    location = models.ForeignKey(
        Location,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    organizer = models.ForeignKey(
        Organizer,
        on_delete=models.PROTECT,
    )
    title = models.CharField(
        max_length=255,
    )
    start = models.DateTimeField(
        blank=True,
        null=True,
    )
    end = models.DateTimeField(
        blank=True,
        null=True,
    )
    description = models.TextField(
        max_length=255,
        blank=True,
        null=True,
    )
    price = models.PositiveIntegerField(
        default=0,
    )
    approval = models.BooleanField(
        default=False,
    )
    capacity = models.IntegerField(
        default=-1,
    )
    theme = models.CharField(
        max_length=10,
        choices=Theme,
        default=Theme.CLASSIC,
    )
    theme_shuffle = models.BooleanField(
        default=False,
    )
    is_available = models.BooleanField(
        default=False,
    )
    was_created = models.DateTimeField(
        auto_created=True,
        null=True,
        editable=True,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
    )
    image_url = models.URLField(
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return self.title


class Question(models.Model) :
    QUESTION_TYPE = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('choice', 'Multiple Choice'),
        ('checkbox', 'Checkbox'),
        ('date', 'Date'),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='questions',
    )
    text = models.CharField(
        max_length=255,
    )
    question_type = models.CharField(
        max_length=32,
        choices=QUESTION_TYPE,
        default='text',
    )
    required = models.BooleanField(
        default=True,
    )

    def __str__(self) :
        return f"{self.text} ({self.event.title})"
    

class Answer(models.Model) :
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    guest = models.ForeignKey(
        Guest,
        on_delete=models.CASCADE,
    )
    answer_text = models.TextField(
        blank=True,
        null=True,
    )
    answer_choice = models.JSONField(
        blank=True,
        null=True,
    )

    def __str__(self) :
        return f"{self.guest.user.username or self.guest.user.email}: {self.answer_text}"


class InviteLink(models.Model) :
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='invite_link',
    )
    
    def get_hashed_id(self) :
        if self.id is None :
            return None
        return Hashids(salt="invite_link_salt", min_length=8).encode(self.id)

    def get_shortened_link(self, request=None) :
        hashed_id = self.get_hashed_id()
        if hashed_id is None :
            return None
        if request :
            base_url = request.build_absolute_uri('/')
        else :
            base_url = "http://localhost:8000/"

        return f"http://localhost:5173/{hashed_id}"

    def __str__(self) :
        return f"invite link for {self.event.title}"
    

class GuestEvent(models.Model) :
    class Status(models.TextChoices) :
        CHECKED_IN = "checked_in", _("Checked In")
        ON_GOING = "ongoing", _("Ongoing")
        COMPLETED = "completed", _("Completed")
        ABORTED = "aborted", _("Aborted")
        CANCELLED = "cancelled", _("Cancelled")

    class ApprovalStatus(models.TextChoices) :
        PENDING = "pending", _("Pending")
        APPROVED = "approved", _("Approved")
        REJECTED = "rejected", _("Rejected")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='guest_events',
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='guest_events',
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='guest_events',
    )
    was_created = models.DateTimeField(
        auto_now_add=True,
    )
    approval_status = models.TextField(
        choices=ApprovalStatus,
        default=ApprovalStatus.PENDING,
    )
    status = models.TextField(
        choices=Status,
        default=Status.ON_GOING,
    )

    def __str__(self) :
        return f'{self.event.title} - {self.user.username or self.user.email}'