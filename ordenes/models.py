from django.db import models


class Orden(models.Model):
    usuario = models.CharField(max_length=100)
    numero_orden = models.CharField(max_length=50)
    fecha = models.DateField(blank=True, null=True)
    descripcion = models.TextField(blank=True)
    estatus = models.CharField(max_length=20, default='pendiente')
    fecha_termino = models.DateField(blank=True, null=True)
    factura = models.IntegerField(blank=True, null=True)
    comentarios = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.numero_orden} - {self.usuario}"
