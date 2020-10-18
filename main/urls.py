from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('registrar/', views.Registration.as_view(), name='registrar'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('user/<int:pk>', views.EditUser.as_view(), name='edit_user'),
    path('news/<int:pk>', views.EditNews.as_view(), name='edit_news'),
    path('news/', views.AddNews.as_view(), name='add_news'),
]