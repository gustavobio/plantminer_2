# Generated by Django 3.0.3 on 2020-02-25 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_details_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='occurrence',
            field=models.CharField(max_length=170, null=True),
        ),
        migrations.AlterField(
            model_name='details',
            name='vegetation_type',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
