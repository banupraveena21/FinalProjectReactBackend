from django.contrib import admin
from .models import Product, CartItem, Order, OrderItem

# Register Product with slug prepopulated and list display
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Automatically fills slug from name
    search_fields = ('name',)
    list_filter = ('stock',)

# Register CartItem with useful display info
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    search_fields = ('user__username', 'product__name')

# Register Order with status and date filter
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)

# Register OrderItem inline to show inside Order admin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price_at_order')
    can_delete = False
    extra = 0

# Update OrderAdmin to show OrderItems inline
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]

# Re-register OrderAdmin to include the inline
admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)
