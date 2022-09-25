from django.urls import path
from .views import EmpleadoViews, EmpresaViews, UsuarioViews, UsuarioEmpleadoViews, MovimientosViews
from . import views

urlpatterns=[
    path('login/',views.loginusuario, name="Ingreso usuario"),
    path('empresa/', EmpresaViews.as_view(), name="Visualizar"),
    path('empresa/<str:nomb>', EmpresaViews.as_view(), name="Actualizar"),
    path('empleado/', EmpleadoViews.as_view(), name="Visualizar"),
    path('empleado/<int:cc>', EmpleadoViews.as_view(), name="Actualizar"),
    path('usuario/', UsuarioViews.as_view(), name="Visualizar"),
    path('usuario/<int:cc>', UsuarioEmpleadoViews.as_view(), name="Actualizar Usuario"),
    path('usuario/<str:user>', UsuarioViews.as_view(), name="Actualizar"),
    path('movimiento/', MovimientosViews.as_view(), name="Visualizar"),
    path('movimiento/<str:nomb>', MovimientosViews.as_view(), name="Eliminar")
]