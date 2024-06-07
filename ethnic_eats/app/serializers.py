from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Cuisine, UserPost, Reviews, MealModel, LocationDetail, ReservationModel

#User serializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

#User Serializers
    #register user serializer
class CreateNewUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Login Serializer
class UserLoginSerielizer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    # change password serializer serializer
class ChangePassWordSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)

    # SendPassWordRestEmailSerializer serializer
class SendPassWordRestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)

    # reset password serializer
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required  = True)


#GroupSerializer  

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

#User Post Serielisers
    # get serializer
class UserPostGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = ['post_id', 'created', 'post_owner', 'post_description']

    # post serializer
class UserPostPostSerielizer(serializers.Serializer):
    user = serializers.IntegerField(read_only=True)
    post_description = serializers.CharField(required=True)




#Review Serializers
    #post
class UserReviewPostSerielizer(serializers.Serializer):
    review = serializers.CharField(required = True)
    cuisine = serializers.IntegerField(read_only = True)
    score = serializers.FloatField(required = True)

    #get
class UserReviewSerielizer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['review_id', 'created', 'cuisine', 'review', 'score']


#Cuisine Serializer
        #get
class CuisineGetSerializer(serializers.Serializer):
    cuisine_id = serializers.IntegerField(read_only = True)
    user = UserSerializer(read_only = True)
    created_at = serializers.DateTimeField()
    name = serializers.CharField(required = True)
    description = serializers.CharField(required = True)
    location = serializers.CharField(required = True)
    contact = serializers.CharField(required = True)
    contact = serializers.CharField(required=True)
    website = serializers.CharField(required = True)
    time_open = serializers.TimeField(required = True)
    time_close = serializers.TimeField(required = True)
    cuisine_pic = serializers.FileField(required = True)

        #post
class CuisinePostSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    description = serializers.CharField(required = True)
    location = serializers.CharField(required = True)
    address = serializers.CharField(required = True)
    contact = serializers.CharField(required = True)
    website = serializers.CharField(required = True)
    time_open = serializers.TimeField(required = True)
    time_close = serializers.TimeField(required = True)
    cuisine_pic = serializers.FileField(required = True)


#meal serializers
    #get
class MealGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealModel
        fields = '__all__'
    #post
class MealPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealModel
        fields = '__all__'

    #cuisine_based menu serializer
class CuisineBasedMenuPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealModel
        fields = ['meal_name', 'price', 'category']

#location serializers
    #get
class LocationDetailGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationDetail
        fields = ['location_id', 'address', 'latitude', 'longitude']

    #post
class LocationDetailPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationDetail
        fields = ['address', 'latitude', 'longitude']


#reservation serializers
    #get
class ReservationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationModel
        fields = ['reservation_id', 'user', 'cuisine', 'total_seats', 'time']
    
    #post
class ReservationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationModel
        fields = ['user', 'cuisine', 'total_seats', 'time']


# from .models import CommunityForumModel
# class GetForumSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CommunityForumModel
#         fields = '__all__'




