from django.shortcuts import render
from django.http import Http404
from django.utils.text import slugify

def tienda_home(request):
    # Catálogo simulado usando diccionarios con slug, descripción, precio e imagen
    PRODUCTS = {
        'mac': {
            'nombre': 'Mac',
            'descripcion': 'Portátil MacBook con gran rendimiento.',
            'precio': 1299.00,
            'imagen': 'templatesApp/imagenes/mac.png'
        },
        'iphone': {
            'nombre': 'iPhone',
            'descripcion': 'Teléfono inteligente Apple.',
            'precio': 999.00,
            'imagen': 'templatesApp/imagenes/iphone.png'
        },
        'playstation': {
            'nombre': 'PlayStation',
            'descripcion': 'Consola de videojuegos moderna.',
            'precio': 499.00,
            'imagen': 'templatesApp/imagenes/playstation.png'
        },
        'auto': {
            'nombre': 'Auto',
            'descripcion': 'Coche de juguete para niños.',
            'precio': 19.99,
            'imagen': 'templatesApp/imagenes/Autos.png'
        },
        'pelota-de-futbol': {
            'nombre': 'Pelota de Fútbol',
            'descripcion': 'Pelota oficial de fútbol.',
            'precio': 24.99,
            'imagen': 'templatesApp/imagenes/pelota.png'
        },
        'figura-de-accion': {
            'nombre': 'Figura de Acción',
            'descripcion': 'Figura coleccionable articulada.',
            'precio': 14.99,
            'imagen': 'templatesApp/imagenes/figura.png'
        },
        'pantalones': {
            'nombre': 'Pantalones',
            'descripcion': 'Pantalones cómodos y resistentes.',
            'precio': 39.99,
            'imagen': 'templatesApp/imagenes/pantalones.png'
        },
        'chaqueta': {
            'nombre': 'Chaqueta',
            'descripcion': 'Chaqueta de abrigo para invierno.',
            'precio': 79.99,
            'imagen': 'templatesApp/imagenes/chaqueta.png'
        },
        'camisa': {
            'nombre': 'Camisa',
            'descripcion': 'Camisa de algodón de alta calidad.',
            'precio': 29.99,
            'imagen': 'templatesApp/imagenes/camisa.png'
        },
    }

    # Categorías listas como slugs que referencian las keys de PRODUCTS
    CATALOG = {
        'electronica': ['mac', 'iphone', 'playstation'],
        'juguetes': ['auto', 'pelota-de-futbol', 'figura-de-accion'],
        'ropa': ['pantalones', 'chaqueta', 'camisa']
    }

    # Soporte de búsqueda por query 'q'
    query = request.GET.get('q', '').strip()
    categoria_seleccionada = request.GET.get('categoria')
    productos_slugs = CATALOG.get(categoria_seleccionada, [])

    # Convertimos slugs a estructuras con slug y nombre para la plantilla
    productos = []
    for slug in productos_slugs:
        p = PRODUCTS.get(slug)
        if p:
            productos.append({'slug': slug, 'nombre': p['nombre'], 'precio': p.get('precio'), 'descripcion': p.get('descripcion'), 'imagen': p.get('imagen')})
    
    # Si hay búsqueda, filtramos todos los productos por nombre/descripcion
    if query:
        productos = []
        for slug, p in PRODUCTS.items():
            if query.lower() in p['nombre'].lower() or query.lower() in p['descripcion'].lower():
                productos.append({'slug': slug, 'nombre': p['nombre'], 'precio': p.get('precio'), 'descripcion': p.get('descripcion'), 'imagen': p.get('imagen')})

    # Obtener total del carrito desde session
    cart = request.session.get('cart', {})
    cart_total = 0.0
    for slug, qty in cart.items():
        prod = PRODUCTS.get(slug)
        if prod:
            cart_total += prod['precio'] * qty
    contexto = {
        'nombre_usuario': 'Ainelyn',
        'categoria': categoria_seleccionada,
        'productos': productos,
        'cart_total': cart_total,
        'query': query,
    }
    # Guardamos los diccionarios para que product_detail los consulte mediante la misma fuente
    request._productos_catalog = PRODUCTS
    return render(request, 'templatesApp/index.html', contexto)


def product_detail(request, slug):
    # Intentamos obtener el catálogo centralizado; si no existe, reconstruimos la data mínima
    PRODUCTS = getattr(request, '_productos_catalog', None)
    if PRODUCTS is None:
        # Mismo dataset reducido por si se llama directamente
        PRODUCTS = {
            'mac': {'nombre': 'Mac', 'descripcion': 'Portátil MacBook con gran rendimiento.', 'precio': 1299.00, 'imagen': 'templatesApp/imagenes/mac.png'},
            'iphone': {'nombre': 'iPhone', 'descripcion': 'Teléfono inteligente Apple.', 'precio': 999.00, 'imagen': 'templatesApp/imagenes/iphone.png'},
            'playstation': {'nombre': 'PlayStation', 'descripcion': 'Consola de videojuegos moderna.', 'precio': 499.00, 'imagen': 'templatesApp/imagenes/playstation.png'},
            'auto': {'nombre': 'Auto', 'descripcion': 'Coche de juguete para niños.', 'precio': 19.99, 'imagen': 'templatesApp/imagenes/Autos.png'},
            'pelota-de-futbol': {'nombre': 'Pelota de Fútbol', 'descripcion': 'Pelota oficial de fútbol.', 'precio': 24.99, 'imagen': 'templatesApp/imagenes/pelota.png'},
            'figura-de-accion': {'nombre': 'Figura de Acción', 'descripcion': 'Figura coleccionable articulada.', 'precio': 14.99, 'imagen': 'templatesApp/imagenes/figura.png'},
            'pantalones': {'nombre': 'Pantalones', 'descripcion': 'Pantalones cómodos y resistentes.', 'precio': 39.99, 'imagen': 'templatesApp/imagenes/pantalones.png'},
            'chaqueta': {'nombre': 'Chaqueta', 'descripcion': 'Chaqueta de abrigo para invierno.', 'precio': 79.99, 'imagen': 'templatesApp/imagenes/chaqueta.png'},
            'camisa': {'nombre': 'Camisa', 'descripcion': 'Camisa de algodón de alta calidad.', 'precio': 29.99, 'imagen': 'templatesApp/imagenes/camisa.png'},
        }

    producto = PRODUCTS.get(slug)
    if not producto:
        raise Http404('Producto no encontrado')
    # Capturamos categoría previa si viene en la querystring (para el botón volver)
    prev_categoria = request.GET.get('categoria')
    # Si no viene explícita, intentamos inferirla desde el Referer (p. ej. la página que enlazó)
    if not prev_categoria:
        referer = request.META.get('HTTP_REFERER', '')
        if referer:
            try:
                from urllib.parse import urlparse, parse_qs
                qs = parse_qs(urlparse(referer).query)
                prev_list = qs.get('categoria')
                if prev_list:
                    prev_categoria = prev_list[0]
            except Exception:
                prev_categoria = None
    contexto = {
        'producto': producto,
        'slug': slug,
        'prev_categoria': prev_categoria,
    }
    # incluir total del carrito
    cart = request.session.get('cart', {})
    cart_total = 0.0
    for s, qty in cart.items():
        p = PRODUCTS.get(s)
        if p:
            cart_total += p['precio'] * qty
    contexto['cart_total'] = cart_total
    return render(request, 'templatesApp/product_detail.html', contexto)


def add_to_cart(request, slug):
    # Añade producto al carrito en session y redirige a la página del carrito
    PRODUCTS = {
        'mac': {'nombre': 'Mac', 'descripcion': 'Portátil MacBook con gran rendimiento.', 'precio': 1299.00},
        'iphone': {'nombre': 'iPhone', 'descripcion': 'Teléfono inteligente Apple.', 'precio': 999.00},
        'playstation': {'nombre': 'PlayStation', 'descripcion': 'Consola de videojuegos moderna.', 'precio': 499.00},
        'auto': {'nombre': 'Auto', 'descripcion': 'Coche de juguete para niños.', 'precio': 19.99},
        'pelota-de-futbol': {'nombre': 'Pelota de Fútbol', 'descripcion': 'Pelota oficial de fútbol.', 'precio': 24.99},
        'figura-de-accion': {'nombre': 'Figura de Acción', 'descripcion': 'Figura coleccionable articulada.', 'precio': 14.99},
        'pantalones': {'nombre': 'Pantalones', 'descripcion': 'Pantalones cómodos y resistentes.', 'precio': 39.99},
        'chaqueta': {'nombre': 'Chaqueta', 'descripcion': 'Chaqueta de abrigo para invierno.', 'precio': 79.99},
        'camisa': {'nombre': 'Camisa', 'descripcion': 'Camisa de algodón de alta calidad.', 'precio': 29.99},
    }

    if slug not in PRODUCTS:
        raise Http404('Producto no encontrado')

    cart = request.session.get('cart', {})
    cart[slug] = cart.get(slug, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    # Redirigir a la vista del carrito
    from django.shortcuts import redirect
    return redirect('view_cart')


def view_cart(request):
    PRODUCTS = {
        'mac': {'nombre': 'Mac', 'descripcion': 'Portátil MacBook con gran rendimiento.', 'precio': 1299.00, 'imagen': 'templatesApp/imagenes/mac.png'},
        'iphone': {'nombre': 'iPhone', 'descripcion': 'Teléfono inteligente Apple.', 'precio': 999.00, 'imagen': 'templatesApp/imagenes/iphone.png'},
        'playstation': {'nombre': 'PlayStation', 'descripcion': 'Consola de videojuegos moderna.', 'precio': 499.00, 'imagen': 'templatesApp/imagenes/playstation.png'},
        'auto': {'nombre': 'Auto', 'descripcion': 'Coche de juguete para niños.', 'precio': 19.99, 'imagen': 'templatesApp/imagenes/Autos.png'},
        'pelota-de-futbol': {'nombre': 'Pelota de Fútbol', 'descripcion': 'Pelota oficial de fútbol.', 'precio': 24.99, 'imagen': 'templatesApp/imagenes/pelota.png'},
        'figura-de-accion': {'nombre': 'Figura de Acción', 'descripcion': 'Figura coleccionable articulada.', 'precio': 14.99, 'imagen': 'templatesApp/imagenes/figura.png'},
        'pantalones': {'nombre': 'Pantalones', 'descripcion': 'Pantalones cómodos y resistentes.', 'precio': 39.99, 'imagen': 'templatesApp/imagenes/pantalones.png'},
        'chaqueta': {'nombre': 'Chaqueta', 'descripcion': 'Chaqueta de abrigo para invierno.', 'precio': 79.99, 'imagen': 'templatesApp/imagenes/chaqueta.png'},
        'camisa': {'nombre': 'Camisa', 'descripcion': 'Camisa de algodón de alta calidad.', 'precio': 29.99, 'imagen': 'templatesApp/imagenes/camisa.png'},
    }
    cart = request.session.get('cart', {})
    items = []
    total = 0.0
    for slug, qty in cart.items():
        prod = PRODUCTS.get(slug)
        if prod:
            subtotal = prod['precio'] * qty
            total += subtotal
            items.append({'slug': slug, 'nombre': prod['nombre'], 'precio': prod['precio'], 'cantidad': qty, 'subtotal': subtotal, 'imagen': prod.get('imagen')})

    contexto = {'items': items, 'total': total}
    return render(request, 'templatesApp/cart.html', contexto)


def set_language(request, lang):
    # Soporte simple de idioma mediante session
    if lang not in ('en', 'es'):
        lang = 'es'
    request.session['lang'] = lang
    # Redirigir a la página previa o al index
    from django.shortcuts import redirect
    next_url = request.GET.get('next', '/')
    return redirect(next_url)

def eliminar_del_carrito(request, slug):
    from django.shortcuts import redirect
    
    # Obtiene el diccionario del carrito de la sesión
    cart = request.session.get('cart', {})
    
    # Si el producto existe en el carrito, lo borra por completo
    if slug in cart:
        del cart[slug]
        request.session['cart'] = cart
        request.session.modified = True
        
    return redirect('view_cart')

