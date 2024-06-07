from django.db import models
from django.contrib.auth.models import User


#cuisine models
class Cuisine(models.Model):
    cuisine_id = models.AutoField(unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    name = models.CharField(max_length = 70, unique = True)
    description = models.CharField(max_length = 400)
    location = models.CharField(max_length=100, default='')
    contact = models.CharField(max_length = 500)
    address = models.CharField(max_length = 100)
    website = models.CharField(max_length = 100)
    time_open = models.TimeField(blank=True, null=True)
    time_close = models.TimeField(blank=True, null=True)
    cuisine_pic = models.FileField(upload_to='cuisines/', blank=True, null=True)


    def __str__(self):
        return self.name

# user reviews of cuisines and model
class Reviews(models.Model):
    review_id = models.AutoField(unique=True, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    review = models.CharField(max_length=300)
    score = models.FloatField(default=0.5)

    def __str__(self):
        return self.review


#user post model
class UserPost(models.Model):
    post_id = models.AutoField(unique=True, primary_key=True)
    created = models.DateTimeField(auto_now_add = True)
    post_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post_description = models.CharField(max_length = 2000)


#picture in a user post
class PostPicture(models.Model):
    post = models.ForeignKey(UserPost, related_name = 'post', on_delete=models.CASCADE)
    post_pic = models.FileField(upload_to='posts/')

    def __str__(self):
        return self.post.post_owner + ' posted ' + self.post.post_description


#meal model
class MealModel(models.Model):
    meal_id = models.AutoField(unique = True, primary_key = True)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length = 50, unique = True)
    price = models.FloatField()
    category = models.CharField(max_length = 50)
    meal_pic = models.FileField(upload_to='meals/', blank=True, null=True)


    def __str__(self):
        return self.meal_name + ' was added in ' + self.cuisine.name + ' menu'

#location oof a cuisine
class LocationDetail(models.Model):
    location_id = models.AutoField(unique = True, primary_key=True)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    address = models.CharField(max_length = 100)
    latitude = models.CharField(max_length = 50)
    longitude = models.CharField(max_length = 50)


class ReservationModel(models.Model):
    reservation_id = models.AutoField(unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    total_seats = models.CharField(max_length=20)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.user} made a reservation on {self.cuisine}"


class Inquires(models.Model):
    inquiry_id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=1000)
