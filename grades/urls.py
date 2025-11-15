from django.urls import path
from . import views

app_name = 'grades'

urlpatterns = [
    path('edit/<int:grade_id>/', views.edit_grade, name='edit_grade'),
]
