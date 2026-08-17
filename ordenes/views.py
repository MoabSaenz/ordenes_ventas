from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from .models import Orden
from .decorators import has_permission


def user_role_hint(user):
    """Optional helper: small role hint for backwards compatibility in templates."""
    if user.is_superuser or user.groups.filter(name='admin').exists():
        return 'admin'
    if user.has_perm('ordenes.can_create_order') and user.has_perm('ordenes.can_edit_order'):
        return 'capturista'
    if user.has_perm('ordenes.can_view_all_orders'):
        return 'lector'
    return None


@login_required
def home(request):
    mensaje = None
    error = None
    # Permission flags for templates and logic
    role = user_role_hint(request.user)
    puede_crear = request.user.has_perm('ordenes.can_create_order')
    puede_editar = request.user.has_perm('ordenes.can_edit_order')
    puede_eliminar = request.user.has_perm('ordenes.can_delete_order')
    puede_ver_todas = request.user.has_perm('ordenes.can_view_all_orders')
    # Filtrar órdenes según permiso
    ordenes_qs = Orden.objects.order_by('-creado_en')
    # Permitir visualización a capturistas y lectores (solo lectura), o a quienes tengan permiso global
    if not (puede_ver_todas or request.user.is_superuser or request.user.groups.filter(name__in=['capturista', 'lector']).exists()):
        ordenes_qs = ordenes_qs.filter(usuario=request.user.username)

    if request.method == 'POST':
        if not puede_crear:
            messages.error(request, 'No tienes permisos para crear órdenes.')
            return redirect('home')

        try:
            orden = Orden(
                usuario=request.POST.get('usuario', '').strip(),
                numero_orden=request.POST.get('orden', '').strip(),
                fecha=request.POST.get('fecha') or None,
                fecha_factura=request.POST.get('fecha_factura') or None,
                descripcion=request.POST.get('descripcion', '').strip(),
                estatus=request.POST.get('estatus', 'pendiente'),
                fecha_termino=request.POST.get('fecha_termino') or None,
                factura=int(request.POST.get('factura', 0)) if request.POST.get('factura') else None,
                comentarios=request.POST.get('comentarios', '').strip(),
                pdf=request.FILES.get('pdf'),
            )
            orden.save()
            mensaje = 'Orden guardada correctamente.'
        except ValueError:
            error = 'La factura debe ser numérica.'
        except IntegrityError as exc:
            error = f'No se pudo guardar la orden: {exc}'
        except Exception as exc:
            error = f'Error inesperado: {exc}'

        return redirect('home')

    search_usuario = request.GET.get('usuario', '').strip()
    search_orden = request.GET.get('orden', '').strip()
    search_factura = request.GET.get('factura', '').strip()
    search_fecha_factura = request.GET.get('fecha_factura', '').strip()
    search_estatus = request.GET.get('estatus', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    fecha_fin = request.GET.get('fecha_fin', '').strip()

    if search_usuario:
        ordenes_qs = ordenes_qs.filter(usuario__icontains=search_usuario)
    if search_orden:
        ordenes_qs = ordenes_qs.filter(numero_orden__icontains=search_orden)
    if search_factura:
        try:
            ordenes_qs = ordenes_qs.filter(factura=int(search_factura))
        except ValueError:
            pass
    if search_fecha_factura:
        ordenes_qs = ordenes_qs.filter(fecha_factura=search_fecha_factura)
    if search_estatus:
        ordenes_qs = ordenes_qs.filter(estatus__iexact=search_estatus)
    if fecha_inicio:
        ordenes_qs = ordenes_qs.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        ordenes_qs = ordenes_qs.filter(fecha__lte=fecha_fin)

    paginator = Paginator(ordenes_qs, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    result_count = ordenes_qs.count()

    query_params = {
        'usuario': search_usuario,
        'orden': search_orden,
        'factura': search_factura,
        'fecha_factura': search_fecha_factura,
        'estatus': search_estatus,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }

    return render(request, 'index.html', {
        'mensaje': mensaje,
        'error': error,
        'ordenes': page_obj,
        'page_obj': page_obj,
        'query_params': query_params,
        'result_count': result_count,
        'request': request,
        'role': role,
        'puede_crear': puede_crear,
        'puede_editar': puede_editar,
        'puede_eliminar': puede_eliminar,
        'puede_ver_todas': puede_ver_todas,
    })


@login_required
@has_permission('ordenes.can_edit_order')
def editar_orden(request, orden_id):
    orden = get_object_or_404(Orden, pk=orden_id)
    role = user_role_hint(request.user)
    if not request.user.has_perm('ordenes.can_edit_order'):
        messages.error(request, 'No tienes permisos para editar órdenes.')
        return redirect('home')
    ordenes = Orden.objects.order_by('-creado_en')

    if request.method == 'POST':
        try:
            orden.usuario = request.POST.get('usuario', '').strip()
            orden.numero_orden = request.POST.get('orden', '').strip()
            orden.fecha = request.POST.get('fecha') or None
            orden.fecha_factura = request.POST.get('fecha_factura') or None
            orden.descripcion = request.POST.get('descripcion', '').strip()
            orden.estatus = request.POST.get('estatus', 'pendiente')
            orden.fecha_termino = request.POST.get('fecha_termino') or None
            orden.factura = int(request.POST.get('factura', 0)) if request.POST.get('factura') else None
            orden.comentarios = request.POST.get('comentarios', '').strip()
            if request.FILES.get('pdf'):
                orden.pdf = request.FILES.get('pdf')
            orden.save()
            return redirect('home')
        except ValueError:
            error = 'La factura debe ser numérica.'
        except Exception as exc:
            error = f'Error inesperado: {exc}'

        return render(request, 'index.html', {'orden': orden, 'ordenes': ordenes, 'editando': True, 'error': error, 'role': role, 'puede_crear': True, 'puede_editar': True, 'puede_eliminar': role == 'admin'})

    return render(request, 'index.html', {'orden': orden, 'ordenes': ordenes, 'editando': True, 'role': role, 'puede_crear': True, 'puede_editar': True, 'puede_eliminar': request.user.has_perm('ordenes.can_delete_order')})


@login_required
def ver_orden(request, orden_id):
    orden = get_object_or_404(Orden, pk=orden_id)
    # Permitir ver si es superusuario, tiene permiso global de ver todas, o es propietario
    if not (request.user.is_superuser or request.user.has_perm('ordenes.can_view_all_orders') or orden.usuario == request.user.username):
        messages.error(request, 'No tienes permisos para ver esta orden.')
        return redirect('home')

    can_edit = request.user.has_perm('ordenes.can_edit_order')
    can_delete = request.user.has_perm('ordenes.can_delete_order')

    return render(request, 'ver_orden.html', {
        'orden': orden,
        'can_edit': can_edit,
        'can_delete': can_delete,
    })


@login_required
@has_permission('ordenes.can_delete_order')
def eliminar_orden(request, orden_id):
    if request.method == 'POST':
        orden = get_object_or_404(Orden, pk=orden_id)
        orden.delete()
    return redirect('home')
