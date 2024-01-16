# Generated by Django 3.2.23 on 2024-01-16 23:11

from django.db import migrations, models
import django.db.models.deletion

def populate_data(apps, schema_editor):
    CustomerStatus = apps.get_model('persons', 'CustomerStatus')
    CustomerStatus.objects.create(name='Active Borrower')
    CustomerStatus.objects.create(name='Expired Membership')
    CustomerStatus.objects.create(name='Overdue Materials')
    CustomerStatus.objects.create(name='Blocked Account')
    CustomerStatus.objects.create(name='Suspended Borrowing Privileges')
    CustomerStatus.objects.create(name='Outstanding Fines')
    CustomerStatus.objects.create(name='Restricted Access')
    CustomerStatus.objects.create(name='Reference Only')
    CustomerStatus.objects.create(name='Guest User')
    CustomerStatus.objects.create(name='Lost Card')
    CustomerStatus.objects.create(name='Renewal Pending')

class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0005_auto_20240102_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RunPython(populate_data),
        migrations.AddField(
            model_name='customer',
            name='credit_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='persons.customerstatus'),
            preserve_default=False,
        ),
        
    ]
