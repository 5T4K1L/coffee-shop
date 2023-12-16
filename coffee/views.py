from django.core.exceptions import ObjectDoesNotExist
from .filters import ProductsFilter
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

from .forms import *
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
    mustTry = Products.objects.filter(bestProduct='MUST TRY')

    context = {
        'product': product,
        'bestProduct': bestProduct,
        'mustTry': mustTry
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


def track_order(request):

    try:
        billing_address = BillingAddress.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return render(request, "track_order.html")

    context = {
        'track': billing_address.is_what,
        'total': billing_address.total_price
    }

    return render(request, "track_order.html", context)


def preparing(request, full_name):
    user_billing_address = BillingAddress.objects.get(full_name=full_name)

    # Update the is_what field for the BillingAddress instance
    user_billing_address.is_what = 'Preparing your order'
    user_billing_address.save()

    # Trigger the WebSocket event after updating the data
    channel_layer = get_channel_layer()

    data = {'is_what': user_billing_address.is_what}

    async_to_sync(channel_layer.group_send)(
        "track_group", {
            "type": "send_track",
            "value": json.dumps(data)
        }
    )

    if request.method == 'POST':
        return redirect("adminPanel")


def outDelivery(request, full_name):
    user_billing_address = BillingAddress.objects.get(full_name=full_name)

    # Update the is_what field for the BillingAddress instance
    user_billing_address.is_what = 'Out for Delivery'
    user_billing_address.save()

    channel_layer = get_channel_layer()

    data = {'is_what': user_billing_address.is_what}

    async_to_sync(channel_layer.group_send)(
        "track_group", {
            "type": "send_track",
            "value": json.dumps(data)
        }
    )

    if request.method == 'POST':
        return redirect("adminPanel")


@login_required(login_url="login")
def cart(request):

    if request.user.is_authenticated:
        items = OrdersInCart.objects.filter(user=request.user)
        admin_cart = UserProductInAdmin.objects.filter(user=request.user)

        is_what_value = None

        try:
            billing = BillingAddress.objects.get(user=request.user)
            is_what_value = billing.is_what
        except ObjectDoesNotExist:
            pass

    context = {
        'items': items,
        'is_what_value': is_what_value,
        'admin_cart': admin_cart
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

        return redirect("track")

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


def remove_from_cart(request, item_id, admin_id):

    item = OrdersInCart.objects.get(pk=item_id)
    cart_admin = UserProductInAdmin.objects.get(pk=admin_id)

    cart_admin.delete()

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

        total_purchase = Completed.objects.count()

        totalIncome = list(
            Completed.objects.values_list('price', flat=True))
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


def receipt(request):
    completed = Completed.objects.all().order_by('-id')

    context = {
        'completed': completed,
    }

    return render(request, "receipt.html", context)


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

        user_orders.delete()
        user_billing_address.delete()

        channel_layer = get_channel_layer()

        data = {'is_what': user_billing_address.is_what}

        async_to_sync(channel_layer.group_send)(
            "track_group", {
                "type": "send_track",
                "value": json.dumps(data)
            }
        )

        return redirect('receipt')

    context = {
        'user': user_billing_address,
        'order': user_orders,
        'user_name': user,
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


def product_management(request):

    products = Products.objects.all()

    myFilter = ProductsFilter(request.GET, queryset=products)
    products = myFilter.qs

    context = {
        'products': products,
        'filter': myFilter,
    }

    return render(request, 'product_mng.html', context)


def create_product(request):
    createProducts = CreateProducts()

    if request.method == 'POST':
        form = CreateProducts(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("productmng")

    context = {
        'create_prod': createProducts
    }

    return render(request, 'create_product.html', context)


def update_product(request, pk):
    products = Products.objects.get(id=pk)
    createProducts = CreateProducts(instance=products)

    if request.method == 'POST':
        form = CreateProducts(request.POST, instance=products)
        if form.is_valid():
            form.save()
            return redirect('productmng')

    context = {
        'create_prod': createProducts
    }
    return render(request, 'create_product.html', context)


def delete_product(request, pk):

    product = Products.objects.get(id=pk)
    product.delete()

    return redirect('productmng')
