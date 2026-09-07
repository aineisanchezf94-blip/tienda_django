from django.shortcuts import render
from django.utils.text import slugify
from .models import Producto


def _coincide_busqueda(nombre, descripcion, query):
    if not query:
        return True
    q = query.strip().lower()
    if not q:
        return True
    nombre_low = nombre.lower()
    descripcion_low = descripcion.lower()
    return (
        q in nombre_low or
        q in descripcion_low or
        nombre_low.startswith(q) or
        descripcion_low.startswith(q)
    )


def lista_productos(request):
    """Devuelve todos los productos activos transformados a objetos simples
    con propiedades `slug`, `nombre`, `precio`, `imagen` y `categoria` para
    que las plantillas (partials) los consumen de forma consistente.
    """
    productos_list = []
    query = request.GET.get('q', '').strip()
    try:
        categoria_req = request.GET.get('categoria')
        qs = Producto.objects.filter(activo=True)
        for p in qs:
            img = p.imagen if getattr(p, 'imagen', None) else None
            categoria_obj = None
            try:
                categoria_obj = type('C', (), {'nombre': p.categoria.nombre})()
            except Exception:
                categoria_obj = type('C', (), {'nombre': ''})()

            if categoria_req and categoria_obj.nombre.lower() != categoria_req.lower():
                continue

            if query and not _coincide_busqueda(p.nombre, p.descripcion or '', query):
                continue

            prod_obj = type('P', (), {})()
            prod_obj.slug = slugify(p.nombre)
            prod_obj.nombre = p.nombre
            prod_obj.precio = p.precio
            prod_obj.imagen = img
            prod_obj.categoria = categoria_obj
            productos_list.append(prod_obj)

        all_products = []
        for p in qs:
            img = p.imagen if getattr(p, 'imagen', None) else None
            try:
                categoria_obj = type('C', (), {'nombre': p.categoria.nombre})()
            except Exception:
                categoria_obj = type('C', (), {'nombre': ''})()

            if query and not _coincide_busqueda(p.nombre, p.descripcion or '', query):
                continue

            prod_obj = type('P', (), {})()
            prod_obj.slug = slugify(p.nombre)
            prod_obj.nombre = p.nombre
            prod_obj.precio = p.precio
            prod_obj.imagen = img
            prod_obj.categoria = categoria_obj
            all_products.append(prod_obj)
    except Exception:
        from types import SimpleNamespace
        sample = []
        sample.append(SimpleNamespace(slug='mac', nombre='Mac', imagen=None, categoria=SimpleNamespace(nombre='electronica'), precio=1299.00))
        sample.append(SimpleNamespace(slug='iphone', nombre='iPhone', imagen=None, categoria=SimpleNamespace(nombre='electronica'), precio=999.00))
        sample.append(SimpleNamespace(slug='playstation', nombre='PlayStation', imagen=None, categoria=SimpleNamespace(nombre='electronica'), precio=499.00))
        sample.append(SimpleNamespace(slug='auto', nombre='Auto', imagen=None, categoria=SimpleNamespace(nombre='juguetes'), precio=19.99))
        sample.append(SimpleNamespace(slug='pelota-de-futbol', nombre='Pelota de Fútbol', imagen=None, categoria=SimpleNamespace(nombre='juguetes'), precio=24.99))
        sample.append(SimpleNamespace(slug='pantalones', nombre='Pantalones', imagen=None, categoria=SimpleNamespace(nombre='ropa'), precio=39.99))
        productos_list = [s for s in sample if not query or _coincide_busqueda(s.nombre, '', query)]
        all_products = [s for s in sample if not query or _coincide_busqueda(s.nombre, '', query)]

    if not all_products:
        from types import SimpleNamespace
        sample = []
        sample.append(SimpleNamespace(slug='mac', nombre='Mac', imagen=None, categoria=SimpleNamespace(nombre='electronica'), precio=1299.00))
        sample.append(SimpleNamespace(slug='iphone', nombre='iPhone', imagen=None, categoria=SimpleNamespace(nombre='electronica'), precio=999.00))
        sample.append(SimpleNamespace(slug='playstation', nombre='PlayStation', imagen=None, categoria=SimpleNamespace(nombre='electronica'), precio=499.00))
        sample.append(SimpleNamespace(slug='auto', nombre='Auto', imagen=None, categoria=SimpleNamespace(nombre='juguetes'), precio=19.99))
        sample.append(SimpleNamespace(slug='pelota-de-futbol', nombre='Pelota de Fútbol', imagen=None, categoria=SimpleNamespace(nombre='juguetes'), precio=24.99))
        sample.append(SimpleNamespace(slug='pantalones', nombre='Pantalones', imagen=None, categoria=SimpleNamespace(nombre='ropa'), precio=39.99))
        all_products = [s for s in sample if not query or _coincide_busqueda(s.nombre, '', query)]

    return render(request, 'templatesApp/catalogo.html', {'productos': productos_list, 'categoria': request.GET.get('categoria'), 'todos_productos': all_products, 'query': query})
