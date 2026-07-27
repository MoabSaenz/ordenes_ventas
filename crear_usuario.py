#!/usr/bin/env python
"""
Script para crear un usuario de prueba en Django
Uso: python manage.py shell < crear_usuario.py
O también: python crear_usuario.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
django.setup()

from django.contrib.auth.models import User

# Datos del usuario de prueba
USERNAME = "admin"
PASSWORD = "admin123"
EMAIL = "admin@test.com"

try:
    # Verificar si el usuario ya existe
    if User.objects.filter(username=USERNAME).exists():
        print(f"✓ El usuario '{USERNAME}' ya existe.")
        user = User.objects.get(username=USERNAME)
        print(f"  Email: {user.email}")
        print(f"  Es superuser: {user.is_superuser}")
    else:
        # Crear superuser
        user = User.objects.create_superuser(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD
        )
        print(f"✓ Usuario creado exitosamente:")
        print(f"  Username: {USERNAME}")
        print(f"  Email: {EMAIL}")
        print(f"  Password: {PASSWORD}")
        print(f"\n  ⚠ Guarda estas credenciales en un lugar seguro")

except Exception as e:
    print(f"✗ Error al crear el usuario: {e}")
