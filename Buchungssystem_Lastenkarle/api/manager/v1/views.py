from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import *
from django.http import Http404

from api.algorithm import *
from api.permissions import *
from api.serializer import *
from db_model.models import *


class AllUserFlags(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated]

    def get(self, request):
        fields_to_include = ['user_status']
        flags = User_status.objects.all()
        serializer = UserFlagSerializer(flags, many=True, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BikesOfStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated]
    def get(self, request):
        store = self.request.user.is_staff_of_store()
        bikes = Bike.objects.filter(store=store)
        fields_to_include = ['id', 'name', 'description', 'image_link']
        serializer = BikeSerializer(bikes, many=True, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated]
    def get(self, request, bike_id):
        try:
            Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        fields_to_include = ['id', 'name', 'description', 'image_link']
        store = self.request.user.is_staff_of_store()
        bike = Bike.objects.get(pk=bike_id, store=store)
        serializer = BikeSerializer(bike, many=False, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SelectedBikeAvailability(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated]
    def get(self, request, bike_id):
        try:
            Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        fields_to_include = ['from_date', 'until_date', 'availability_status']
        store = self.request.user.is_staff_of_store()
        availabilities = Availability.objects.filter(bike_id=bike_id, store=store)
        serializer = AvailabilitySerializer(availabilities, many=True, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingsOfStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated]
    def get(self, request):
        store = self.request.user.is_staff_of_store()
        bookings = Booking.objects.filter(bike__store=store)
        fields_to_include = ['id', 'user', 'bike', 'begin', 'end', 'booking_status']
        serializer = BookingSerializer(bookings, many=True, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SelectedBookingOfStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff]

    def get(self, request, booking_id):
        bookings = Booking.objects.get(pk=booking_id)
        fields_to_include = ['user', 'bike', 'begin', 'end', 'booking_status']
        serializer = BookingSerializer(bookings, many=True, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #cancel booking
    def post(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id)
        booking.booking_status.clear()
        booking.booking_status.set(Booking_Status.objects.filter(booking_status='S'))
        booking.save()
        merge_availabilities_algorithm(booking)
        return Response(status=status.HTTP_200_OK)

class CommentToBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated]
    serializer_class = CommentSerializer
    def update(self, request, booking_id, *args, **kwargs):
        store = self.request.user.is_staff_of_store()
        instance = Comment.objects.get(store=store, booking_id=booking_id)
        serializer = CommentSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, booking_id):
        store = self.request.user.is_staff_of_store()
        comment = Comment.objects.get(store=store, booking_id=booking_id)
        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
