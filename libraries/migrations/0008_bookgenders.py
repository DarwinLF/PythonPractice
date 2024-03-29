# Generated by Django 3.2.23 on 2024-01-11 01:23

from django.db import migrations, models

def create_initial_book_genders(apps, schema_editor):
    BookGenders = apps.get_model('libraries', 'BookGenders')
    genders = ['Fiction', 'Non-Fiction', 'Poetry', 'Drama', 'Science Fiction', 
               'Fantasy', 'Mystery and Suspense', 'Romance', 'Adventure',
               'Historical', 'Humor']

    for gender in genders:
        BookGenders.objects.create(name=gender)


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0007_rename_count_to_rent_rent_amount_to_rent'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookGenders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RunPython(create_initial_book_genders)
    ]
