from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

from django.core.paginator import Paginator

from . form import ContactForm
from .models import *

# Create your views here.

def index(request):
    search = request.GET.get('search')
    if search:
        data = Product.objects.filter(Q(name__icontains=search) 
                                      | Q(category__name__icontains=search))
        sendData={
            'products': data
        }
        return render(request, 'pages/search-list.html', sendData)
    else:
        data={
            'products':Product.objects.all()
        }
        return render(request, 'pages/index.html', data)


def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'pages/index.html')
        else:
            return render(request, 'pages/login.html')
    else:
        data={
            'form': AuthenticationForm()
        }
        return render(request, 'pages/login.html', data)

def user_logout(request):
    logout(request)
    return render(request, 'pages/index.html')


def register(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username, password=password)
            login(request, user)
            return render(request, 'pages/index.html')
        else:
            data={
                'form': form
            }
            return render(request, 'pages/register.html', data)
    else:
        data={
            'form': UserCreationForm()
        }
        return render(request, 'pages/register.html', data)
    


def contact(request):
        if request.method=="POST":
            form=ContactForm(request.POST)
            if form.is_valid():
                # form.save()
                return render(request, 'pages/index.html')
            else:
                data={
                    'form': form
                }
                return render(request, 'pages/contact.html', data)
        else:
            data={
                'form': ContactForm()
            }
            return render(request, 'pages/contact.html', data)  
        

def category_views(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    cat_id = category.id
    products = Product.objects.filter(category=cat_id)
    data={
        'products': products
    }
    return render(request, 'pages/category-products.html', data)


def products_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 3) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    data={
        'products': page_obj
    }
    return render(request, 'pages/products.html', data)




def add_to_cart(request, product_id):
    p_id = product_id
    find_product_object = Product.objects.get(id=p_id)
    product_session_key = request.session.get('product_unique_cart_key', None)
    if product_session_key:
        cart_object = UniqueCart.objects.get(id=product_session_key)
        exists_product = cart_object.cartproduct_set.filter(product=find_product_object)
        if exists_product:
            product_object = exists_product.last()
            product_object.quantity += 1
            product_object.sub_total += find_product_object.price
            product_object.save()
            cart_object.total += find_product_object.price
            cart_object.save()
        else:
            cart_product = CartProduct.objects.create(
                cart=cart_object,
                product=find_product_object,
                rate=find_product_object.price,
                quantity=1,
                sub_total=find_product_object.price

            )
            cart_product.save()
            cart_object.total += find_product_object.price
            cart_object.save()

    else:
        unique_cart_object = UniqueCart.objects.create(total=0)
        request.session['product_unique_cart_key'] = unique_cart_object.id
        cart_product = CartProduct.objects.create(
            cart=unique_cart_object,
            product=find_product_object,
            rate=find_product_object.price,
            quantity=1,
            sub_total=find_product_object.price
        )
        cart_product.save()
        unique_cart_object.total += find_product_object.price
        unique_cart_object.save()


    messages.success(request, "Cart was successfully create")
    back =request.META.get('HTTP_REFERER')
    return redirect(back)


def cart_list(request):
    product_unique_cart_id = request.session.get('product_unique_cart_key')
    if product_unique_cart_id:
        data = UniqueCart.objects.get(id=product_unique_cart_id)
    else:
        data = None

    content = {
        'allCartData': data
    }

    return render(request, 'pages/cat-list.html', content)




def increment_quantity(request, cart_id):
    get_cat_id = cart_id
    cart_product_object = CartProduct.objects.get(id=get_cat_id)
    ct = cart_product_object.cart
    cart_product_object.quantity += 1
    cart_product_object.sub_total += cart_product_object.rate
    cart_product_object.save()
    ct.total += cart_product_object.rate
    ct.save()
    messages.success(request, "Cart was successfully update")
    return redirect(request.META.get('HTTP_REFERER'))


def decrement_quantity(request, cart_id):
    get_cat_id = cart_id
    cart_product_object = CartProduct.objects.get(id=get_cat_id)
    ct = cart_product_object.cart
    cart_product_object.quantity -= 1
    cart_product_object.sub_total -= cart_product_object.rate
    cart_product_object.save()
    ct.total -= cart_product_object.rate
    ct.save()
    if cart_product_object.quantity == 0:
        cart_product_object.delete()
    messages.success(request, "Cart was successfully update")
    return redirect(request.META.get('HTTP_REFERER'))


def delete_quantity(request, cart_id):
    get_cat_id = cart_id
    cart_product_object = CartProduct.objects.get(id=get_cat_id)
    ct = cart_product_object.cart
    ct.total -= cart_product_object.sub_total
    ct.save()
    cart_product_object.delete()
    messages.success(request, "Cart was successfully deleted")
    return redirect(request.META.get('HTTP_REFERER'))


def clear_cart(request):
    get_key = request.session.get('product_unique_cart_key')
    cart = UniqueCart.objects.get(id=get_key)
    cart.cartproduct_set.all().delete()
    cart.total = 0
    cart.save()
    messages.success(request, "Cart was successfully remove")
    return redirect(request.META.get('HTTP_REFERER'))
