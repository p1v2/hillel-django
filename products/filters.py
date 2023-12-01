import django_filters


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="iexact")
    price = django_filters.NumberFilter(lookup_expr="iexact")
    price__gt = django_filters.NumberFilter(
        field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(
        field_name="price", lookup_expr="lt")

    description = django_filters.CharFilter(lookup_expr="icontains")

    # Filter by foreign key
    category = django_filters.CharFilter(
        field_name="category__name", lookup_expr="iexact"
    )

    q = django_filters.CharFilter(method="filter_by_q", label="Search")

    def filter_by_q(self, queryset, name, value):
        return (
            queryset.filter(name__icontains=value)
            | queryset.filter(description__icontains=value)
            | queryset.filter(category__name__icontains=value)
        )
