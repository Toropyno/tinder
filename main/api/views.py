from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import UserSerializer

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
