# events/urls.py  
  
from django.urls import path  
from . import views  
from django.contrib.auth.views import LogoutView  
  
urlpatterns = [  
    # Regular views for pages  
    path('', views.home, name='home'),  
    path('register/', views.register, name='register'),  
    path('profile/update/', views.update_profile, name='update_profile'),  
    path('login/', views.CustomLoginView.as_view(), name='login'),  
    path('logout/', LogoutView.as_view(), name='logout'),  
    path('profile/', views.user_profile, name='user_profile'),  
    path('profile/success/', views.profile_success, name='profile_success'),  
    # No API routes here  
]  