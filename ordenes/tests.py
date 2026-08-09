from datetime import date

from django.test import TestCase

from .models import Orden


class OrdenModelTests(TestCase):
    def test_fecha_factura_can_be_saved(self):
        orden = Orden.objects.create(
            usuario='test-user',
            numero_orden='ORD-001',
            fecha_factura=date(2026, 8, 6),
        )

        self.assertEqual(orden.fecha_factura, date(2026, 8, 6))
