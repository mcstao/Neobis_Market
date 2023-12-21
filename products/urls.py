from django.urls import path
from .views import ProductCreateAPIView, ProductListAPIView, ProductDetailView, UserProductList, ProductLikeAPIView, \
    ProductUnlikeAPIView, LikeListApiView, LikeProductCheckApiView

urlpatterns = [
    path('create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('', ProductListAPIView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('user/', UserProductList.as_view(), name='user-product-list'),
    path('like/<int:product_id>/', ProductLikeAPIView.as_view(), name='product-like'),
    path('unlike/<int:product_id>/', ProductUnlikeAPIView.as_view(), name='product-unlike'),
    path('likes/', LikeListApiView.as_view(), name='like-list'),
    path('likes/<int:pk>/', LikeProductCheckApiView.as_view(), name='like-product-check'),
]
