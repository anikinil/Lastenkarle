from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import *
from django.http import Http404
from api.serializer import *
from db_model.models import *
from api.algorithm import split_availabilities_algorithm


class AllRegions(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(Store.REGION, status=status.HTTP_200_OK)


class AllAvailabilities(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request):
        fields_to_include = ['from_date', 'until_date', 'store', 'bike', 'availability_status']
        availabilities = Availability.objects.all()
        serializer = AvailabilitySerializer(availabilities, many=True, fields=fields_to_include)
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
            Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        fields_to_include = ['name', 'description', 'image_link']
        bike = Bike.objects.get(pk=bike_id)
        serializer = BikeSerializer(bike, many=False, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreByBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request, bike_id):
        fields_to_include = ['region', 'address', 'name']
        store = Bike.objects.get(pk=bike_id).store
        serializer = StoreSerializer(store, many=False, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailabilityOfBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request, bike_id):
        fields_to_include = ['from_date', 'until_date', 'availability_status']
        availability_of_bike = Availability.objects.filter(bike=Bike.objects.get(pk=bike_id))
        serializer = AvailabilitySerializer(availability_of_bike, many=True, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MakeBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, bike_id):
        user = self.request.user
        bike = Bike.objects.get(pk=bike_id)
        additional_data = {
            'user': user.pk,
            'bike': bike.pk,
        }
        data = {**request.data, **additional_data}
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            booking = serializer.save()
            booking.booking_status.set(Booking_Status.objects.filter(booking_status='B'))
            split_availabilities_algorithm(booking)
            # check if oidc user
            # check verification date against time now and if need to be check to adjust mail
            # adjustment: tell them to bring personal id
            # send email
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)