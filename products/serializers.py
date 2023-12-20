from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import Product


class ProductSerializer(ModelSerializer):
    total_likes = SerializerMethodField()
    user_like = SerializerMethodField()

    def get_total_likes(self, obj):
        return obj.total_likes()

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

    def get_total_likes(self, obj):
        return obj.total_likes()

    def get_user_like(self, obj):
        request = self.context.get('request')
        if request:
            return obj.user_like(request.user)
        return False
