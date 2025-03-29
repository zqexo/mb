# Generated by Django 5.1.4 on 2025-01-24 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='static/default_img/avatar.jpg', help_text='Загрузите изображение для вашего профиля', null=True, upload_to='avatars/', verbose_name='Аватар'),
        ),
    ]
