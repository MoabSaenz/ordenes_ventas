from django.core.management.base import BaseCommand
from django.utils import timezone
from ordenes.models import Orden
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Popula la base de datos con 50 órdenes de prueba'

    def handle(self, *args, **options):
        usuarios = ['alice', 'bob', 'carol', 'david', 'eva']
        estatus_choices = ['pendiente', 'proceso', 'completo']
        base_date = timezone.now()
        created = 0
        for i in range(50):
            usuario = random.choice(usuarios)
            numero_orden = f'TEST-{random.randint(1000,9999)}-{i}'
            days_back = random.randint(0, 365)
            fecha = (base_date - timedelta(days=days_back)).date()
            fecha_factura = fecha if random.random() < 0.6 else None
            estatus = random.choice(estatus_choices)
            factura = random.randint(10000, 99999) if random.random() < 0.5 else None
            descripcion = f'Orden de prueba {i} para {usuario}'
            Orden.objects.create(
                usuario=usuario,
                numero_orden=numero_orden,
                fecha=fecha,
                fecha_factura=fecha_factura,
                descripcion=descripcion,
                estatus=estatus,
                factura=factura,
                comentarios='Generada por populate_test_orders'
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Creadas {created} órdenes de prueba.'))
