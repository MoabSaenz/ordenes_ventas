from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from .models import Orden


def home(request):
    mensaje = None
    error = None
    ordenes = Orden.objects.order_by('-creado_en')

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

    return render(request, 'index.html', {'mensaje': mensaje, 'error': error, 'ordenes': ordenes})


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
