# Generated by Django 5.1.3 on 2024-11-30 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='detail',
            field=models.TextField(blank=True, null=True),
        ),
    ]