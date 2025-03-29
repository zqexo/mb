# Generated by Django 5.1.4 on 2025-01-26 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='size_list',
            field=models.TextField(blank=True, editable=False, verbose_name='Список размеров'),
        ),
        migrations.AddField(
            model_name='category',
            name='total_sizes',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Общее количество размеров'),
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Размер')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Размер',
                'verbose_name_plural': 'Размеры',
            },
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_sizes', to='catalog.product', verbose_name='Продукт')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_sizes', to='catalog.size', verbose_name='Размер')),
            ],
            options={
                'verbose_name': 'Размер продукта',
                'verbose_name_plural': 'Размеры продуктов',
                'unique_together': {('product', 'size')},
            },
        ),
    ]
