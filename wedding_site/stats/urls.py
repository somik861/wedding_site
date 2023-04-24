from django.urls import path, register_converter

from . import views

class BoolConverter:
    regex = 'false|true'
    def to_python(self, value):
        return value == 'true'
    
    def to_url(self, value):
        return 'true' if value else 'false'
    
register_converter(BoolConverter, 'bool')

urlpatterns = [
    path('', views.login, name='login'),
    path('main_view', views.main_view, name='main_view'),
    path('respondent/<int:resp_id>', views.respondent_view, name='respondent_view'),
    path('respondent/<int:resp_id>/<bool:verbose>', views.respondent_view, name='respondent_view'),
    path('survey/<int:survey_id>', views.survey_view, name='survey_view'),
]