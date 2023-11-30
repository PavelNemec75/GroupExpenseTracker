from django.contrib import admin
from .models import Event, Participant, EventParticipant, EventExpenseItem, EventExpenseGroup

admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(EventParticipant)
admin.site.register(EventExpenseItem)
admin.site.register(EventExpenseGroup)
