import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Comment
from .serializers import CommentSerializer

class EventCommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.room_name = f"event_{self.event_id}"
        self.room_group_name = f"event_{self.event_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        comment_text = text_data_json['comment']

        # Create new comment and save to database
        comment = Comment.objects.create(event_id=self.event_id, user=self.scope['user'], text=comment_text)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'comment_message',
                'comment': comment_text,
            }
        )

    async def comment_message(self, event):
        # Send comment to WebSocket
        await self.send(text_data=json.dumps({
            'comment': event['comment'],
        }))
