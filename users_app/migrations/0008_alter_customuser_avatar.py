# Generated by Django 4.2.8 on 2023-12-21 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0007_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='https://res.cloudinary.com/dbiyaguqb/image/upload/v1703179554/media/avatar_pics/pitcrmjoyykcpaqy2gjj.jpg', upload_to='avatar_pics/'),
        ),
    ]
