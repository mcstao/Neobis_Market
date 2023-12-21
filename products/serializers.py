from drf_spectacular.utils import extend_schema_field
from rest_framework.fields import SerializerMethodField, IntegerField, BooleanField
from rest_framework.serializers import ModelSerializer

from .models import Product


class ProductSerializer(ModelSerializer):
    total_likes = SerializerMethodField()
    user_like = SerializerMethodField()

    @extend_schema_field(IntegerField())
    def get_total_likes(self, obj):
        return obj.total_likes()

    @extend_schema_field(BooleanField())
    def get_user_like(self, obj):
        return obj.user_like(self.context['request'].user)

    class Meta:
        model = Product
        fields = ["id", "author", "title", "price", "total_likes", "user_like", "image"]


class ProductDetailSerializer(ModelSerializer):
    total_likes = SerializerMethodField()
    user_like = SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "author", "title", "price", "total_likes", "user_like", "image", "short_description",
                  "long_description"]

    @extend_schema_field(IntegerField())
    def get_total_likes(self, obj):
        return obj.total_likes()

    @extend_schema_field(BooleanField())
    def get_user_like(self, obj):
        request = self.context.get('request')
        if request:
            return obj.user_like(request.user)
        return False
