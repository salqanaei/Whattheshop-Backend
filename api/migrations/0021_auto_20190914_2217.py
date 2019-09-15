# Generated by Django 2.1.5 on 2019-09-14 22:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0020_auto_20190914_2119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='item',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Cart'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
