from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import *
from django.http import Http404

from api.algorithm import *
from api.permissions import *
from api.serializer import *
from db_model.models import *
from send_mail.views import send_booking_confirmation
from send_mail.views import send_cancellation_through_store_confirmation
from send_mail.views import send_bike_drop_off_confirmation
from send_mail.views import send_bike_pick_up_confirmation
from send_mail.views import send_user_warning_to_admins
from send_mail.views import send_user_warning


class AllUserFlags(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request):
        store = self.request.user.is_staff_of_store()
        serializer = UserStatusSerializer(store.store_flag, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StorePage(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request):
        store = self.request.user.is_staff_of_store()
        serializer = StoreSerializer(store, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        store = self.request.user.is_staff_of_store()
        instance = store
        serializer = StoreSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EnrollUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def post(self, request):
        contact_data = request.data['contact_data']
        store = self.request.user.is_staff_of_store()
        flag = store.store_flag
        user = User.objects.get(contact_data=contact_data)
        user.user_status.add(flag)
        user.is_staff = True
        user.save()
        return Response(status=status.HTTP_202_ACCEPTED)


class DeleteBike(DestroyAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def perform_destroy(self, instance):
        instance.delete()


class BikesOfStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request):
        store = self.request.user.is_staff_of_store()
        bikes = Bike.objects.filter(store=store)
        serializer = BikeSerializer(bikes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        store = self.request.user.is_staff_of_store()
        additional_data = {
            'store': store.pk,
        }
        data = {**request.data, **additional_data}
        serializer = BikeSerializer(data=data)
        if serializer.is_valid():
            bike = serializer.save()
            Availability.create_availability(store, bike)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SelectedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request, bike_id):
        try:
            Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        store = self.request.user.is_staff_of_store()
        bike = Bike.objects.get(pk=bike_id, store=store)
        serializer = BikeSerializer(bike, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MakeInternalBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

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
            'bike': bike.pk,
            'begin': begin,
            'end': end
        }
        data = {**booking_data, **request.data}
        serializer = MakeBookingSerializer(data=data)
        if serializer.is_valid():
            booking = serializer.save(user=user)
            booking.booking_status.add(Booking_Status.objects.get(booking_status='Internal usage').pk)
            booking_string = generate_random_string(5)
            booking.string = booking_string
            booking.save()
            split_availabilities_algorithm(booking)
            send_booking_confirmation(booking)
            serializer = BookingSerializer(booking, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateSelectedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def patch(self, request, bike_id, *args, **kwargs):
        store = self.request.user.is_staff_of_store()
        instance = Bike.objects.get(store=store, pk=bike_id)
        serializer = BikeSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedBikeEquipment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def post(self, request,bike_id):
        store = self.request.user.is_staff_of_store()
        bike = Bike.objects.get(pk=bike_id, store=store)
        equipment = request.data['equipment']
        if Equipment.objects.filter(equipment=equipment).exists():
            bike.equipment.add(Equipment.objects.get(equipment=equipment).pk)
            return Response(status=status.HTTP_202_ACCEPTED)
        serializer = EquipmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_equipment = serializer.save()
        bike.equipment.add(new_equipment.pk)
        bike.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SelectedBikeAvailability(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request, bike_id):
        try:
            Bike.objects.get(pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        store = self.request.user.is_staff_of_store()
        availabilities = Availability.objects.filter(bike_id=bike_id, store=store)
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingsOfStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request):
        store = self.request.user.is_staff_of_store()
        bookings = Booking.objects.filter(bike__store=store)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedBookingOfStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request, booking_id):
        store = self.request.user.is_staff_of_store()
        bookings = Booking.objects.get(pk=booking_id, bike__store=store)
        serializer = BookingSerializer(bookings, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, booking_id):
        store = self.request.user.is_staff_of_store()
        try:
            Booking.objects.get(pk=booking_id, bike__store=store)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id, bike__store=store)
        booking.booking_status.clear()
        booking.booking_status.set(Booking_Status.objects.filter(booking_status='Cancelled'))
        booking.string = None
        booking.save()
        send_cancellation_through_store_confirmation(booking)
        merge_availabilities_algorithm(booking)
        return Response(status=status.HTTP_202_ACCEPTED)


class CommentToBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def get(self, request, booking_id):
        store = self.request.user.is_staff_of_store()
        booking = Booking.objects.get(pk=booking_id)
        serializer = BookingSerializer(booking, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, booking_id, *args, **kwargs):
        instance = Booking.objects.get(pk=booking_id)
        serializer = BookingSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckLocalData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def get(self, request, booking_id):
        try:
            Booking.objects.filter(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id)
        if not LocalData.objects.filter(user=booking.user).exists():
            error_message = {'error': 'User has no associated local data'}
            return Response(error_message,status=status.HTTP_404_NOT_FOUND)
        local_data = LocalData.objects.get(user=booking.user)
        serializer = LocalDataSerializer(local_data, many=False)
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
        serializer = LocalDataSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmBikeHandOut(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]


    def post(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id)
        booking.booking_status.remove(Booking_Status.objects.get(booking_status='Booked').pk)
        booking.booking_status.add(Booking_Status.objects.get(booking_status='Picked up').pk)
        #TODO: bike pick up confirmation call
        return Response(status=status.HTTP_202_ACCEPTED)

class ConfirmBikeReturn(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def post(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id)
        booking.booking_status.remove(Booking_Status.objects.get(booking_status='Picked up').pk)
        booking.booking_status.add(Booking_Status.objects.get(booking_status='Returned').pk)
        booking.string = None
        merge_availabilities_algorithm(booking)
        # TODO: bike drop of confirmation call
        return Response(status=status.HTTP_202_ACCEPTED)

class FindByQRString(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def get(self, request, qr_string):
        booking = Booking.objects.get(string=qr_string)
        serializer = BookingSerializer(booking, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisteredEquipment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def get(self, request):
        equipment = Equipment.objects.all()
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReportComment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def post(self, request, booking_id):
        booking = Booking.objects.get(pk=booking_id)
        store = self.request.user.is_staff_of_store()
        send_user_warning_to_admins(booking)
        send_user_warning(booking)
        return Response(status=status.HTTP_202_ACCEPTED)
