# Generated by Django 5.0.6 on 2024-06-06 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_cuisine_cuisine_pic_delete_cuisinepictures'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuisine',
            name='time_close',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cuisine',
            name='time_open',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
