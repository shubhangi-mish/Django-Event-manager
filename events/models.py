from django.contrib.auth.models import User
from django.db import models
#from django.contrib.gis.db import models as geomodels
from django.utils import timezone

# Extending the default User model using a OneToOneField
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username


# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Event Model
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
  #  location = geomodels.PointField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_public = models.BooleanField(default=True)
    host = models.ForeignKey(User, related_name='events_hosted', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='events_participated', through='EventParticipant')
    tags = models.ManyToManyField(Tag, related_name='events')
    
    def __str__(self):
        return self.title

    # Custom Manager to filter events by location and time
    class EventManager(models.Manager):
       # def get_by_location(self, point, distance):
        #    return self.filter(location__distance_lte=(point, distance))

        def get_by_date_range(self, start_date, end_date):
            return self.filter(start_time__gte=start_date, end_time__lte=end_date)

    objects = EventManager()


# EventParticipant Model (to store many-to-many relationships for participants)
class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invited = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} in {self.event.title}'


# Comment Model
class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.event.title}'
