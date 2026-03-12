from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.user_logout, name='logout'),
    path('category/<category_slug>', views.category_views, name='category'),
    path('products', views.products_list, name='products'),
    path('contact', views.contact, name='contact'),
    path('add-to-cart/<product_id>', views.add_to_cart, name='add_to_cart'),
    path('cart-list', views.cart_list, name='cart_list'),
    path('increment-quantity/<cart_id>', views.increment_quantity, name='increment-quantity'),
    path('decrement-quantity/<cart_id>', views.decrement_quantity, name='decrement-quantity'),
    path('delete-quantity/<cart_id>', views.delete_quantity, name='delete-quantity'),
    path('clear-cart', views.clear_cart, name='clear-cart'),
]
