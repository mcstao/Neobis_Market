from rest_framework import generics, permissions
from django.shortcuts import render
from users_app.permission import IsVerifiedOrReadOnly, IsOwnerProfileOrReadOnly
from products.serializers import ProductSerializer, ProductDetailSerializer
from .models import Product


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedOrReadOnly]


class UserProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(author=self.request.user)
