from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from ordenes.models import Orden


class Command(BaseCommand):
    help = 'Crea los grupos admin, capturista y lector con permisos básicos para órdenes.'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Orden)

        admin_group, _ = Group.objects.get_or_create(name='admin')
        capturista_group, _ = Group.objects.get_or_create(name='capturista')
        lector_group, _ = Group.objects.get_or_create(name='lector')

        permissions = {
            'admin': [
                'view_orden',
                'add_orden',
                'change_orden',
                'delete_orden',
            ],
            'capturista': [
                'view_orden',
                'add_orden',
            ],
            'lector': [
                'view_orden',
            ],
        }

        for group_name, perm_codenames in permissions.items():
            group = {
                'admin': admin_group,
                'capturista': capturista_group,
                'lector': lector_group,
            }[group_name]
            group.permissions.clear()
            for codename in perm_codenames:
                permission = Permission.objects.get(content_type=content_type, codename=codename)
                group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Grupos y permisos creados correctamente.'))