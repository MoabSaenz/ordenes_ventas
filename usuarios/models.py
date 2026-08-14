from django.contrib.auth.models import User
from django.db import models


class Actividad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actividades')
    accion = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    def __str__(self):
        return f'{self.usuario.username} - {self.accion}'
