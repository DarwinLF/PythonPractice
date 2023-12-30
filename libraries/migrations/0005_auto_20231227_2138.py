# Generated by Django 3.2.23 on 2023-12-28 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0004_library_rnc'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='library',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, related_name='books', to='libraries.library'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=17, unique=True),
        ),
        migrations.AlterField(
            model_name='library',
            name='rnc',
            field=models.CharField(max_length=13, unique=True),
        ),
    ]