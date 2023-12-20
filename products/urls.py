from django.urls import path
from .views import ProductCreateAPIView, ProductListAPIView, ProductDetailView, UserProductList

urlpatterns = [
    path('create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('', ProductListAPIView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('user/', UserProductList.as_view(), name='user-product-list'),
]
