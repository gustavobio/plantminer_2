# Generated by Django 3.0.3 on 2020-02-25 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200225_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortnames',
            name='short_name',
            field=models.CharField(max_length=40),
        ),
    ]
