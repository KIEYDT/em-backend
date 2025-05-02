import os

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.static import static as django_static
from django.urls import path, include


urlpatterns = [
    path('', include('users.urls')),
    path('', include('event.urls')),
]

