from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # Correct import
from events import urls as event_urls
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from app.routing import websocket_urlpatterns  # Ensure correct path to routing file
from django.core.wsgi import get_wsgi_application
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Correct reference
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Correct reference
    path('events/', include(event_urls)),
    path('', lambda request: redirect('/events/')), 
]

# WebSocket URL routing
application = ProtocolTypeRouter({
    "http": get_wsgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Ensure this matches the correct path
        )
    ),
})
