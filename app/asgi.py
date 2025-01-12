# app/asgi.py  
  
import os  
from channels.routing import ProtocolTypeRouter, URLRouter  
from django.core.asgi import get_asgi_application  
from channels.auth import AuthMiddlewareStack  
from app.routing import websocket_urlpatterns  # Ensure correct path to routing file  
  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')  
  
application = ProtocolTypeRouter({  
    "http": get_asgi_application(),  
    "websocket": AuthMiddlewareStack(  
        URLRouter(  
            websocket_urlpatterns  
        )  
    ),  
})  