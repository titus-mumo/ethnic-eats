# Generated by Django 5.0.6 on 2024-06-14 04:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inquires',
            fields=[
                ('inquiry_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('cuisine_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=70, unique=True)),
                ('description', models.CharField(max_length=400)),
                ('location', models.CharField(default='', max_length=100)),
                ('contact', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=100)),
                ('website', models.CharField(max_length=100)),
                ('time_open', models.TimeField(blank=True, null=True)),
                ('time_close', models.TimeField(blank=True, null=True)),
                ('cuisine_pic', models.FileField(blank=True, null=True, upload_to='cuisines/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LocationDetail',
            fields=[
                ('location_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('address', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('cuisine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cuisine')),
            ],
        ),
        migrations.CreateModel(
            name='MealModel',
            fields=[
                ('meal_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('meal_name', models.CharField(max_length=50, unique=True)),
                ('price', models.FloatField()),
                ('category', models.CharField(max_length=50)),
                ('meal_pic', models.FileField(blank=True, null=True, upload_to='meals/')),
                ('cuisine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cuisine')),
            ],
        ),
        migrations.CreateModel(
            name='ReservationModel',
            fields=[
                ('reservation_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('total_seats', models.CharField(max_length=20)),
                ('time', models.DateTimeField()),
                ('cuisine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cuisine')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('review', models.CharField(max_length=300)),
                ('score', models.FloatField(default=0.5)),
                ('cuisine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cuisine')),
            ],
        ),
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('post_description', models.CharField(max_length=2000)),
                ('post_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_pic', models.FileField(upload_to='posts/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='app.userpost')),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('meal_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.mealmodel')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_id', 'meal_id')},
            },
        ),
    ]
