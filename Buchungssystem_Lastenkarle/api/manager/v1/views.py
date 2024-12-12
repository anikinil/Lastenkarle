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
from send_mail.views import send_bike_drop_off_confirmation
from send_mail.views import send_bike_pick_up_confirmation
from send_mail.views import send_user_warning_to_admins


class StoresOfManager(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsVerfied]

    def get(self, request):
        stores = set()
        for store in Store.objects.all():
            if store.store_flag in request.user.user_flags.all():
                stores.add(store)
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StorePage(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request, store_name):
        store = Store.objects.get(name=store_name)
        serializer = StoreSerializer(store, exclude=['store_flag'], many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, store_name):
        store = Store.objects.get(name=store_name)
        serializer = UpdateStoreSerializer(store, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EnrollUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def post(self, request, store_name):
        serializer = EnrollmentSerializer(data={'contact_data': request.data.get('contact_data', None), 'flag': 'Store: ' + store_name}, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=None, validated_data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class DeleteBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def delete(self, request, store_name, bike_id, *args, **kwargs):
        store = Store.objects.get(name=store_name)
        try:
            bike = Bike.objects.get(pk=bike_id, store=store)
        except ObjectDoesNotExist:
            raise Http404
        if Booking.objects.filter(bike=bike, booking_status__status='Picked up').exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for booking in Booking.objects.filter(bike=bike, booking_status__status='Booked'):
            booking.cancel_booking()
            send_cancellation_through_store_confirmation(booking)
        bike.delete()
        return Response(status=status.HTTP_200_OK)


class BikesOfStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, store_name):
        serializer = BikeSerializer(Bike.objects.filter(store=Store.objects.get(name=store_name)), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, store_name):
        store = Store.objects.get(name=store_name)
        data = {
            "store": store.name,
            "name": request.data.get('name', None),
            "description": request.data.get('description', None),
            "image": request.FILES.get('image', None)
        }
        serializer = BikeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        bike = serializer.save()
        Availability.create_availability(store, bike)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SelectedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request, store_name, bike_id):
        store = Store.objects.get(name=store_name)
        try:
            bike = Bike.objects.get(pk=bike_id, store=store)
        except ObjectDoesNotExist:
            raise Http404
        serializer = BikeSerializer(bike, exclude=['id', 'store'], many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateSelectedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]
    parser_classes = (MultiPartParser, FormParser)

    def patch(self, request, store_name, bike_id, *args, **kwargs):
        store = Store.objects.get(name=store_name)
        try:
            bike = Bike.objects.get(store=store, pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = UpdateBikeSerializer(instance=bike, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedBikeAddEquipment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def post(self, request, store_name, bike_id):
        try:
            bike = Bike.objects.get(pk=bike_id, store=Store.objects.get(name=store_name))
        except ObjectDoesNotExist:
            raise Http404
        equipment, created = Equipment.objects.get_or_create(equipment=request.data.get('equipment'))
        bike.bike_equipment.add(equipment.pk)
        return Response(status=status.HTTP_200_OK)


class SelectedBikeRemoveEquipment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def post(self, request, store_name, bike_id):
        try:
            bike = Bike.objects.get(pk=bike_id, store=Store.objects.get(name=store_name))
        except ObjectDoesNotExist:
            raise Http404
        serializer = RemoveEquipmentSerializer(data={'bike_id': bike.pk, 'equipment': request.data['equipment']})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class SelectedBikeAvailability(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request, store_name, bike_id):
        store = Store.objects.get(name=store_name)
        try:
            bike = Bike.objects.get(pk=bike_id, store=store)
            availabilities = Availability.objects.filter(bike=bike)
        except ObjectDoesNotExist:
            raise Http404
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingsOfStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request, store_name):
        store = Store.objects.get(name=store_name)
        serializer = BookingSerializer(Booking.objects.filter(bike__store=store), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedBookingOfStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request, store_name, booking_id):
        store = Store.objects.get(name=store_name)
        try:
            booking = Booking.objects.get(pk=booking_id, bike__store=store)
        except ObjectDoesNotExist:
            raise Http404
        serializer = BookingSerializer(booking, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, store_name, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, bike__store=Store.objects.get(name=store_name))
        except ObjectDoesNotExist:
            raise Http404
        if Booking_Status.objects.get(status='Booked') not in booking.booking_status.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        booking.cancel_booking()
        send_cancellation_through_store_confirmation(booking)
        merge_availabilities_algorithm(booking)
        return Response(status=status.HTTP_200_OK)


class CommentToBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def patch(self, request, store_name, booking_id, *args, **kwargs):
        try:
            booking = Booking.objects.get(pk=booking_id, bike__store=Store.objects.get(name=store_name))
        except ObjectDoesNotExist:
            raise Http404
        serializer = UpdateCommentOfBookingSerializer(booking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckLocalData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def get(self, request, store_name, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, bike__store=Store.objects.get(name=store_name))
            local_data = LocalData.objects.get(user=booking.user)
        except ObjectDoesNotExist:
            raise Http404
        serializer = LocalDataSerializer(local_data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, store_name, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, bike__store=Store.objects.get(name=store_name))
        except ObjectDoesNotExist:
            raise Http404
        if LocalData.objects.filter(user=booking.user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = LocalDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=booking.user, date_of_verification=datetime.now().date() + timedelta(days=180))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, store_name, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, bike__store=Store.objects.get(name=store_name))
            local_data = LocalData.objects.get(user=booking.user)
        except ObjectDoesNotExist:
            raise Http404
        serializer = LocalDataSerializer(local_data, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(date_of_verification=datetime.now().date() + timedelta(days=180))
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmBikeHandOut(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def post(self, request, store_name, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, bike__store=Store.objects.get(name=store_name))
        except ObjectDoesNotExist:
            raise Http404
        if Booking_Status.objects.get(status='Booked') not in booking.booking_status.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        booking.booking_status.remove(Booking_Status.objects.filter(status='Booked')[0].pk)
        booking.booking_status.add(Booking_Status.objects.filter(status='Picked up')[0].pk)
        booking.save()
        send_bike_pick_up_confirmation(booking)
        return Response(status=status.HTTP_200_OK)


class ConfirmBikeReturn(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def post(self, request, store_name, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, bike__store=Store.objects.get(name=store_name))
        except ObjectDoesNotExist:
            raise Http404
        if Booking_Status.objects.get(status='Picked up') not in booking.booking_status.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        booking.booking_status.remove(Booking_Status.objects.filter(status='Picked up')[0].pk)
        booking.booking_status.add(Booking_Status.objects.filter(status='Returned')[0].pk)
        booking.string = None
        booking.save()
        merge_availabilities_algorithm(booking)
        send_bike_drop_off_confirmation(booking)
        return Response(status=status.HTTP_200_OK)


class FindByQRString(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def get(self, request, store_name, qr_string):
        try:
            booking = Booking.objects.get(string=qr_string, bike__store=Store.objects.get(name=store_name))
        except ObjectDoesNotExist:
            raise Http404
        serializer = BookingSerializer(booking, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisteredEquipment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def get(self, request, store_name):
        equipment = Equipment.objects.all()
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReportComment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def post(self, request, store_name, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, bike__store=Store.objects.get(name=store_name))
            user = booking.user
        except ObjectDoesNotExist:
            raise Http404
        user.user_flags.add(User_Flag.objects.get(flag='Reminded'))
        send_user_warning_to_admins(booking)
        return Response(status=status.HTTP_200_OK)

