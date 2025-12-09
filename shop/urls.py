from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'reviews', views.ReviewViewSet)

urlpatterns = [
    path('', views.api_overview, name='api-overview'),
    path('', include(router.urls)),
    path('auth/register/', views.register_user, name='register'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
]

