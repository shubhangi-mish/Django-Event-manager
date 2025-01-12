from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Event, Comment, Profile
from .serializers import EventSerializer, CommentSerializer, EventDetailSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from rest_framework import serializers  
from .forms import ProfileUpdateForm


# Home view (Landing Page)
def home(request):
    return render(request, 'home.html')


# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# User Login View (Using Django's built-in view)
from django.contrib.auth.views import LoginView, LogoutView

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        # Redirect to the user's profile page after login
        return reverse('user_profile') 

def user_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)  # This form allows the user to update fields
        if form.is_valid():
            form.save()
            return redirect('profile_success')  # Redirect to success page after successful update
    else:
        form = UserChangeForm(instance=request.user)  # Pre-populate the form with the user's current data
    
    return render(request, 'profile/user_profile.html', {'form': form})

def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Replace 'profile' with your desired redirect URL
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'user_profile.html', {'form': form})


# Profile Success View (After profile creation)
def profile_success(request):
    return render(request, 'profile/profile_success.html')


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
    queryset = Event.objects.all().order_by('start_time')  
    serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsOwner]
        return [permissions.IsAuthenticated()]

from rest_framework.pagination import CursorPagination  

class CommentCursorPagination(CursorPagination):  
    page_size = 10  # Adjust as needed  
    ordering = '-created_at'  # Use the correct field name  

# Comment ViewSet (CRUD operations)
class CommentViewSet(viewsets.ModelViewSet):  
    queryset = Comment.objects.all()  
    serializer_class = CommentSerializer  
    permission_classes = [IsAuthenticated]  
    pagination_class = CommentCursorPagination   
  
    def perform_create(self, serializer):  
        event_id = self.request.data.get('event_id')  
        if not event_id:  
            raise serializers.ValidationError({'event_id': 'This field is required.'})  
        try:  
            event = Event.objects.get(id=event_id)  
        except Event.DoesNotExist:  
            raise serializers.ValidationError({'event_id': 'Invalid event ID.'})  
