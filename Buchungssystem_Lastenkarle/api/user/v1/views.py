from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializer import *
from db_model.models import *


class ListBooking(APIView):


    def get(self, request, user_id):
        bookings = Booking.objects.filter(user_id=user_id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class DetailBooking(APIView):


    def get(self, request, user_id, booking_id):
        booking = Booking.objects.get(pk=booking_id)
        serializer = BookingSerializer(booking, many=False)
        return Response(serializer.data)


class DetailBikeByBooking(APIView):


    def get(self, request, user_id, booking_id):
        bike = Booking.objects.get(pk=booking_id).bike
        serializer = BikeSerializer(bike, many=False)
        return Response(serializer.data)


class DetailStoreByBike(APIView):


    def get(self, request, user_id, booking_id):
        store = Booking.objects.get(pk=booking_id).bike.store
        serializer = StoreSerializer(store, many=False)
        return Response(serializer.data)


class DetailUserData(APIView):


    def get(self, request, user_id):
        user_data = ID_Data.objects.get(user_id=user_id)
        serializer = UserDataSerializer(user_data, many=False)
        return Response(serializer.data)


class UserRegistration(APIView):


    def post(self, request):
        serializer = ID_DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)