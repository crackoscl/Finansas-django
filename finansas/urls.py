from django.urls import path
from .views import ListarMovimiento,CrearMovimiento,UpdateMovimiento,DeleteMovimiento,get_category

app_name = "finansas"

urlpatterns = [
    path('movimientos/crear',CrearMovimiento.as_view(),name='crear-mov'),
    path('movimientos/listar', ListarMovimiento.as_view(),name='listar_mov'),
    path('movimientos/editar/<int:pk>',UpdateMovimiento.as_view(),name='actualizar-mov'),
    path('movimientos/borrar/<int:pk>',DeleteMovimiento.as_view(),name='borrar-mov'),
    path('get-categories/', get_category, name='get-categories'),
]
