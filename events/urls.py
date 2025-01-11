from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, CommentViewSet
from django.contrib.auth.views import LogoutView

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    # Regular views for pages
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/success/', views.profile_success, name='profile_success'),

    # JWT Authentication View
    path('token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # API routes for events and comments
    path('api/', include(router.urls)),
]
