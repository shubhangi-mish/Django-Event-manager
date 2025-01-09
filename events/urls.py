from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, CommentViewSet, TokenObtainPairView

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
]
