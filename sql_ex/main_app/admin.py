from django.contrib import admin
from .models import Venue
from .models import ClubMember
from .models import Event

# Register your models here.
admin.site.register(Venue)
admin.site.register(ClubMember)
admin.site.register(Event)
