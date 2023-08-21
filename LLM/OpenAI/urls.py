from django.urls import path
from . import views

urlpatterns = [
    path('OpenAI/', views.home, name='OpenAI'),
]