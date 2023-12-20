from django.db import models

from users_app.models import CustomUser


class Product(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_pics/', blank=True, null=True)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField()
    likes = models.ManyToManyField(CustomUser, related_name='liked_products', blank=True)

    def total_likes(self):
        return self.likes.count()

    def user_like(self, user):
        return self.likes.filter(pk=user.pk).exists()

    def __str__(self):
        return f"{self.title} - {self.author}"


