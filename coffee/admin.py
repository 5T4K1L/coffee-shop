from django.contrib import admin
from .models import *

# Register your models here.


class ModelAdmin(admin.ModelAdmin):
    # Include 'id' and other fields you want to display
    list_display = ('id', 'slug')


admin.site.register(Products)
admin.site.register(OrdersInCart)
admin.site.register(Comment)
admin.site.register(BillingAddress)
admin.site.register(UsersOrderNotif)
