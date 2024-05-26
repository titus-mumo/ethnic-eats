from rest_framework.views import APIView
from django.contrib.auth.models import Group, User
from .models import Cuisine, ReservationModel
from django.http import JsonResponse
from rest_framework import status, permissions
from .serializers import ReservationPostSerializer, ReservationGetSerializer


class ReservationViewForUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        if User.objects.filter(id = user.id).exists():
            data = request.data
            data['user'] = user.id
            cuisine = Cuisine.objects.filter(cuisine_id = data.get('cuisine')).first()
            if not cuisine:
                return JsonResponse({"message": " Restaurant not found"}, status = status.HTTP_404_NOT_FOUND)
            serializer = ReservationPostSerializer(data = data)
            if serializer.is_valid():
                reservation = ReservationModel.objects.create(user = user, cuisine = cuisine, total_seats  = data.get('total_seats'), time = data.get('time'))
                serialized_reservation = ReservationGetSerializer(reservation, many = False)
                return JsonResponse(serialized_reservation.data, status = status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
    def get(self, request):
        user = request.user
        reservations = ReservationModel.objects.filter(user = user)
        serialized_reservations = ReservationGetSerializer(reservations, many = True)
        return JsonResponse(serialized_reservations.data, status = status.HTTP_200_OK, safe=False)
    
class ReservationViewForCuisine(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, cuisine_id):
        try:
            cuisine = Cuisine.objects.filter(cuisine_id = cuisine_id).first()
            if not cuisine:
                return JsonResponse({"massage": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Cuisine.DoesNotExist:
            return JsonResponse({"message": "Restaurant not found"}, status = status.HTTP_404_NOT_FOUND)
        try:
            reservations = ReservationModel.objects.filter(cuisine = cuisine)
            serializer = ReservationGetSerializer(reservations, many = True)
            return JsonResponse(serializer.data, status = status.HTTP_200_OK, safe = False)
        except ReservationModel.DoesNotExist:
            return JsonResponse({"message" : "Reservations specific for this cuisine not found"})
        
class DeleteReservationView(APIView):
        permission_classes = [permissions.IsAuthenticated]
        def delete(self, request, reservation_id):
            user = request.user
            try:
                reservation = ReservationModel.objects.get(user=user, reservation_id=reservation_id)
                reservation.delete()
                return JsonResponse({"message": "Reservation deleted successfully."}, status=status.HTTP_200_OK)
            except ReservationModel.DoesNotExist:
                return JsonResponse({"error": "Reservation not found."}, status=status.HTTP_404_NOT_FOUND)
               

