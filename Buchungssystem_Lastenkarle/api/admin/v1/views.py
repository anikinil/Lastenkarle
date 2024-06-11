from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.http import QueryDict
import logging

from api.algorithm import *
from api.permissions import *
from api.serializer import *
from db_model.models import *
from send_mail.views import send_cancellation_through_store_confirmation
from send_mail.views import send_banned_mail_to_user


class AllUserFlags(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request):
        flags = User_Flag.objects.all()
        serializer = UserFlagSerializer(flags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=None, validated_data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class AllUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request):
        users = User.objects.all()
        fields_to_include = ['id', 'user_status', 'assurance_lvl', 'year_of_birth',
                             'contact_data', 'username', 'preferred_username']
        serializer = UserSerializer(users, fields=fields_to_include, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            raise Http404
        fields_to_include = ['user_status', 'assurance_lvl', 'year_of_birth',
                             'contact_data', 'username', 'preferred_username']
        serializer = UserSerializer(user, fields=fields_to_include, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllBookingsOfUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            raise Http404
        bookings = Booking.objects.filter(user=user)
        fields_to_include = ['preferred_username', 'assurance_lvl', 'bike', 'begin', 'end',
                             'comment', 'booking_status', 'equipment', 'id']
        serializer = BookingSerializer(bookings, fields=fields_to_include, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllBookings(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request):
        bookings = Booking.objects.all()
        fields_to_include = ['preferred_username', 'assurance_lvl', 'bike', 'begin', 'end',
                             'comment', 'booking_status', 'equipment', 'id']
        serializer = BookingSerializer(bookings, fields=fields_to_include, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = BookingSerializer(booking, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        if not booking.booking_status.contains(Booking_Status.objects.get(status='Booked')):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        booking.booking_status.clear()
        booking.booking_status.set(Booking_Status.objects.filter(status='Cancelled'))
        booking.string = None
        booking.save()
        merge_availabilities_algorithm(booking)
       # send_cancellation_through_store_confirmation(booking)
        return Response(status=status.HTTP_200_OK)


class AddBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, store_id):
        try:
            store = Store.objects.get(pk=store_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = BikeCreationSerializer(data=request.data, context={'store': store})
        serializer.is_valid(raise_exception=True)
        bike = serializer.save()
        Availability.create_availability(store, bike)
        return Response(serializer.data,  status=status.HTTP_201_CREATED)


class DeleteBike(DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def delete(self, request, bike_id, *args, **kwargs):
        try:
            bike = Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        if Booking.objects.filter(bike=bike, booking_status__status='Picked up').exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for booking in Booking.objects.filter(bike=bike, booking_status__status='Booked'):
            booking.booking_status.clear()
            booking.booking_status.set(Booking_Status.objects.filter(status='Cancelled'))
#            send_cancellation_through_store_confirmation(booking)
            booking.string = None
            booking.save()
        bike.delete()
        return Response(status=status.HTTP_200_OK)


class AllBikes(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request):
        bikes = Bike.objects.all()
        serializer = BikeSerializer(bikes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, bike_id):
        try:
            bike = Bike.objects.get(pk=bike_id)
        except Bike.DoesNotExist:
            raise Http404
        serializer = BikeSerializer(bike, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateSelectedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]
    parser_classes = (MultiPartParser, FormParser)

    def patch(self, request, bike_id, *args, **kwargs):
        try:
            bike = Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = UpdateBikeSerializer(instance=bike, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EquipmentOfBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def post(self, request, bike_id):
        try:
            bike = Bike.objects.get(pk=bike_id)
        except Bike.DoesNotExist:
            raise Http404
        equipment = request.data['equipment']
        if Equipment.objects.filter(equipment=equipment).exists():
            if bike.bike_equipment.filter(equipment=equipment).exists():
                return Response(status=status.HTTP_200_OK)
            bike.bike_equipment.add(Equipment.objects.get(equipment=equipment).pk)
            return Response(status=status.HTTP_200_OK)
        serializer = EquipmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_equipment = serializer.save()
        bike.bike_equipment.add(new_equipment.pk)
        bike.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, bike_id):
        try:
            bike = Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404

        equipment = request.data['equipment']
        if not Equipment.objects.filter(equipment=equipment).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not bike.bike_equipment.contains(Equipment.objects.get(equipment=equipment)):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        bike.bike_equipment.remove(Equipment.objects.get(equipment=equipment))
        return Response(status=status.HTTP_200_OK)


class RegisteredEquipment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request):
        equipment = Equipment.objects.all()
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailabilityOfBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, bike_id):
        try:
            bike = Bike.objects.get(pk=bike_id)
            availability = Availability.objects.filter(bike=bike)
        except ObjectDoesNotExist:
            raise Http404
        serializer = AvailabilitySerializer(availability, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        store = serializer.save()
        store_flag = User_Flag.custom_create_store_flags(store)
        store.store_flag = store_flag
        store.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteStore(DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def delete(self, request, store_id, *args, **kwargs):
        try:
            store = Store.objects.get(pk=store_id)
        except ObjectDoesNotExist:
            raise Http404
        if Booking.objects.filter(bike__store=store, booking_status__status='Picked up').exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for booking in Booking.objects.filter(bike__store=store, booking_status__status='Booked'):
            booking.booking_status.clear()
            booking.booking_status.set(Booking_Status.objects.filter(status='Cancelled'))
#            send_cancellation_through_store_confirmation(booking)
            booking.string = None
            booking.save()
        store.delete()
        return Response(status=status.HTTP_200_OK)


class AllStores(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, store_id):
        try:
            store = Store.objects.get(pk=store_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = StoreSerializer(store, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateSelectedStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def patch(self, request, store_id, *args, **kwargs):
        try:
            store = Store.objects.get(pk=store_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = UpdateStoreSerializer(store, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailabilityOfBikesFromStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, store_id):
        try:
            store = Store.objects.get(pk=store_id)
            availabilities = Availability.objects.filter(store=store)
        except ObjectDoesNotExist:
            raise Http404
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BanUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def post(self, request):
        serializer = BanningSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.update(instance=None, validated_data=serializer.validated_data)
        send_banned_mail_to_user(user)
        return Response(status=status.HTTP_200_OK)

