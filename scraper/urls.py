from django.conf.urls import url
from django.urls import path

from . import views
from .views import *


urlpatterns = [
    path('', views.CommitsView.as_view()),
]
