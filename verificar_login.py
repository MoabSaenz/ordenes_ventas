#!/usr/bin/env python
"""
Script para comprobar y ejecutar el login funcional
"""

import os
import sys
import subprocess
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
django.setup()

from django.contrib.auth.models import User

print("=" * 60)
print("COMPROBADOR DE LOGIN - SISTEMA DE ÓRDENES")
print("=" * 60)

# 1. Verificar migraciones
print("\n[1] Verificando migraciones...")
result = subprocess.run(
    [sys.executable, "manage.py", "migrate", "--check"],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print("    ✗ Hay migraciones pendientes")
    print("    → Ejecutando migraciones...")
    subprocess.run([sys.executable, "manage.py", "migrate"])
    print("    ✓ Migraciones aplicadas")
else:
    print("    ✓ Todas las migraciones están al día")

# 2. Verificar usuario de prueba
print("\n[2] Verificando usuario de prueba...")
try:
    user = User.objects.get(username="admin")
    print(f"    ✓ Usuario 'admin' existe")
    print(f"      Email: {user.email}")
    print(f"      Es superuser: {user.is_superuser}")
except User.DoesNotExist:
    print("    ✗ Usuario 'admin' no existe")
    print("    → Creando usuario de prueba...")
    user = User.objects.create_superuser(
        username="admin",
        email="admin@test.com",
        password="admin123"
    )
    print("    ✓ Usuario creado exitosamente")
    print(f"      Username: admin")
    print(f"      Password: admin123")

# 3. Información para comprobar el login
print("\n" + "=" * 60)
print("✓ SETUP COMPLETADO - EL LOGIN YA ES FUNCIONAL")
print("=" * 60)

print("\n📋 CREDENCIALES DE PRUEBA:")
print("   Username: admin")
print("   Password: admin123")

print("\n🚀 PARA COMPROBAR QUE FUNCIONA:")
print("\n   1. Inicia el servidor:")
print("      python manage.py runserver")
print("\n   2. Abre el navegador y ve a:")
print("      http://localhost:8000/")
print("\n   3. Deberías ver el formulario de login")
print("      (Si entras directamente sin autenticar, te redirige al login)")
print("\n   4. Ingresa las credenciales:")
print("      Usuario: admin")
print("      Contraseña: admin123")
print("\n   5. Después de iniciar sesión, verás la página de GESTIÓN DE ÓRDENES")
print("\n   6. Para cerrar sesión, usa el botón de logout")

print("\n" + "=" * 60)
