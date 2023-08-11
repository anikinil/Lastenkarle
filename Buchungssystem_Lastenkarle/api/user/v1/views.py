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

from api.algorithm import merge_availabilities_algorithm
from api.serializer import *
from db_model.models import *


class RegistrateUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)


class UpdateUserData(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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

    # gets all bookings of the user if none it is an empty list
    def get(self, request):
        fields_to_include = ['begin', 'end', 'booking_status']
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingFromUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # get the booking details as the customer
    def get(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        fields_to_include = ['id', 'begin', 'end', 'booking_status']
        booking = Booking.objects.get(pk=booking_id)
        serializer = BookingSerializer(booking, many=False, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # cancel booking as the customer -> changes booking status flag
    def post(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id)
        booking.booking_status.clear()
        booking.booking_status.add(Booking_Status.objects.get(booking_status='C'))
        booking.string = None
        booking.save()
        merge_availabilities_algorithm(booking)
        return Response(status=status.HTTP_200_OK)


class BookedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id).bike
        except ObjectDoesNotExist:
            raise Http404
        fields_to_include = ['id', 'name', 'description', 'image_link']
        bike = Booking.objects.get(pk=booking_id).bike
        serializer = BikeSerializer(bike, many=False, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreOfBookedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id).bike.store
        except ObjectDoesNotExist:
            raise Http404
        fields_to_include = ['region', 'address', 'name']
        store = Booking.objects.get(pk=booking_id).bike.store
        serializer = StoreSerializer(store, many=False, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDataOfUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            User.objects.get(pk=self.request.user.pk)
        except ObjectDoesNotExist:
            raise Http404
        data = User.objects.get(pk=self.request.user.pk)
        serializer = UserSerializer(data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)



class DeleteUserAccount(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        if LocalData.objects.filter(user=user).exists():
            LocalData.objects.get(user=user).anonymize().save()
        user.anonymize().save()
        return Response(status=status.HTTP_200_OK)