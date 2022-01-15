from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import UserSerializer
from .. import services

User = get_user_model()


@api_view(['GET'])
def api_root(request, format=None):
    """
    Корень API
    """
    return Response({
        'client-create': reverse('client-create', request=request, format=format),
    })


class CreateUserView(CreateAPIView):
    """
    Представление для создания пользователей
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(['POST'])
def client_match(request, id):
    """
    Оценивает пользователя

    Пользователь с ID равным аргументу id добавляется в
    симпатии (поле likes) пользователя request.user

    В случае взаимной симпатии, оповещает пользователей и
    возвращает почту оцененного пользователя
    """
    request_user = User.objects.get(id=request.user.id)
    user = User.objects.get(id=id)
    request_user.likes.add(user)

    if services.check_match(request_user, user):
        data = {
            'user_email': user.email
        }
        services.report_mutual_sympathy(request_user, user)
        return Response(data)
    return Response()
