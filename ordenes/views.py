from django.shortcuts import render
from .models import Orden


def formulario(request):
    mensaje = None

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
            )
            orden.save()
            mensaje = 'Orden guardada correctamente.'
        except ValueError:
            mensaje = 'La factura debe ser numérica.'

    return render(request, 'index.html', {'mensaje': mensaje})
