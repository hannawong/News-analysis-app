# Generated by Django 3.1.1 on 2020-10-16 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_weibohot_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weibohot',
            name='url',
            field=models.CharField(max_length=100),
        ),
    ]
