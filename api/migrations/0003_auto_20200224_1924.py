# Generated by Django 3.0.3 on 2020-02-24 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200221_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='synonym',
            name='accepted',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='synonyms', to='api.Accepted'),
        ),
    ]
