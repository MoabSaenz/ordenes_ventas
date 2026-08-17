from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission, User
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from ordenes.models import Orden
from .models import Actividad


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
            if role == 'admin':
                user.is_staff = True
                admin_permissions = Permission.objects.filter(
                    codename__in=[
                        'view_orden',
                        'add_orden',
                        'change_orden',
                        'delete_orden',
                        'can_create_order',
                        'can_edit_order',
                        'can_delete_order',
                        'can_view_all_orders',
                        'change_user',
                    ]
                )
                user.user_permissions.add(*admin_permissions)
                user.save()
            Actividad.objects.create(
                usuario=request.user,
                accion='Creación de usuario',
                descripcion=f'Usuario "{user.username}" creado con rol "{role}".',
            )
            messages.success(request, 'Usuario creado y rol asignado correctamente.')

    usuarios = User.objects.order_by('username').all()
    return render(request, 'gestion_usuarios.html', {
        'usuarios': usuarios,
        'roles': roles,
    })


@login_required
def editar_usuario(request, user_id):
    if not (request.user.is_superuser or request.user.has_perm('auth.change_user')):
        messages.error(request, 'No tienes permisos para editar usuarios.')
        return redirect('dashboard')

    usuario = get_object_or_404(User, pk=user_id)
    if usuario.is_superuser and not request.user.is_superuser:
        messages.error(request, 'No puedes editar un superusuario.')
        return redirect('gestion_usuarios')

    roles = ['admin', 'capturista', 'lector']
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        role = request.POST.get('role')

        if not username or role not in roles:
            messages.error(request, 'Debes completar el usuario y el rol.')
        elif User.objects.filter(username=username).exclude(pk=usuario.pk).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
        else:
            usuario.username = username
            usuario.groups.clear()
            group, _ = Group.objects.get_or_create(name=role)
            usuario.groups.add(group)

            if role == 'admin':
                usuario.is_staff = True
                admin_permissions = Permission.objects.filter(
                    codename__in=[
                        'view_orden',
                        'add_orden',
                        'change_orden',
                        'delete_orden',
                        'can_create_order',
                        'can_edit_order',
                        'can_delete_order',
                        'can_view_all_orders',
                        'change_user',
                    ]
                )
                usuario.user_permissions.add(*admin_permissions)
            else:
                usuario.is_staff = False
                usuario.user_permissions.remove(*Permission.objects.filter(
                    codename__in=[
                        'view_orden',
                        'add_orden',
                        'change_orden',
                        'delete_orden',
                        'can_create_order',
                        'can_edit_order',
                        'can_delete_order',
                        'can_view_all_orders',
                        'change_user',
                    ]
                ))

            usuario.save()
            Actividad.objects.create(
                usuario=request.user,
                accion='Edición de usuario',
                descripcion=f'Usuario "{usuario.username}" actualizado al rol "{role}".',
            )
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('gestion_usuarios')

    return render(request, 'editar_usuario.html', {
        'usuario': usuario,
        'roles': roles,
    })


@login_required
def eliminar_usuario(request, user_id):
    if not (request.user.is_superuser or request.user.has_perm('auth.change_user')):
        messages.error(request, 'No tienes permisos para eliminar usuarios.')
        return redirect('dashboard')

    if request.method == 'POST':
        if request.user.id == user_id:
            messages.error(request, 'No puedes eliminar tu propio usuario.')
        else:
            usuario = get_object_or_404(User, pk=user_id)
            if usuario.is_superuser:
                messages.error(request, 'No puedes eliminar un superusuario.')
            else:
                usuario.delete()
                Actividad.objects.create(
                    usuario=request.user,
                    accion='Eliminación de usuario',
                    descripcion=f'Usuario "{usuario.username}" eliminado.',
                )
    return redirect('gestion_usuarios')


@login_required
def actividad(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='admin').exists()):
        messages.error(request, 'No tienes permisos para ver la actividad.')
        return redirect('dashboard')

    usuario_filtro = request.GET.get('usuario', '')
    fecha_filtro = request.GET.get('fecha', '')
    actividades = Actividad.objects.select_related('usuario').all()
    usuarios = User.objects.order_by('username')

    if usuario_filtro:
        actividades = actividades.filter(usuario__id=usuario_filtro)

    if fecha_filtro:
        try:
            fecha_obj = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
            actividades = actividades.filter(timestamp__date=fecha_obj)
        except ValueError:
            messages.error(request, 'Fecha inválida. Usa el formato YYYY-MM-DD.')

    return render(request, 'actividad.html', {
        'actividades': actividades,
        'usuarios': usuarios,
        'usuario_filtro': usuario_filtro,
        'fecha_filtro': fecha_filtro,
        'timezone_label': 'Zona horaria hora estándar central (MT)',
    })


@login_required
def reportes(request):
    import json
    from django.db.models import Count
    from django.db.models.functions import TruncMonth

    # Filters
    usuario_filtro = request.GET.get('usuario', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    fecha_fin = request.GET.get('fecha_fin', '').strip()

    qs = Orden.objects.all()
    if usuario_filtro:
        qs = qs.filter(usuario__icontains=usuario_filtro)
    if fecha_inicio:
        qs = qs.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        qs = qs.filter(fecha__lte=fecha_fin)

    # KPIs
    total = qs.count()
    pendientes = qs.filter(estatus='pendiente').count()
    en_proceso = qs.filter(estatus='proceso').count()
    completadas = qs.filter(estatus='completo').count()
    facturas = qs.filter(factura__isnull=False).count()

    # Monthly aggregation (by fecha if present, else creado_en)
    month_field = 'fecha' if Orden.objects.filter(fecha__isnull=False).exists() else 'creado_en'
    monthly_qs = qs.exclude(**{f"{month_field}__isnull": True}).annotate(month=TruncMonth(month_field)).values('month').annotate(count=Count('id')).order_by('month')
    monthly_labels = [m['month'].strftime('%Y-%m') for m in monthly_qs]
    monthly_data = [m['count'] for m in monthly_qs]

    # Orders per user
    users_qs = qs.values('usuario').annotate(count=Count('id')).order_by('-count')
    user_labels = [u['usuario'] for u in users_qs]
    user_data = [u['count'] for u in users_qs]

    # Status percentages
    status_counts = qs.values('estatus').annotate(count=Count('id'))
    status_map = {s['estatus']: s['count'] for s in status_counts}
    status_labels = ['pendiente', 'proceso', 'completo']
    status_data = [status_map.get(k, 0) for k in status_labels]

    context = {
        'fecha_actual': timezone.localdate(),
        'total': total,
        'pendientes': pendientes,
        'en_proceso': en_proceso,
        'completadas': completadas,
        'facturas': facturas,
        'monthly_labels_json': json.dumps(monthly_labels),
        'monthly_data_json': json.dumps(monthly_data),
        'user_labels_json': json.dumps(user_labels),
        'user_data_json': json.dumps(user_data),
        'status_labels_json': json.dumps(status_labels),
        'status_data_json': json.dumps(status_data),
        'usuario_filtro': usuario_filtro,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }

    return render(request, 'reportes.html', context)