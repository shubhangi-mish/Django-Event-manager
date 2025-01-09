from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/event/<int:event_id>/comments/', consumers.EventCommentConsumer.as_asgi()),
]
