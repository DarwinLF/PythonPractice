# Generated by Django 3.2.23 on 2024-01-02 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0004_auto_20231220_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='rnc',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='customer',
            name='rnc',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='employee',
            name='rnc',
            field=models.CharField(max_length=13),
        ),
    ]
