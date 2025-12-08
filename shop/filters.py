import django_filters 
from .models import Product

class ProductFilter(django_filters.FilterSet):
    """Advaced filtering for product model"""
    # Price range Filters
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    # Text filters
    name = django_filters.CharFilter(lookup_expr='icontains')
    material = django_filters.CharFilter(lookup_expr='icontains')
    color = django_filters.CharFilter(lookup_expr='icontains')

    # Boolean filters
    is_featured = django_filters.BooleanFilter()
    in_stock = django_filters.CharFilter(method='filter_in_stock')

    # Category filter
    category = django_filters.NumberFilter(field_name='category__id')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = [
            'category', 'is_featured', 'material',
            'color', 'min_price', 'max_price'
        ]

    def filter_in_stock(self, queryset, name, value):
        """Filter products that are in stock"""
        if value:
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock=0)