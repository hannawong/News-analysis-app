# Generated by Django 3.1.1 on 2020-10-16 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_auto_20201016_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weibohot',
            name='url0',
        ),
    ]