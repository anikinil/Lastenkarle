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
        serializer = StoreSerializer(Store.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllRegions(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = RegionSerializer(Region.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllAvailabilities(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = AvailabilitySerializer(Availability.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllBikes(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = BikeSerializer(Bike.objects.all(), many=True)
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
        serializer = StoreSerializer(bike.store, exclude=['store_flag'], many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailabilityOfBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request, bike_id):
        try:
            bike = Bike.objects.get(pk=bike_id)
            availability_of_bike = Availability.objects.filter(bike=bike)
        except ObjectDoesNotExist:
            raise Http404
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
        data = {
            'begin': request.data['begin'],
            'end': request.data['end'],
            'bike': bike.pk
        }
        serializer = MakeBookingSerializer(data=data, context={'no_limit': False})
        serializer.is_valid(raise_exception=True)
        booking = serializer.save(user=request.user)
        split_availabilities_algorithm(booking)
        send_booking_confirmation(booking)
        return Response(status=status.HTTP_201_CREATED)
