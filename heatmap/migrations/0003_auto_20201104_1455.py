# Generated by Django 3.1.1 on 2020-11-04 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heatmap', '0002_auto_20201029_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heatmapdata',
            name='locdict',
            field=models.CharField(default='null', max_length=2000),
        ),
    ]
