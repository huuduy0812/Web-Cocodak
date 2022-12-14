import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from product.models import Product, Category
from cart.models import Cart, CartItem
from order.models import Order, Orderitem
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from user.models import User, Favorite
from order.models import Order
from django.contrib import messages, auth
from django.core.mail import EmailMessage


# Create your views here.
# cart = {}


def dishdetail_view(request, id):
    item = Product.objects.get(id=id)
    object_product = Product.objects.all()
    object_category = Category.objects.all()
    if request.user.is_authenticated:
        get_cart = Cart.objects.get(user_id=request.user)
        total = get_cart.total
        get_cartitem = CartItem.objects.filter(cart=get_cart)
        object_favorite = Favorite.objects.filter(user_id=request.user)
    else:
        total = 0
        get_cartitem = ''
        object_favorite = ''

    return render(request, 'dishdetail.html',
                  dict(object_product=object_product,
                       object_category=object_category,
                       total=total,
                       cartitem=get_cartitem,
                       product=item,
                       favorite=object_favorite
                       ))


def deletecart_index(request):
    if request.is_ajax():
        id = request.POST.get('id')
        user = User.objects.get(id=request.user.id)
        product = Product.objects.get(id=id)
        cart = Cart.objects.get(user_id=user)
        cartitem = CartItem.objects.filter(cart=cart).get(item=product)
        cart_user = Cart.objects.get(user_id=request.user)
        cart_user.total = round(cart_user.total - cartitem.total, 2)
        cart_user.save()
        cartitem.delete()

        html = render_to_string('deletecart.html', {'success': 'delete cart success'})
    return HttpResponse(html)


def Favorite_view(request):
    if request.user.is_authenticated:
        favorite = Favorite.objects.filter(user_id=request.user)
        object_product = Product.objects.all()
        object_category = Category.objects.all()

        get_cart = Cart.objects.get(user_id=request.user)
        total = get_cart.total
        get_cartitem = CartItem.objects.filter(cart=get_cart)

        return render(request, 'favorite.html', dict(
            favorite=favorite,
            object_product=object_product,
            object_category=object_category,
            total=total,
            cartitem=get_cartitem
        ))
    else:
        return redirect('index')


def order_view(request):
    object_product = Product.objects.all()
    object_category = Category.objects.all()
    total_all = 0
    total = 0
    if request.user.is_authenticated:
        get_cart = Cart.objects.get(user_id=request.user)
        total = get_cart.total
        get_cartitem = CartItem.objects.filter(cart=get_cart)
        count = get_cartitem.count()
    else:
        total = 0
        get_cartitem = ''
        count = 0
    if total > 0:
        ship = 5
        total_all = round(total * 1.1 + 5, 2)
    else:
        ship = 0
        total_all = 0

    return render(request, 'ordering.html',
                  dict(object_product=object_product,
                       object_category=object_category,
                       total=total,
                       cartitem=get_cartitem,
                       count=count,
                       total_all=total_all,
                       ship=ship
                       ))


def addcart(request):
    if request.is_ajax():
        id = request.POST.get('id')
        quantity = request.POST.get('qty')

        if request.user.is_authenticated:
            try:
                cart_user = Cart.objects.get(user_id=request.user)
            except:
                cart_user = Cart.objects.create(user_id=request.user)
            cartdetail = CartItem.objects.filter(cart=cart_user)
            product = Product.objects.get(id=id)
            try:
                cartitem = cartdetail.get(item=product)
            except:
                cartitem = ''
            if cartitem != '':
                cartitem.quantity += int(quantity)
                cartitem.save()
                html = render_to_string('addcart.html', {'cart': cart_user})
            else:
                new_cartitem = CartItem.objects.create(
                    cart=cart_user,
                    quantity=int(quantity),
                    item=product
                )
                new_cartitem.save()
                html = render_to_string('addcart.html', {'cart': cart_user})

    return HttpResponse(html)


def deletecart(request):
    if request.is_ajax():
        id = request.POST.get('id')
        if request.user.is_authenticated:
            cartitem = CartItem.objects.get(id=id)
            cart_user = Cart.objects.get(user_id=request.user)
            cart_user.total = round(cart_user.total - cartitem.total, 2)
            cart_user.save()
            cartitem.delete()

        html = render_to_string('deletecart.html', {'success': 'delete cart success'})
    return HttpResponse(html)


def quantity_cart(request):
    if request.is_ajax():
        id = request.POST.get('id')
        quantity = request.POST.get('qty')
        if request.user.is_authenticated:
            cartitem = CartItem.objects.get(id=id)
            cartitem.quantity = quantity
            cartitem.save()
        html = render_to_string('quantity_cart.html', {'success': 'success'})
    return HttpResponse(html)


def home_view(request):
    object_product = Product.objects.all()
    object_category = Category.objects.all()
    if request.user.is_authenticated:
        get_cart = Cart.objects.get(user_id=request.user)
        total = get_cart.total
        get_cartitem = CartItem.objects.filter(cart=get_cart)
        object_favorite = Favorite.objects.filter(user_id=request.user)
    else:
        total = 0
        object_favorite = ''
        get_cartitem = ''

    return render(request, 'index.html',
                  dict(object_product=object_product,
                       object_category=object_category,
                       total=total,
                       cartitem=get_cartitem,
                       favorite=object_favorite
                       ))


def search_view(request):
    if 'q' in request.GET:
        q = request.GET.get('q')
        search = Product.objects.filter(title__icontains=q)
        object_product = Product.objects.all()
        object_category = Category.objects.all()
        if request.user.is_authenticated:
            get_cart = Cart.objects.get(user_id=request.user)
            total = get_cart.total
            get_cartitem = CartItem.objects.filter(cart=get_cart)
            object_favorite = Favorite.objects.filter(user_id=request.user)
        else:
            total = 0
            object_favorite = ''
            get_cartitem = ''
        print(search)
    return render(request, 'search.html', dict(search=search, favorite=object_favorite,
                                               object_product=object_product,
                                               object_category=object_category,
                                               total=total,
                                               cartitem=get_cartitem,
                                               ))


def favorite(request):
    if request.is_ajax():
        id = request.POST.get('id')
        status = int(request.POST.get('status'))
        product = Product.objects.get(id=id)
        if status == 1:
            newfavorite = Favorite.objects.create(user_id=request.user,
                                                  product_id=product
                                                  )
            newfavorite.save()
        else:
            deletefavorite = Favorite.objects.filter(user_id=request.user).get(product_id=product)
            deletefavorite.delete()
        html = render_to_string('favorite_status.html', {'success': 'success'})
        return HttpResponse(html)


id_order = 0


def checkout_process(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user_id=request.user)
        print(cart)
        cartitem = CartItem.objects.filter(cart=cart)
        print(cartitem)
        total = cart.total
        total_all = round(total * 1.1 + 5, 2)
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        new_order = Order.objects.create(user=request.user,
                                         total=total,
                                         total_all=total_all,
                                         status=1,
                                         name=name,
                                         shipping_address=address,
                                         phone=phone
                                         )
        new_order.save()
        global id_order
        id_order = new_order.id
        for item in cartitem:
            product = item.item
            order = new_order
            quanity = item.quantity
            total = item.total
            orderitem = Orderitem.objects.create(product=product,
                                                 order=order,
                                                 quantity=quanity,
                                                 total=total
                                                 )
            orderitem.save()
            item.delete()
        cart.delete()
        newcart = Cart.objects.create(user_id=request.user)
        newcart.save()
    else:
        return redirect('login')
    return render(request, 'checkout.html')


def orderdetail(request):
    order = Order.objects.filter(user=request.user)
    return render(request, 'orderdetail.html', dict(order=order))


ordernow = {}
id_ordernow = 0
qty_ordernow = 1


def addorder(request):
    if request.is_ajax():
        id = request.POST.get['id']
        proDetail = Product.objects.get(id=id)
        itemcart = {
            'title': proDetail.title,
            'price': proDetail.price,
            'description': proDetail.description,
            'picture': str(proDetail.picture),
            'id': id
        }
        html = render_to_string('favorite_status.html', {'success': 'true'})
        ordernow[id] = itemcart
        request.session['ordernow'] = ordernow
        cartInfo = request.session['ordernow']
        html = render_to_string('favorite_status.html', {'success': html})
    return HttpResponse(html)


def ordernow(request):
    global id_ordernow, qty_ordernow
    product = Product.objects.get(id=id_ordernow)
    qty_ordernow = int(qty_ordernow)
    total = round(product.price * qty_ordernow, 2)
    total_all = round((total + 5) * 1.1, 2)
    if qty_ordernow < 10:
        qty_ordernow = '0' + str(qty_ordernow)

    return render(request, 'ordernow.html',
                  dict(product=product,
                       total=total,
                       total_all=total_all,
                       ship='5',
                       qty=qty_ordernow
                       ))


def checkout(request):
    global id_order
    order = Order.objects.get(id=id_order)

    return render(request, 'checkout.html', dict(order=order))


def deletefavorite(request):
    if request.is_ajax():
        id = request.POST.get('id')
        fav = Favorite.objects.get(id=id)
        fav.delete()
        html = render_to_string('favorite_status.html', {'success': 'true'})
    return HttpResponse(html)


def ordernow_process(request):
    if request.is_ajax():
        global id_ordernow, qty_ordernow
        id_ordernow = request.POST.get('id')
        qty_ordernow = request.POST.get('qty')
    html = render_to_string('favorite_status.html', {'success': 'true'})
    return HttpResponse(html)


def checkout_ordernow_process(request):
    name = request.POST.get('name')
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    qty = request.POST.get('qty')
    global id_ordernow
    product = Product.objects.get(id=id_ordernow)
    # print('\n\n\n' + qty + '\n\n\n')
    total = round(float(qty) * product.price)
    total_all = round(total * 1.1 + 5, 2)
    new_order = Order.objects.create(user=request.user,
                                     total=total,
                                     total_all=total_all,
                                     status=1,
                                     name=name,
                                     shipping_address=address,
                                     phone=phone
                                     )
    new_order.save()
    global id_order
    id_order = new_order.id
    return HttpResponse(status=204)


def favorite_add_check(request):
    if request.is_ajax():
        id = request.POST.get('id')
        product = Product.objects.get(id=id)
        x = 'false'
        try:
            favorite_check = Favorite.objects.filter(user_id=request.user).get(product_id=product)
        except:
            newfavorite = Favorite.objects.create(user_id=request.user,
                                                  product_id=product
                                                  )
            newfavorite.save()
            x = 'success'
        html = render_to_string('favorite_status.html', {'success': x})
    return HttpResponse(html)
