from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from main import services

User = get_user_model()


class UserFilter(filters.FilterSet):
    """Фильтрация пользователей"""
    first_name = filters.CharFilter(lookup_expr='iexact')
    last_name = filters.CharFilter(lookup_expr='iexact')
    distance = filters.NumberFilter(label='distance', method='filter_distance')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'distance']

    def filter_distance(self, queryset, name, value):
        """
        Фильтрация по полю distance
        """
        request_user = self.request.user
        distance = int(value)

        if distance <= 0:
            raise ValidationError(
                {'distance': ['Значение должно быть положительным']}
            )
        if not request_user.has_coords:
            raise ValidationError(
                {'distance': ['Необходимо заполнить поля longitude и latitude']}
            )

        user_lat = float(request_user.latitude)
        user_lon = float(request_user.longitude)

        # чтобы не считать расстояние до каждого пользователя,
        # предварительно отсеем тех, кто находится "слишком" далеко;
        # для этого определим в каком диапазоне координат должны находиться пользователи
        # относительно текущего пользователя, учитывая значение distance
        lon_delta = services.get_longitude_delta(distance)  # отклонение долготы в градусах
        lat_delta = services.get_latitude_delta(distance, user_lat)  # отклонение широты в градусах
        filtered_users = queryset.filter(
            longitude__range=(user_lon - lon_delta, user_lon + lon_delta),
            latitude__range=(user_lat - lat_delta, user_lat + lat_delta)
        )

        # до оставшихся пользователей считаем расстояние и выбираем тех,
        # кто находится в пределах distance
        filtered_users = list(
            user.id for user in filtered_users if services.get_distance_between_clients(request_user, user) <= distance)
        return User.objects.filter(id__in=filtered_users)
