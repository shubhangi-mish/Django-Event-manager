# app/urls.py  
  
from django.contrib import admin  
from django.urls import path, include  
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  
from django.shortcuts import redirect  
from rest_framework.routers import DefaultRouter  
from events.views import EventViewSet, CommentViewSet  # Import your viewsets  
  
# Create a router and register the viewsets  
router = DefaultRouter()  
router.register(r'events', EventViewSet)  
router.register(r'comments', CommentViewSet)  
  
urlpatterns = [  
    path('admin/', admin.site.urls),  
    # JWT Authentication URLs  
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    # API Endpoints  
    path('api/', include(router.urls)),  
    # Include the events app URLs  
    path('events/', include('events.urls')),  
    # Redirect the root URL to /events/  
    path('', lambda request: redirect('/events/')),   
]  