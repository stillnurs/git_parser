from django.urls import path

from . import views


urlpatterns = [
    path('', views.CommitsView.as_view()),
]
