# Generated by Django 3.2.23 on 2023-12-21 01:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('persons', '0004_auto_20231220_2101'),
        ('libraries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rents_due', to='persons.customer'),
        ),
        migrations.AddField(
            model_name='rent',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rents_done', to='persons.employee'),
        ),
        migrations.AddField(
            model_name='rent',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rents', to='libraries.library'),
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='persons.author'),
        ),
        migrations.AddField(
            model_name='book',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='libraries.bookstatus'),
        ),
    ]
