from django.contrib import admin
from .models import Profile, Tag, Event, Comment

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Event)
admin.site.register(Comment)