# Generated by Django 3.1.1 on 2020-10-16 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20201016_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weibohot',
            name='url',
            field=models.CharField(default='null', max_length=200, null=True),
        ),
    ]
