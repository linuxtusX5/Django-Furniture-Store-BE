from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Q, F
from django.contrib.auth import authenticate

from .models import Category, Product, Customer, Order, OrderItem, Review
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    CustomerSerializer, OrderSerializer, OrderCreateSerializer,
    OrderItemSerializer, ReviewSerializer, UserRegistrationSerializer,
    AnalyticsSerializer
)
from .filters import ProductFilter

# Create your views here.
class CategoryViewSet(viewsets, ModelViewSet):
    queryset = Category.objects.all()
    serializers_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SerializerFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class ProductViewSet(viewsets, ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['price', 'created_at', 'name', 'stock']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_products = self.queryset.filter(is_featured=True)
        page = self.paginate_queryset(featured_products)

        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProductListSerializer(featured_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class CustomerViewSet(viewsets.ModelSerializer):
    queryset = Customer.objects.all()
    serializers_class = CustomerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'phone', 'city', 'country']
    ordering_fields = ['full_name', 'created_at']

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        customer = self.get_object()
        orders = customer.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelSerializer):
    queryset = Order.objects.select_related('customer').prefetch_related('items').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'customer']
    ordering_fields = ['created_at', 'total_price']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('product', 'customer').all()
    serializers_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'customer', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # Create associated customer
        customer_data = request.data.get('customer', {})
        customer = Customer.objects.create(
            user=user,
            full_name = customer_data.get('full_name', f"{user.first_name} {user.last_name}"),
            email = user.email,
            phone = customer_data.get('phone', ''),
            address = customer_data.get('address', ''),
            city = customer_data.get('city', ''),
            country = customer_data.get('country', '')
        )

        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'customer': CustomerSerializer(customer).data
        }, status = status.HTTP_201_CREATED)

    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)