from django.contrib import admin
from .models import Category, Product, Customer, Order, OrderItem, Review

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    lst_display = ['name', 'created_at', 'products_count']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    ordering = ['name']

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'price', 'stock',
        'material', 'color', 'is_featured', 'created_at'
    ]
    list_filter = ['category', 'is_featured', 'material', 'color', 'created_at']
    search_fields = ['name', 'description', 'material', 'color']
    list_editable = ['price', 'stock', 'is_featured']
    ordering = ['-created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'image')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock', 'is_featured')
        }),
        ('Specifications', {
            'fields': ('material', 'color', 'demensions')
        })
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'city', 'country', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'city', 'country']
    list_filter = ['country', 'city', 'created_at']
    ordering = ['-created_at']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['subtotal']
    fields = ['product','quantity', 'subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer', 'total_price', 'status',
        'items_count', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['customer__full_name', 'customer__email']
    list_editable = ['status']
    ordering = ['-created_at']
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'total_price', 'status')
        }),
        ('Additional Details', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Items'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'subtotal']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['product__name', 'order__customer__full_name']
    readonly_fields = ['subtotal']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'customer__full_name', 'comment']
    ordering = ['-created_at']

    fieldsets =(
        ('Review Information', {
            'fields': ('product', 'customer', 'rating', 'comment')
        }),
        ('Timestamp', {
        'fields': ('created_at', ),
        'classes': ('collapse', )
        }),
    )
    readonly_fields = ['created_at']