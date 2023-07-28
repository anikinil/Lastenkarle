from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from rest_framework.authentication import BasicAuthentication

from knox.views import LoginView as KnoxLoginView

from api.serializer import *
from db_model.models import *


class RegistrateUser(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)


class UpdateUserData(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserDataSerializer


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super(LoginView, self).post(request, format=None)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response.data, status=status.HTTP_200_OK)


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
        user_data = ID_Data.objects.get(user=UserI.objects.get(pk=user_id))
        serializer = UserFlagSerializer(user_data, many=False)
        return Response(serializer.data)
