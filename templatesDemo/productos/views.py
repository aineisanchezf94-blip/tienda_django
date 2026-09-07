from django.shortcuts import render
from django.utils.text import slugify
from .models import Producto


def lista_productos(request):
    """Devuelve todos los productos activos transformados a objetos simples
    con propiedades `slug`, `nombre`, `precio`, `imagen` y `categoria` para
    que las plantillas (partials) los consuman de forma consistente.
    """
    productos_list = []
    try:
        categoria_req = request.GET.get('categoria')
        qs = Producto.objects.filter(activo=True)
        for p in qs:
            # Mantener el FileField si existe para poder usar `.url` en plantilla
            img = p.imagen if getattr(p, 'imagen', None) else None
            categoria_obj = None
            try:
                categoria_obj = type('C', (), {'nombre': p.categoria.nombre})()
            except Exception:
                categoria_obj = type('C', (), {'nombre': ''})()

            # Si el request pidió una categoría, filtrar por ella (case-insensitive)
            if categoria_req and categoria_obj.nombre.lower() != categoria_req.lower():
                continue

            prod_obj = type('P', (), {})()
            prod_obj.slug = slugify(p.nombre)
            prod_obj.nombre = p.nombre
            prod_obj.precio = p.precio
            prod_obj.imagen = img
            prod_obj.categoria = categoria_obj
            productos_list.append(prod_obj)
        # Construir lista completa (sin filtrar por categoría) para mostrar "todos los productos"
        all_products = []
        for p in qs:
            img = p.imagen if getattr(p, 'imagen', None) else None
            try:
                categoria_obj = type('C', (), {'nombre': p.categoria.nombre})()
            except Exception:
                categoria_obj = type('C', (), {'nombre': ''})()
            prod_obj = type('P', (), {})()
            prod_obj.slug = slugify(p.nombre)
            prod_obj.nombre = p.nombre
            prod_obj.precio = p.precio
            prod_obj.imagen = img
            prod_obj.categoria = categoria_obj
            all_products.append(prod_obj)
    except Exception:
        # Fallback con datos de ejemplo si la BD no responde
        from types import SimpleNamespace
        sample = []
        sample.append(SimpleNamespace(slug='mac', nombre='Mac', imagen=None, categoria=SimpleNamespace(nombre='electronica'), precio=1299.00))
        sample.append(SimpleNamespace(slug='iphone', nombre='iPhone', imagen=None, categoria=SimpleNamespace(nombre='electronica'), precio=999.00))
        sample.append(SimpleNamespace(slug='playstation', nombre='PlayStation', imagen=None, categoria=SimpleNamespace(nombre='electronica'), precio=499.00))
        sample.append(SimpleNamespace(slug='auto', nombre='Auto', imagen=None, categoria=SimpleNamespace(nombre='juguetes'), precio=19.99))
        sample.append(SimpleNamespace(slug='pelota-de-futbol', nombre='Pelota de Fútbol', imagen=None, categoria=SimpleNamespace(nombre='juguetes'), precio=24.99))
        sample.append(SimpleNamespace(slug='pantalones', nombre='Pantalones', imagen=None, categoria=SimpleNamespace(nombre='ropa'), precio=39.99))
        productos_list = sample
        all_products = sample

    # Pasar la categoría solicitada y la lista completa al template
    # Si no hay productos en la BD, usar datos de ejemplo para que la página no quede vacía
    if not all_products:
        from types import SimpleNamespace
        sample = []
        sample.append(SimpleNamespace(slug='mac', nombre='Mac', imagen=None, categoria=SimpleNamespace(nombre='electronica'), precio=1299.00))
        sample.append(SimpleNamespace(slug='iphone', nombre='iPhone', imagen=None, categoria=SimpleNamespace(nombre='electronica'), precio=999.00))
        sample.append(SimpleNamespace(slug='playstation', nombre='PlayStation', imagen=None, categoria=SimpleNamespace(nombre='electronica'), precio=499.00))
        sample.append(SimpleNamespace(slug='auto', nombre='Auto', imagen=None, categoria=SimpleNamespace(nombre='juguetes'), precio=19.99))
        sample.append(SimpleNamespace(slug='pelota-de-futbol', nombre='Pelota de Fútbol', imagen=None, categoria=SimpleNamespace(nombre='juguetes'), precio=24.99))
        sample.append(SimpleNamespace(slug='pantalones', nombre='Pantalones', imagen=None, categoria=SimpleNamespace(nombre='ropa'), precio=39.99))
        all_products = sample

    return render(request, 'templatesApp/catalogo.html', {'productos': productos_list, 'categoria': request.GET.get('categoria'), 'todos_productos': all_products})
