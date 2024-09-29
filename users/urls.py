from django.urls import path
from .views import EditUser

app_name = "users"

urlpatterns = [
    path('editar/<int:pk>',EditUser.as_view(),name='editar-user'),
  
]
