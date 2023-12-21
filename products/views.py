from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response

from users_app.permission import IsVerifiedOrReadOnly, IsOwnerProfileOrReadOnly
from products.serializers import ProductSerializer, ProductDetailSerializer
from .models import Product


@extend_schema(
    description='Этот эндпоинт создает товар'
)
class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(
    description='Этот эндпоинт служит для получение всех товаров'
)
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema(
    description='Этот эндпоинт служит для просмотра, изменения, удаления 1 товара'
)
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedOrReadOnly]


@extend_schema(
    description='Этот эндпоинт возврщает товары пользователя'
)
class UserProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(author=self.request.user)


class ProductLikeAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        description='Этот эндпоинт служит для нажатия на лайк'
    )

    def patch(self, request, product_id):
        user = request.user
        if not user.is_verified:
            return Response({'message': 'Завершите регистрацию номера.'})
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response({'error': 'Товар не был найден.'}, status=status.HTTP_404_NOT_FOUND)
        if product.likes.filter(id=user.id).exists():
            return Response({'message': 'Вы уже лайкнули этот продукт.'}, status=status.HTTP_400_BAD_REQUEST)
        product.likes.add(user.id)
        return Response({'message': 'Продукт успешно добавлен в понравившиеся.'}, status=status.HTTP_200_OK)


class ProductUnlikeAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        description='Этот эндпоинт служит для отмены лайка'
    )

    def patch(self, request, product_id):
        user = request.user
        if not user.is_verified:
            return Response({'message': 'Вы должны завершить регситрацию номера.'})
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)
        if not product.likes.filter(id=user.id).exists():
            return Response({'message': 'Вы не лайкали этот продукт.'}, status=status.HTTP_400_BAD_REQUEST)
        product.likes.remove(user.id)
        return Response({'success': 'Товар успешно удален из понравившихся.'})


@extend_schema(
    description='Этот эндпоинт служит для просмотра понравившихся товаров'
)
class LikeListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        author = self.request.user.id
        queryset = Product.objects.filter(likes__id=author)
        return queryset


@extend_schema(
    description='Просмотр лайкнутого товара, если надо'
)
class LikeProductCheckApiView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        author = self.request.user.id
        queryset = Product.objects.filter(likes__id=author)
        return queryset
