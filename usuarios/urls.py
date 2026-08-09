from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("dashboard/", views.inicio, name="dashboard"),
    path("usuarios/", views.gestion_usuarios, name="gestion_usuarios"),
    path("reportes/", views.reportes, name="reportes"),
]