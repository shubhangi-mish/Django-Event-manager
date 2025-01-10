from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User


# Extending the default User model with additional fields like bio and profile picture
class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username


# Tag Model for categorizing events
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Event Model with various fields, relationships, and custom manager
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_public = models.BooleanField(default=True)

    # Relationships
    host = models.ForeignKey('auth.User', related_name='hosted_events', on_delete=models.CASCADE)
    participants = models.ManyToManyField('auth.User', related_name='participated_events')
    tags = models.ManyToManyField(Tag, related_name='events')

    def __str__(self):
        return self.title

    # Custom manager to fetch active events
    class EventManager(models.Manager):
        def active_events(self):
            return self.filter(is_public=True, start_time__gte=models.functions.Now())

    # Assigning the custom manager
    objects = EventManager()

    # Custom QuerySet method to get upcoming events for a user
    @staticmethod
    def get_upcoming_events_for_user(user):
        return Event.objects.filter(participants=user, start_time__gte=models.functions.Now())

class EventParticipant(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} in {self.event.name}'

# Comment Model for users to leave comments on events
class Comment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.event.title}"


# Signal to notify participants when a new event is created
@receiver(post_save, sender=Event)
def notify_participants(sender, instance, created, **kwargs):
    if created:
        for participant in instance.participants.all():
            send_mail(
                subject=f"New Event: {instance.title}",
                message=f"Hey {participant.username}, a new event '{instance.title}' has been created!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[participant.email]
            )
