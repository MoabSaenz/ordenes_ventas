from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Orden


@login_required
def home(request):
    mensaje = None
    error = None
    ordenes_qs = Orden.objects.order_by('-creado_en')

    if request.method == 'POST':
        try:
            orden = Orden(
                usuario=request.POST.get('usuario', '').strip(),
                numero_orden=request.POST.get('orden', '').strip(),
                fecha=request.POST.get('fecha') or None,
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
    })


def editar_orden(request, orden_id):
    orden = get_object_or_404(Orden, pk=orden_id)
    ordenes = Orden.objects.order_by('-creado_en')

    if request.method == 'POST':
        try:
            orden.usuario = request.POST.get('usuario', '').strip()
            orden.numero_orden = request.POST.get('orden', '').strip()
            orden.fecha = request.POST.get('fecha') or None
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

        return render(request, 'index.html', {'orden': orden, 'ordenes': ordenes, 'editando': True, 'error': error})

    return render(request, 'index.html', {'orden': orden, 'ordenes': ordenes, 'editando': True})


def eliminar_orden(request, orden_id):
    if request.method == 'POST':
        orden = get_object_or_404(Orden, pk=orden_id)
        orden.delete()
    return redirect('home')
