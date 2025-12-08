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


