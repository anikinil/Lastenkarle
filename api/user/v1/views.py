from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializer import *


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