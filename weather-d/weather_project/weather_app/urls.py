from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Ensure this path is correct
]
