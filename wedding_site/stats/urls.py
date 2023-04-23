from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('main_view', views.main_view, name='main_view')
]