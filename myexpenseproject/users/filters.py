from csv import field_size_limit
from pydoc import describe
import django_filters
from django_filters import DateRangeFilter
from .models import Item

class ItemFilter(django_filters.FilterSet):
    time_it_was_bought = DateRangeFilter()
    class Meta:
        model = Item
        fields = ['name','time_it_was_bought', 'description']
    