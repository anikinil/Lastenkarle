from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

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
        user_status = User_Status.objects.all()
        serializer = UserStatusSerializer(user_status, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        contact_data = request.data['contact_data']
        user_flag = request.data['user_status']
        try:
            user = User.objects.get(contact_data=contact_data)
            User_Status.objects.get(user_status=user_flag)
        except ObjectDoesNotExist:
            raise Http404
        user.user_status.add(User_Status.objects.get(user_status=user_flag).pk)
        if user_flag.startswith("Store:"):
            user.is_staff = True
            user.save()
        return Response(status=status.HTTP_200_OK)


class AllUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllBookingsOfUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, user_id):
        try:
            bookings = Booking.objects.filter(user_id=user_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllBookings(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request):
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
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
        booking.booking_status.clear()
        booking.booking_status.set(Booking_Status.objects.filter(booking_status='Cancelled'))
        booking.string = None
        booking.save()
        merge_availabilities_algorithm(booking)
        send_cancellation_through_store_confirmation(booking)
        return Response(status=status.HTTP_202_ACCEPTED)


class CommentOfBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = BookingSerializer(booking, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, store_id):
        try:
            store = Store.objects.get(pk=store_id)
        except ObjectDoesNotExist:
            raise Http404
        bike = Bike.create_bike(store, **request.data)
        Availability.create_availability(store, bike)
        serializer = BikeSerializer(bike, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteBike(DestroyAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def perform_destroy(self, instance):
        instance.delete()


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
            instance = Bike.objects.get(pk=bike_id)
        except Bike.DoesNotExist:
            raise Http404
        serializer = BikeSerializer(instance, data=request.data, partial=True)
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
            if bike.equipment.filter(equipment=equipment).exists():
                return Response(status=status.HTTP_200_OK)
            bike.equipment.add(Equipment.objects.get(equipment=equipment).pk)
            return Response(status=status.HTTP_200_OK)
        serializer = EquipmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_equipment = serializer.save()
        bike.equipment.add(new_equipment.pk)
        bike.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
            bike = Store.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        availability = Availability.objects.filter(bike=bike)
        serializer = AvailabilitySerializer(availability, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            store = serializer.save()
            store_flag = User_Status.custom_create_store_flags(store)
            store.store_flag = store_flag
            store.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteStore(DestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def perform_destroy(self, instance):
        instance.delete()


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
            instance = Store.objects.get(pk=store_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = StoreSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailabilityOfBikesFromStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, store_id):
        try:
            store = Store.objects.get(pk=store_id)
        except ObjectDoesNotExist:
            raise Http404
        availabilities = Availability.objects.filter(store=store)
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BanUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def post(self, request):
        contact_data = request.data.get('contact_data')
        try:
            user = User.objects.get(contact_data=contact_data)
        except ObjectDoesNotExist:
            raise Http404
        user_status_banned = User_Status.objects.get(user_status='Banned')
        user.user_status.add(user_status_banned)
        user.is_active = False
        user.save()
        send_banned_mail_to_user(user)
        return Response(status=status.HTTP_200_OK)

