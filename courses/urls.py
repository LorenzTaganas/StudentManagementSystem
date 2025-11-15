from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('subject/<int:subject_id>/students/', views.subject_students, name='subject_students'),
    path('subjects/', views.subject_list, name='subject_list'),
]
