# Generated by Django 4.1.2 on 2024-06-16 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veterinaria', '0006_producto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='id',
        ),
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
