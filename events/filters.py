from django_filters import rest_framework as filters
from .models import Event

class EventFilter(filters.FilterSet):
    start_time = filters.DateTimeFilter(field_name='start_time', lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name='end_time', lookup_expr='lte')
    tags = filters.CharFilter(field_name='tags__name', lookup_expr='icontains')
   # location = filters.CharFilter(field_name='location', lookup_expr='icontains')
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['start_time', 'end_time', 'tags', 'search']
