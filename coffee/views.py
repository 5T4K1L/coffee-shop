from django.shortcuts import render, redirect
from .models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
# Create your views here.


@login_required(login_url="login/")
def homepage(request):
    product = Products.objects.filter(bestProduct='MUST TRY')
    bestProduct = Products.objects.filter(bestProduct='BEST PRODUCT')

    context = {
        'product': product,
        'bestProduct': bestProduct,
    }

    return render(request, "index.html", context)


@login_required(login_url="login/")
def menu(request):
    product = Products.objects.filter(category='COLD')
    hotProduct = Products.objects.filter(category='HOT')

    context = {
        'product': product,
        'hotProduct': hotProduct,
    }

    return render(request, 'menu.html', context)


@login_required(login_url="login/")
def product_view(request, slug):

    product = Products.objects.get(slug=slug)
    comment = Comment.objects.filter(product=product)

    context = {
        'product': [product],
        'comment': comment,
    }

    return render(request, 'productview.html', context)


def addComment(request):

    product_id = request.GET.get('product_id')
    product = get_object_or_404(Products, id=product_id)
    comment = request.GET.get('addcomment')

    Comment(user=request.user, product=product, comment=comment).save()
    return redirect('menu')


@login_required(login_url="login/")
def cart(request):

    if request.user.is_authenticated:
        items = OrdersInCart.objects.filter(user=request.user)

    context = {
        'items': items,
    }

    return render(request, 'cart.html', context)


def checkoutPage(request):
    products_ordered = OrdersInCart.objects.filter(user=request.user)

    totalPrice = list(
        OrdersInCart.objects.values_list('price', flat=True))
    numeric_prices = [int(price) for price in totalPrice]
    total_sum = sum(numeric_prices)

    if request.method == 'POST':
        user = request.user
        full_name = request.POST['fullname']
        contact_num = request.POST['contactnumber']
        full_add = request.POST['fulladdress']
        msg = request.POST['message']

        BillingAddress(user=user, full_name=full_name,
                       contact_number=contact_num, full_address=full_add, message=msg, total_price=total_sum).save()

        return redirect("homepage")

    context = {
        'usersCart': products_ordered,
        'total': total_sum,
    }

    return render(request, 'checkout.html', context)


def add_to_cart(request):
    product_id = request.GET.get("prod_id")
    product_size = request.GET.get("size")
    product_quantity = request.GET.get("quantity")
    product_price = request.GET.get("total_placeholder")

    product = Products.objects.filter(id=product_id)
    product_name = Products.objects.get(id=product_id)

    for p in product:
        image = p.productImage
        OrdersInCart(user=request.user, image=image, name=product_name, size=product_size,
                     quantity=product_quantity, price=product_price).save()

    return redirect("menu")


def remove_from_cart(request, item_id):

    item = OrdersInCart.objects.get(pk=item_id)

    item.delete()
    return redirect('cart')


def registerPage(request):

    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password']

        user = User.objects.create_user(username=username, password=password1)
        user.save()

        return redirect('login')

    return render(request, 'register.html')


def loginPage(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            print("No named hehe")

    return render(request, 'login.html')


def logoutView(request):
    logout(request)
    return redirect("login")


def adminPanel(request):

    if request.user.is_staff or request.user.is_superuser:
        userCount = User.objects.count()

        total_purchase = BillingAddress.objects.count()

        totalIncome = list(
            BillingAddress.objects.values_list('total_price', flat=True))
        numeric_prices = [int(price) for price in totalIncome]
        total_sum = sum(numeric_prices)

        ordered = BillingAddress.objects.all()

        context = {
            'userCount': userCount,
            'totalIncome': total_sum,
            'totalpurch': total_purchase,
            'ordered': ordered,
        }

        return render(request, 'adminpanel.html', context)

    else:
        return redirect('homepage')


def whoOrdered(request, full_name):

    user_billing_address = BillingAddress.objects.get(full_name=full_name)

    user = user_billing_address.user

    user_orders = OrdersInCart.objects.filter(user=user)

    context = {
        'user': user_billing_address,
        'order': user_orders,
    }

    return render(request, 'view_user.html', context)
