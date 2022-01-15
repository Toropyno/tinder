from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('clients/create/',
         views.CreateUserView.as_view(),
         name='client-create'),
    path('clients/<int:id>/match/',
         views.client_match,
         name='client-match'),
    path('',
         include('rest_framework.urls')),
])
