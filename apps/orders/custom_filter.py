from django_filters.rest_framework import FilterSet, DateTimeFilter
from .models import Order


class OrderFilter(FilterSet):
    start_date = DateTimeFilter(field_name='date_created', lookup_expr='range')
    end_date = DateTimeFilter(field_name='date_created', lookup_expr='range')

    class Meta:
        model = Order
        fields = '__all__'