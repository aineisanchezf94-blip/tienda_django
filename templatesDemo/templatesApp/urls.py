from django.urls import path
from . import views

urlpatterns = [
    path('', views.tienda_home, name='index'),
    path('producto/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('lang/<str:lang>/', views.set_language, name='set_language'),
    path('carrito/eliminar/<slug:slug>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
]