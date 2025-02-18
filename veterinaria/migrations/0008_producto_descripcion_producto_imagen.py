# Generated by Django 4.1.2 on 2024-06-16 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veterinaria', '0007_remove_producto_id_alter_producto_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='descripcion',
            field=models.CharField(default=3, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(default=2, upload_to='productos/'),
            preserve_default=False,
        ),
    ]
