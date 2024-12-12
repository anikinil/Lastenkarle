from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import FormParser, MultiPartParser
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
from send_mail.views import send_cancellation_through_store_confirmation
from send_mail.views import send_banned_mail_to_user


class AllUserFlags(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request):
        serializer = UserFlagSerializer(User_Flag.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data, context={'user': self.request.user})
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=None, validated_data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class AllUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request):
        serializer = UserSerializer(User.objects.all(), many=True)
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
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = BookingSerializer(Booking.objects.filter(user=user), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllBookings(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request):
        serializer = BookingSerializer(Booking.objects.all(), many=True)
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
        booking.cancel_booking()
        merge_availabilities_algorithm(booking)
        send_cancellation_through_store_confirmation(booking)
        return Response(status=status.HTTP_200_OK)


class AddBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, store_name):
        try:
            store = Store.objects.get(name=store_name)
        except ObjectDoesNotExist:
            raise Http404
        serializer = BikeCreationSerializer(data=request.data, context={'store': store})
        serializer.is_valid(raise_exception=True)
        bike = serializer.save()
        Availability.create_availability(store, bike)
        return Response(serializer.data,  status=status.HTTP_201_CREATED)


class DeleteBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def delete(self, request, bike_id):
        try:
            bike = Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        if Booking.objects.filter(bike=bike, booking_status__status='Picked up').exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for booking in Booking.objects.filter(bike=bike, booking_status__status='Booked'):
            booking.cancel_booking()
            send_cancellation_through_store_confirmation(booking)
        bike.delete()
        return Response(status=status.HTTP_200_OK)


class AllBikes(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request):
        serializer = BikeSerializer(Bike.objects.all(), many=True)
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

    def patch(self, request, bike_id):
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
        except ObjectDoesNotExist:
            raise Http404
        equipment, created = Equipment.objects.get_or_create(equipment=request.data['equipment'])
        if equipment in bike.bike_equipment.all():
            return Response('Can\'t add same equipment multiple times', status=status.HTTP_400_BAD_REQUEST)
        bike.bike_equipment.add(equipment.pk)
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
        serializer = EquipmentSerializer(Equipment.objects.all(), many=True)
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
        serializer = CreateStoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        store = serializer.save()
        store_flag = User_Flag.custom_create_store_flags(store)
        store.store_flag = store_flag
        store.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def delete(self, request, store_name):
        try:
            store = Store.objects.get(name=store_name)
        except ObjectDoesNotExist:
            raise Http404
        if Booking.objects.filter(bike__store=store, booking_status__status='Picked up').exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for booking in Booking.objects.filter(bike__store=store, booking_status__status='Booked'):
            booking.cancel_booking()
            send_cancellation_through_store_confirmation(booking)
        store.delete()
        return Response(status=status.HTTP_200_OK)


class AllStores(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request):
        serializer = StoreSerializer(Store.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, store_name):
        try:
            store = Store.objects.get(name=store_name)
        except ObjectDoesNotExist:
            raise Http404
        serializer = StoreSerializer(store, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateSelectedStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def patch(self, request, store_name, *args, **kwargs):
        try:
            store = Store.objects.get(name=store_name)
        except ObjectDoesNotExist:
            raise Http404
        serializer = UpdateStoreSerializer(store, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailabilityOfBikesFromStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, store_name):
        try:
            store = Store.objects.get(name=store_name)
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
        serializer.save()
        send_banned_mail_to_user(User.objects.get(contact_data=request.data.get('contact_data')))
        return Response(status=status.HTTP_200_OK)


class BikesOfStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser & IsVerfied]

    def get(self, request, store_name):
        serializer = BikeSerializer(Bike.objects.filter(store=Store.objects.get(name=store_name)), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)