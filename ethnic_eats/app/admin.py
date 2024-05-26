from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Reviews)
class UserReviewsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Reviews._meta.fields]

@admin.register(models.Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Cuisine._meta.fields]
    
@admin.register(models.UserPost)
class UserPostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.UserPost._meta.fields]

@admin.register(models.LocationDetail)
class LocationDetailAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.LocationDetail._meta.fields]


@admin.register(models.MealModel)
class MealModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.MealModel._meta.fields]


@admin.register(models.PostPicture)
class PostPictureAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.PostPicture._meta.fields]


@admin.register(models.CuisinePictures)
class CuisinePicturesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.CuisinePictures._meta.fields]

# @admin.register(models.CommunityForumModel)
# class CommunityForumAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in models.CommunityForumModel._meta.fields]

@admin.register(models.ReservationModel)
class ReservationModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.ReservationModel._meta.fields]