from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from django.utils import timezone

from ordenes.models import Orden


# Create your views here.
def iniciar_sesion(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "login.html")


def cerrar_sesion(request):
    logout(request)
    return redirect("login")


@login_required
def inicio(request):
    hoy = timezone.localdate()
    semana_inicio = hoy - timedelta(days=hoy.weekday())
    mes_inicio = hoy.replace(day=1)

    total_pendientes = Orden.objects.filter(estatus='pendiente').count()
    total_proceso = Orden.objects.filter(estatus='proceso').count()
    total_completas = Orden.objects.filter(estatus='completo').count()
    total_facturas = Orden.objects.filter(factura__isnull=False).count()
    ordenes_dia = Orden.objects.filter(creado_en__date=hoy).count()
    ordenes_semana = Orden.objects.filter(creado_en__date__gte=semana_inicio, creado_en__date__lte=hoy).count()
    ordenes_mes = Orden.objects.filter(creado_en__date__gte=mes_inicio, creado_en__date__lte=hoy).count()

    return render(request, "dashboard.html", {
        'fecha_actual': hoy,
        'total_pendientes': total_pendientes,
        'total_proceso': total_proceso,
        'total_completas': total_completas,
        'total_facturas': total_facturas,
        'ordenes_dia': ordenes_dia,
        'ordenes_semana': ordenes_semana,
        'ordenes_mes': ordenes_mes,
    })



@login_required
def gestion_usuarios(request):
    if not (request.user.is_superuser or request.user.has_perm('auth.change_user')):
        messages.error(request, 'No tienes permisos para administrar usuarios.')
        return redirect('dashboard')

    roles = ['admin', 'capturista', 'lector']
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role')

        if not username or not password or role not in roles:
            messages.error(request, 'Debes completar el usuario, contraseña y rol.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
        else:
            user = User.objects.create_user(username=username, password=password)
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
            messages.success(request, 'Usuario creado y rol asignado correctamente.')

    usuarios = User.objects.order_by('username').all()
    return render(request, 'gestion_usuarios.html', {
        'usuarios': usuarios,
        'roles': roles,
    })


@login_required
def reportes(request):
    hoy = timezone.localdate()
    semana_inicio = hoy - timedelta(days=hoy.weekday())
    mes_inicio = hoy.replace(day=1)

    pendientes = Orden.objects.filter(estatus='pendiente').count()
    en_proceso = Orden.objects.filter(estatus='proceso').count()
    completadas = Orden.objects.filter(estatus='completo').count()
    facturas = Orden.objects.filter(factura__isnull=False).count()
    ordenes_dia = Orden.objects.filter(creado_en__date=hoy).count()
    ordenes_semana = Orden.objects.filter(creado_en__date__gte=semana_inicio, creado_en__date__lte=hoy).count()
    ordenes_mes = Orden.objects.filter(creado_en__date__gte=mes_inicio, creado_en__date__lte=hoy).count()

    return render(request, 'reportes.html', {
        'fecha_actual': hoy,
        'pendientes': pendientes,
        'en_proceso': en_proceso,
        'completadas': completadas,
        'facturas': facturas,
        'ordenes_dia': ordenes_dia,
        'ordenes_semana': ordenes_semana,
        'ordenes_mes': ordenes_mes,
    })