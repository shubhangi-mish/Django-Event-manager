from django.urls import re_path
from events.consumers import EventCommentConsumer

websocket_urlpatterns = [
    re_path(r'ws/events/(?P<event_id>\d+)/$', EventCommentConsumer.as_asgi()),
]
