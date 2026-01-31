import django_filters
from .models import HouseModel

class HouseFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter( field_name="house_price", lookup_expr="gte")
    max_price = django_filters.NumberFilter( field_name="house_price", lookup_expr="lte") 
    class Meta:
        model = HouseModel
        fields = ["house_price",]