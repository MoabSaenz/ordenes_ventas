from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('editar/<int:orden_id>/', views.editar_orden, name='editar_orden'),
    path('eliminar/<int:orden_id>/', views.eliminar_orden, name='eliminar_orden'),
]
