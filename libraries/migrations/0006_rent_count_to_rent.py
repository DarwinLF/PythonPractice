# Generated by Django 3.2.23 on 2024-01-02 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0005_auto_20231227_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='count_to_rent',
            field=models.IntegerField(default=1),
        ),
    ]
