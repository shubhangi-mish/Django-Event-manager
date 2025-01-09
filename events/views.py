from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point
from .models import Event, Comment, Profile
from .serializers import EventSerializer, CommentSerializer, EventDetailSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


import django 

# JWT Authentication View
class TokenObtainPairView(APIView):
    def post(self, request):
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)


# Event ViewSet (CRUD operations)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsOwner]
        return [permissions.IsAuthenticated()]


# Comment ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event = Event.objects.get(id=self.kwargs['event_id'])
        serializer.save(user=self.request.user, event=event)
