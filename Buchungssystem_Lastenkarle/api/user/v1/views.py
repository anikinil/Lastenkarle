from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView

from api.serializer import *
from db_model.models import *


class RegistrateUser(CreateAPIView):
    queryset = LoginData.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)


class UpdateLoginData(RetrieveUpdateAPIView):
    queryset = LoginData.objects.all()
    serializer_class = UpdateLoginDataSerializer


class UpdateLocalData(RetrieveUpdateAPIView):
    queryset = LocalData.objects.all()
    serializer_class = UpdateLocalDataSerializer


class UpdateUserData(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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

class UserStatusView(APIView):

    def post(self, request):
        serializer = UserStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        user_data = LocalData.objects.get(user=User.objects.get(pk=user_id))
        serializer = UserFlagSerializer(user_data, many=False)
        return Response(serializer.data)
