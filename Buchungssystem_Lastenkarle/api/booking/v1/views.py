from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.permissions import IsVerfied
from django.core.exceptions import *
from django.http import Http404
from api.serializer import *
from db_model.models import *
from api.algorithm import split_availabilities_algorithm
from send_mail.views import send_booking_confirmation


class AllStores(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllRegions(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(Store.REGION, status=status.HTTP_200_OK)


class AllAvailabilities(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request):
        availabilities = Availability.objects.all()
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllBikes(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request):
        bikes = Bike.objects.all()
        serializer = BikeSerializer(bikes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request, bike_id):
        try:
            bike = Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = BikeSerializer(bike, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreByBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request, bike_id):
        try:
            bike = Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = StoreSerializer(bike.store, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailabilityOfBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request, bike_id):
        try:
            bike = Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        availability_of_bike = Availability.objects.filter(bike=bike)
        serializer = AvailabilitySerializer(availability_of_bike, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MakeBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsVerfied]

    def post(self, request, bike_id):
        try:
            bike = Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        user = self.request.user
        additional_data = {
            'bike': bike.pk,
        }
        data = {**request.data, **additional_data}
        serializer = MakeBookingSerializer(data=data)
        if serializer.is_valid():
            booking = serializer.save(user=user)
            booking.booking_status.set(Booking_Status.objects.filter(booking_status='Booked'))
            booking_string = generate_random_string(5)
            booking.string = booking_string
            booking.save()
            split_availabilities_algorithm(booking)
            send_booking_confirmation(booking)
            serializer = BookingSerializer(booking, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
