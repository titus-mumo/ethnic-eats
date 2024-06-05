from rest_framework import serializers, status
from .models import Inquires
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.mail import send_mail


class InquirySerializers(serializers.ModelSerializer):
    class Meta:
        model = Inquires
        fields = '__all__'

class InquiryView(APIView):

    def post(self, request):
        inquiry_data = InquirySerializers(data = request.data)

        if inquiry_data.is_valid():
            saved_inquiry = inquiry_data.save()
            subject = f'New Inquiry: {saved_inquiry.subject}'
            message = f'You have received a new inquiry from {saved_inquiry.name}.\n\n' \
                      f'Email: {saved_inquiry.email}\n' \
                      f'Subject: {saved_inquiry.subject}\n' \
                      f'Message:\n{saved_inquiry.message}'
            from_email = 'tituskennedy74@gmail.com'
            recipient_list = ['tituskennedy74@gmail.com']

            # Send email
            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
            )

            return JsonResponse(inquiry_data.data, status = status.HTTP_201_CREATED)
        else:
            return JsonResponse(inquiry_data.errors, status = status.HTTP_400_BAD_REQUEST)
