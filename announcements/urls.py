from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    path('create/', views.create_announcement, name='create_announcement'),
    path('my-announcements/', views.my_announcements, name='my_announcements'),
    path('edit/<int:announcement_id>/', views.edit_announcement, name='edit_announcement'),
    path('delete/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),
]
