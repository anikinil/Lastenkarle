from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
        return Response(User_status.USER_STATUS_FLAG, status=status.HTTP_200_OK)


class EnrollUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated]

    def post(self, request):
        username = request.data['username']
        store = self.request.user.is_staff_of_store()
        flag_name = 'S' + str(store.pk)
        flag = User_status.objects.get(user_status=flag_name)
        user = User.objects.get(username=username)
        user.user_status.add(flag)
        user.is_staff = True
        user.save()
        return Response(status=status.HTTP_200_OK)




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

    # book for internal usages as store manager
    def post(self, request, bike_id):
        try:
            Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        store = self.request.user.is_staff_of_store()
        bike = Bike.objects.get(pk=bike_id)
        begin = request.data['from_date']
        end = request.data['until_date']
        if not merge_availabilities_from_until_algorithm(begin, end, store, bike):
            error_message = {'error': 'Please select a different time frame in which the bike is available'}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(pk=self.request.user.pk)
        booking_data = {
            'user': user.pk,
            'bike': bike.pk,
            'begin': begin,
            'end': end
        }
        data = {**booking_data}
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            booking = serializer.save()
            booking.booking_status.add(Booking_Status.objects.get(booking_status='I').pk)
            booking.save()
            split_availabilities_algorithm(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        store = self.request.user.is_staff_of_store()
        bookings = Booking.objects.get(pk=booking_id, bike__store=store)
        fields_to_include = ['user', 'bike', 'begin', 'end', 'booking_status']
        serializer = BookingSerializer(bookings, many=False, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #cancel booking
    def post(self, request, booking_id):
        store = self.request.user.is_staff_of_store()
        try:
            Booking.objects.get(pk=booking_id, bike__store=store)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id, bike__store=store)
        booking.booking_status.clear()
        booking.booking_status.set(Booking_Status.objects.filter(booking_status='C'))
        booking.string = None
        booking.save()
        merge_availabilities_algorithm(booking)
        return Response(status=status.HTTP_200_OK)


class CommentToBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff]

    def get(self, request, booking_id):
        store = self.request.user.is_staff_of_store()
        if not Comment.objects.filter(store=store, booking_id=booking_id).exists():
            error_message = {'error': 'Booking has no associated comment'}
            return Response(error_message, status=status.HTTP_404_NOT_FOUND)
        fields_to_include = ['content']
        comment = Comment.objects.get(store=store, booking_id=booking_id)
        serializer = CommentSerializer(comment, fields=fields_to_include, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, booking_id):
        store = self.request.user.is_staff_of_store()
        additional_data = {
            'store': store.pk,
            'booking': booking_id,
        }
        data = {**request.data, **additional_data}
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, booking_id, *args, **kwargs):
        store = self.request.user.is_staff_of_store()
        fields_to_include = ['content']
        instance = Comment.objects.get(store=store, booking_id=booking_id)
        serializer = CommentSerializer(instance, data=request.data, fields=fields_to_include, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckLocalData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff]

    def get(self, request, booking_id):
        try:
            Booking.objects.filter(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id)
        if not LocalData.objects.filter(user=booking.user).exists():
            error_message = {'error': 'User has no associated local data'}
            return Response(error_message,status=status.HTTP_404_NOT_FOUND)
        localdata = LocalData.objects.get(user=booking.user)
        serializer = LocalDataSerializer(localdata, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id)
        user = booking.user
        serializer = LocalDataSerializer(data=request.data)
        if serializer.is_valid():
            local_data = serializer.save()
            local_data.user = user
            local_data.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id)
        instance = LocalData.objects.get(user=booking.user)
        serializer = UpdateLocalDataSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmBikeHandOut(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff]

    def get(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id)
        serializer = BookingConfirmationSerializer(booking, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id)
        if not booking.booking_status.contains(Booking_Status.objects.get(booking_status='P')):
            booking.booking_status.add(Booking_Status.objects.get(booking_status='P').pk)
        if booking.booking_status.contains(Booking_Status.objects.get(booking_status='P')):
            booking.booking_status.remove(Booking_Status.objects.get(booking_status='P').pk)
            booking.booking_status.add(Booking_Status.objects.get(booking_status='R').pk)
            booking.string = None
        return Response(status=status.HTTP_200_OK)


class FindByQRString(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff]

    def get(self, request, qr_string):
        booking = Booking.objects.get(string=qr_string)
        fields_to_include = ['id']
        serializer = BookingSerializer(booking, many=False, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)


### FEHLT: REPORT FUNKTION VON COMMENTS AUS