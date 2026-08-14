from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from ordenes.models import Orden


class Command(BaseCommand):
    help = 'Crea los grupos admin, capturista y lector con permisos básicos para órdenes.'

    def handle(self, *args, **options):
        orden_content_type = ContentType.objects.get_for_model(Orden)
        user_content_type = ContentType.objects.get_for_model(User)

        admin_group, _ = Group.objects.get_or_create(name='admin')
        capturista_group, _ = Group.objects.get_or_create(name='capturista')
        lector_group, _ = Group.objects.get_or_create(name='lector')

        permissions = {
            'admin': [
                'view_orden',
                'add_orden',
                'change_orden',
                'delete_orden',
                'can_create_order',
                'can_edit_order',
                'can_delete_order',
                'can_view_all_orders',
                'change_user',
            ],
            'capturista': [
                'view_orden',
                'add_orden',
                'can_create_order',
                'can_edit_order',
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
                if codename == 'change_user':
                    permission = Permission.objects.get(content_type=user_content_type, codename=codename)
                else:
                    permission = Permission.objects.get(content_type=orden_content_type, codename=codename)
                group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Grupos y permisos creados correctamente.'))