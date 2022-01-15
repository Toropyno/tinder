from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

User = get_user_model()


class UserFilter(filters.FilterSet):
    """Фильтрация пользователей"""
    first_name = filters.CharFilter(lookup_expr='iexact')
    last_name = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender']
