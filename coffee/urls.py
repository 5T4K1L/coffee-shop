from coffee import views
from .views import *
from django.urls import include, path

# app_name = 'coffee'

urlpatterns = [
    path("", views.welcomePage, name='welcome'),

    path("homepage/", views.homepage, name="homepage"),
    path("menu/", views.menu, name="menu"),
    path("menu/product/<slug:slug>", views.product_view, name="productview"),
    path("track/", views.track_order, name='track'),
    path("cart/", views.cart, name='cart'),

    path("add_to_cart", views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/<int:admin_id>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkoutPage, name='checkoutPage'),

    path("addcomment/", views.addComment, name="addcomment"),

    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutView),

    path('admin-panel/', views.adminPanel, name='adminPanel'),
    path('receipt/', views.receipt, name='receipt'),
    path('view_user/<full_name>', views.whoOrdered, name='whoordered'),
    path('preparing/<full_name>', views.preparing, name='preparing'),
    path('out_delivery/<full_name>', views.outDelivery, name='outDelivery'),

    path('cold-products/', views.orderedCold, name='coldproducts'),
    path('hot-products/', views.orderedHot, name='hotproducts'),

    path('product_manager/', views.product_management, name="productmng"),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<int:pk>', views.update_product, name='update_product'),
    path('remove_product/<int:pk>', views.delete_product, name="delete_prod"),
]
