from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("dashboard/", views.inicio, name="dashboard"),
    path("usuarios/", views.gestion_usuarios, name="gestion_usuarios"),
    path("usuarios/editar/<int:user_id>/", views.editar_usuario, name="editar_usuario"),
    path("usuarios/eliminar/<int:user_id>/", views.eliminar_usuario, name="eliminar_usuario"),
    path("actividad/", views.actividad, name="actividad"),
    path("reportes/", views.reportes, name="reportes"),
]