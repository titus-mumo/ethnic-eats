# Generated by Django 5.0 on 2024-05-16 08:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_cuisine_id_mealmodel_cuisine'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityForumModel',
            fields=[
                ('communityforum_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReservationModel',
            fields=[
                ('reservation_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('total_seats', models.CharField(max_length=20)),
                ('time', models.TimeField()),
                ('cuisine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cuisine')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]