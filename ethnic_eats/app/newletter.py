from .models import SubscribeNewLetter
from rest_framework.views import APIView
from rest_framework import serializers, status
from django.http import JsonResponse


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribeNewLetter
        fields = '__all__'


class SubscribeToNewletter(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        
        if SubscribeNewLetter.objects.filter(email = email).exists():
            return JsonResponse({"message": "You are already subscribed"}, status = status.HTTP_200_OK)
        
        serializer = SubscriberSerializer(data = request.data, many = False)
        if serializer.is_valid():
            subscriber = SubscribeNewLetter.objects.create(email = email)
            return JsonResponse({"message": "Successfully subscribed to our newsletter"}, status = status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, {"message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

        