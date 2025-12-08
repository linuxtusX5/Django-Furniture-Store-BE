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

