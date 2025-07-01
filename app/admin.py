from django.contrib import admin
from .models import Item, OrderItem, Order, Payment

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_number', 'price', 'category')
    readonly_fields = ('item_number',)

    
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)
