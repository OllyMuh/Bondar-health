from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Order, OrderItem


def order_pdf(obj):
    return format_html('<a href="{}">{}</a>',
                       reverse('orders:invoice_pdf', args=[obj.id]), 'PDF')

order_pdf.short_description = 'Invoice'


class OrderItemInline(admin.TabularInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'address', 'postal_code', 'city',
        # 'transport',
        'created', 'status', order_pdf
        ]
    list_filter = ['created', 'updated']

    inlines = [OrderItemInline]

