# Generated by Django 3.0.3 on 2020-02-28 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20200226_0206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Words',
            fields=[
                ('word', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
    ]