from django.db import models
from .mixins import AuditMixin


class Orden(AuditMixin):
    usuario = models.CharField(max_length=100)
    numero_orden = models.CharField(max_length=50)
    fecha = models.DateField(blank=True, null=True)
    fecha_factura = models.DateField(blank=True, null=True)
    descripcion = models.TextField(blank=True)
    estatus = models.CharField(max_length=20, default='pendiente')
    fecha_termino = models.DateField(blank=True, null=True)
    factura = models.IntegerField(blank=True, null=True)
    comentarios = models.TextField(blank=True)
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)


class ActivityLog(models.Model):
    """Simple activity log for audit purposes."""
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=20)
    model = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.numero_orden} - {self.usuario}"

    class Meta:
        permissions = [
            ("can_create_order", "Puede crear órdenes"),
            ("can_edit_order", "Puede editar órdenes"),
            ("can_delete_order", "Puede eliminar órdenes"),
            ("can_view_all_orders", "Puede ver todas las órdenes"),
        ]
