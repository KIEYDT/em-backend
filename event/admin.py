from django.contrib import admin

from .models import Event, Location, InviteLink, GuestEvent
from ticket.models import Ticket

class InviteLinkInline(admin.TabularInline) :
    model = InviteLink
    extra = 0
    can_delete = True
    readonly_fields = ('get_shortened_link_display',)
    

    def get_shortened_link_display(self, obj) :
        if obj.pk :
            return obj.get_shortened_link()
        return '-'
    
class GuestEventInline(admin.TabularInline) :
    model = GuestEvent
    extra = 0
    can_delete = True
    readonly_fields = ('ticket', 'user', 'event', 'status', 'was_created')


class EventAdmin(admin.ModelAdmin) :
    list_display = ['title', 'organizer', 'start', 'end']
    inlines = [InviteLinkInline, GuestEventInline]



admin.site.register(Event, EventAdmin)
admin.site.register(Location)
admin.site.register(InviteLink)