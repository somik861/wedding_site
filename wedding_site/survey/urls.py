from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:survey_id>', views.survey),
    path('rsvp', views.rsvp),
    path('rvsp/<str:name>', views.rvsp_quest)
]
