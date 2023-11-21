from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404

from django.contrib import messages
# Create your views here.


def welcomePage(request):

    if request.user.is_authenticated:
        return redirect("homepage")
    else:
        return render(request, 'welcome.html')


@login_required(login_url="login")
def homepage(request):
    product = Products.objects.filter(bestProduct='MUST TRY')
    bestProduct = Products.objects.filter(bestProduct='BEST PRODUCT')

    context = {
        'product': product,
        'bestProduct': bestProduct,
    }

    return render(request, "index.html", context)


@login_required(login_url="login")
def menu(request):
    all_product = Products.objects.all()

    context = {
        'all': all_product,
    }

    return render(request, 'menu.html', context)


@login_required(login_url="login")
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


@login_required(login_url="login")
def cart(request):

    if request.user.is_authenticated:
        items = OrdersInCart.objects.filter(user=request.user)

    context = {
        'items': items,
    }

    return render(request, 'cart.html', context)


@login_required(login_url="login")
def checkoutPage(request):
    products_ordered = OrdersInCart.objects.filter(user=request.user)

    numeric_prices = [int(order.price) for order in products_ordered]

    total_sum = sum(numeric_prices)

    if request.method == 'POST':
        user = request.user
        full_name = request.POST['fullname']
        contact_num = request.POST['contactnumber']
        full_add = request.POST['fulladdress']
        msg = request.POST['message']

        BillingAddress(user=user, full_name=full_name,
                       contact_number=contact_num, full_address=full_add, message=msg, total_price=total_sum).save()

        products_ordered.delete()

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

        UserProductInAdmin(user=request.user, prod_name=product_name, prod_size=product_size,
                           prod_quantity=product_quantity, prod_price=product_price).save()

    return redirect("menu")


def remove_from_cart(request, item_id):

    item = OrdersInCart.objects.get(pk=item_id)

    item.delete()
    return redirect('cart')


def registerPage(request):

    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password1)
        user.save()

        return redirect('login')

    return render(request, 'register.html')


def loginPage(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("homepage")
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logoutView(request):
    logout(request)
    return redirect("login")


def adminPanel(request):

    if request.user.is_staff or request.user.is_superuser:
        userCount = User.objects.count()

        total_purchase = BillingAddress.objects.count()

        totalIncome = list(
            Completed.objects.values_list('price', flat=True))
        numeric_prices = [int(price) for price in totalIncome]
        total_sum = sum(numeric_prices)

        ordered = BillingAddress.objects.all()

        completed = Completed.objects.all().order_by('-id')

        context = {
            'userCount': userCount,
            'totalIncome': total_sum,
            'totalpurch': total_purchase,
            'ordered': ordered,
            'completed': completed,
        }

        return render(request, 'adminpanel.html', context)

    else:
        return redirect('homepage')


def whoOrdered(request, full_name):

    user_billing_address = BillingAddress.objects.get(full_name=full_name)
    user = user_billing_address.user

    user_orders = UserProductInAdmin.objects.filter(user=user)

    if request.method == 'POST':

        user_billing_address.is_complete = 'YES'
        user_billing_address.save()

        for order in user_orders:
            Completed.objects.create(
                full_name=user_billing_address.full_name,
                product_name=order.prod_name,
                price=order.prod_price,
                product=order.prod_size,
                quantity=order.prod_quantity,
            )

        user_billing_address.delete()
        user_orders.delete()

        return redirect('adminPanel')

    context = {
        'user': user_billing_address,
        'order': user_orders,
    }

    return render(request, 'view_user.html', context)


@login_required(login_url="login")
def orderedCold(request):

    category = Products.objects.filter(category='COLD')

    context = {
        'category': category,
    }

    return render(request, 'coldcat.html', context)


@login_required(login_url="login")
def orderedHot(request):

    category = Products.objects.filter(category='HOT')

    context = {
        'category': category,
    }

    return render(request, 'hotcat.html', context)
