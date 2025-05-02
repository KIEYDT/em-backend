from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User

from .models import Organizer, Guest


class OrganizerAdmin(admin.ModelAdmin) :
    list_display = ['name', 'user__username']


admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Guest)

admin.site.unregister(Group)