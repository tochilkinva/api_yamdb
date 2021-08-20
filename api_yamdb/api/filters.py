from django_filters.rest_framework import CharFilter, FilterSet

from media_content.models import Title


class FilterTitle(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="contains")
    category = CharFilter(field_name="category__slug")
    genre = CharFilter(field_name="genre__slug")

    class Meta:
        fields = "__all__"
        model = Title
