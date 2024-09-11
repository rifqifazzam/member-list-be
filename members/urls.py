from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.list_members, name='list_members'), 
    path('members/<int:pk>/', views.get_member, name='get_member'),
    path('members/create/', views.create_member, name='create_member'), 
    path('members/<int:pk>/update/', views.update_member, name='update_member'), 
    path('members/<int:pk>/delete/', views.delete_member, name='delete_member'),  
]
