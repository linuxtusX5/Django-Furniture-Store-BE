from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    # price = models.FloatField(validators=[MinValueValidator(0.0)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    material = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)
    dimensions = models.CharField(max_length=100, blank=True, help_text="e.g., 120x80x75 cm")

    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_featured']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    @property
    def in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0

    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name


class Order(models.Model):
    """Order model with status tracking"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    total_price = models.FloatField(validators=[MinValueValidator(0.0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.customer.full_name}"

    @property
    def items_count(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    subtotal = models.FloatField(validators=[MinValueValidator(0.0)])

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['product', 'customer']

    def __str__(self):
        return f"{self.product.name} - {self.rating} stars by {self.customer.full_name}"