from django.contrib import admin
from .models import RecordLabel
from .models import Musician
from .models import Album

# Register your models here.
admin.site.register(RecordLabel)
admin.site.register(Musician)
admin.site.register(Album)
