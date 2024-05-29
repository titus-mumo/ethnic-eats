from rest_framework import serializers, status
from .models import Inquires
from rest_framework.views import APIView
from django.http import JsonResponse


class InquirySerializers(serializers.ModelSerializer):
    class Meta:
        model = Inquires
        fields = '__all__'

class InquiryView(APIView):

    def post(self, request):
        inquiry_data = InquirySerializers(data = request.data)

        if inquiry_data.is_valid():
            saved_inquiry = inquiry_data.save()
            return JsonResponse(inquiry_data.data, status = status.HTTP_201_CREATED)
        else:
            return JsonResponse(inquiry_data.errors, status = status.HTTP_400_BAD_REQUEST)
