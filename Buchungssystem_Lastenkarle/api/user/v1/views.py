from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import *
from authlib.integrations.django_client import OAuth
from django.http import Http404
from api.permissions import IsStaff, IsSuperUser

from api.serializer import *
from db_model.models import *

#oauth = OAuth()
#print("Das Ding ist:")
#print(oauth.helmholtz)

class RegistrateUser(CreateAPIView):
    queryset = LoginData.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)


class UpdateLoginData(RetrieveUpdateAPIView):
    queryset = LoginData.objects.all()
    serializer_class = UpdateLoginDataSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class UpdateLocalData(RetrieveUpdateAPIView):
    queryset = LocalData.objects.all()
    serializer_class = UpdateLocalDataSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class UpdateUserData(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


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


class AllBookingsFromUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user_id=request.user.pk)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingFromUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id)
        serializer = BookingSerializer(booking, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id).bike
        except ObjectDoesNotExist:
            raise Http404
        bike = Booking.objects.get(pk=booking_id).bike
        serializer = BikeSerializer(bike, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreOfBookedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id).bike.store
        except ObjectDoesNotExist:
            raise Http404
        store = Booking.objects.get(pk=booking_id).bike.store
        serializer = StoreSerializer(store, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LocalDataOfUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            LocalData.objects.get(user=request.user)
        except ObjectDoesNotExist:
            raise Http404
        local_data = LocalData.objects.get(user=request.user)
        serializer = LocalDataSerializer(local_data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
