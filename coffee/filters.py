import django_filters
from .models import *


class ProductsFilter(django_filters.FilterSet):
    class Meta:
        model = Products
        fields = ['name']
