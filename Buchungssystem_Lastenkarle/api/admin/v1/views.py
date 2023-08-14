from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from api.algorithm import *
from api.permissions import *
from api.serializer import *
from db_model.models import *


class AllUserFlags(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request):
        return Response(User_status.USER_STATUS_FLAG, status=status.HTTP_200_OK)

    def post(self, request):
        contact_data = request.data['contact_data']
        user_flag = request.data['user_status']
        user = User.objects.get(contact_data=contact_data)
        user.user_status.add(User_status.objects.get(user_status=user_flag).pk)
        return Response(status=status.HTTP_200_OK)


class AllUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllBookingsOfUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request, user_id):
        bookings = Booking.objects.filter(user_id=user_id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllBookings(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request):
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request, booking_id):
        bookings = Booking.objects.get(pk=booking_id)
        serializer = BookingSerializer(bookings, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, booking_id):
        if not Booking.objects.filter(pk=booking_id).exists():

            return Response(status=status.HTTP_400_BAD_REQUEST)
        booking = Booking.objects.get(pk=booking_id)
        booking.booking_status.clear()
        booking.booking_status.set(Booking_Status.objects.filter(booking_status='C'))
        booking.string = None
        booking.save()
        merge_availabilities_algorithm(booking)
        return Response(status=status.HTTP_200_OK)


class CommentOfBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request, booking_id):
        if not Comment.objects.filter(booking_id=booking_id).exists():

            return Response(status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.get(booking_id=booking_id)
        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllBikes(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request):
        bikes = Bike.objects.all()
        serializer = BikeSerializer(bikes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request, bike_id):
        bike = Bike.objects.get(pk=bike_id)
        serializer = BikeSerializer(bike, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailabilityOfBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request, bike_id):
        availability = Availability.objects.filter(bike_id=bike_id)
        serializer = AvailabilitySerializer(availability, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllStores(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request, store_id):
        store = Store.objects.get(pk=store_id)
        serializer = StoreSerializer(store, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailabilityOfBikesFromStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request, store_id):
        store = Store.objects.get(pk=store_id)
        availabilities = Availability.objects.filter(store=store)
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BanUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def post(self, request):
        contact_data = request.data['contact_data']
        user = User.objects.get(contact_data=contact_data)
        user.user_status.add(User_status.objects.get(user_status='B').pk)
        user.is_active = False
        return Response(status=status.HTTP_200_OK)