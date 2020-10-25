from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('<int:pk>/', views.Counter.as_view(), name='counter'),
]
