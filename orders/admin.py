from django.contrib import admin
from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'retailer',
        'total_amount',
        'status',
        'created_at'
    )


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)