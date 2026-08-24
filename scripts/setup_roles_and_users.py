import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so 'sistema' package is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
django.setup()

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from ordenes.models import Orden


def setup_roles():
    orden_ct = ContentType.objects.get_for_model(Orden)
    admin_group, _ = Group.objects.get_or_create(name='admin')
    capturista_group, _ = Group.objects.get_or_create(name='capturista')
    lector_group, _ = Group.objects.get_or_create(name='lector')

    perms = {
        'admin': ['view_orden', 'add_orden', 'change_orden', 'delete_orden'],
        'capturista': ['view_orden', 'add_orden', 'change_orden'],
        'lector': ['view_orden'],
    }

    for name, codenames in perms.items():
        group = {'admin': admin_group, 'capturista': capturista_group, 'lector': lector_group}[name]
        group.permissions.clear()
        for codename in codenames:
            try:
                perm = Permission.objects.get(content_type=orden_ct, codename=codename)
            except Permission.DoesNotExist:
                print(f'Permission {codename} not found for ordenes; skipping')
                continue
            group.permissions.add(perm)

    print('Groups and permissions ensured.')


def create_capturista_user(username='capturista1', password='Testpass123'):
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.save()
        print(f'Created user {username} with password {password}')
    else:
        print(f'User {username} already exists')
    capturista = Group.objects.get(name='capturista')
    user.groups.add(capturista)
    user.save()
    print(f'Added {username} to group capturista')
    # show effective perms
    perms = sorted(user.get_all_permissions())
    print('Effective permissions for', username, ':', perms)


if __name__ == '__main__':
    setup_roles()
    create_capturista_user()
