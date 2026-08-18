from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ver/<int:orden_id>/', views.ver_orden, name='ver_orden'),
    path('editar/<int:orden_id>/', views.editar_orden, name='editar_orden'),
    path('editar_modal/<int:orden_id>/', views.editar_orden_modal, name='editar_orden_modal'),
    path('eliminar/<int:orden_id>/', views.eliminar_orden, name='eliminar_orden'),
]
