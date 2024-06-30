from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
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


class StorePage(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request):
        store = self.request.user.is_staff_of_store()
        serializer = StoreSerializer(store, many=False)
        serializer.exclude_fields(['store_flag'])
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        store = self.request.user.is_staff_of_store()
        serializer = UpdateStoreSerializer(store, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EnrollUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def post(self, request):
        contact_data = request.data['contact_data']
        try:
            user = User.objects.get(contact_data=contact_data)
        except ObjectDoesNotExist:
            raise Http404
        if user.is_staff_of_store() is None:
            store = self.request.user.is_staff_of_store()
            flag = store.store_flag
            user.user_flags.add(flag)
            user.is_staff = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def delete(self, request, bike_id, *args, **kwargs):
        store = self.request.user.is_staff_of_store()
        try:
            bike = Bike.objects.get(pk=bike_id, store=store)
        except ObjectDoesNotExist:
            raise Http404
        if Booking.objects.filter(bike=bike, booking_status__status='Picked up').exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for booking in Booking.objects.filter(bike=bike, booking_status__status='Booked'):
            booking.booking_status.clear()
            booking.booking_status.set(Booking_Status.objects.filter(status='Cancelled'))
            send_cancellation_through_store_confirmation(booking)
            booking.string = None
            booking.save()
        bike.delete()
        return Response(status=status.HTTP_200_OK)


class BikesOfStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        store = self.request.user.is_staff_of_store()
        bikes = Bike.objects.filter(store=store)
        fields_to_include = ['id', 'name', 'image', 'description', 'equipment']
        serializer = BikeSerializer(bikes, fields=fields_to_include, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        store = self.request.user.is_staff_of_store()
        data = {
            "store": store.pk,
            "name": request.data.get('name'),
            "description": request.data.get('description'),
            "image": request.FILES.get('image')
        }
        serializer = BikeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        bike = serializer.save()
        Availability.create_availability(store, bike)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SelectedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request, bike_id):
        store = self.request.user.is_staff_of_store()
        try:
            bike = Bike.objects.get(pk=bike_id, store=store)
        except ObjectDoesNotExist:
            raise Http404
        fields_to_include = ['name', 'image', 'description', 'equipment']
        serializer = BikeSerializer(bike, fields=fields_to_include, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateSelectedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]
    parser_classes = (MultiPartParser, FormParser)

    def patch(self, request, bike_id, *args, **kwargs):
        store = self.request.user.is_staff_of_store()
        try:
            bike = Bike.objects.get(store=store, pk=bike_id)
        except ObjectDoesNotExist:
            raise Http404
        serializer = UpdateBikeSerializer(instance=bike, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedBikeEquipment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def post(self, request, bike_id):
        store = self.request.user.is_staff_of_store()
        try:
            bike = Bike.objects.get(pk=bike_id, store=store)
        except ObjectDoesNotExist:
            raise Http404
        equipment = request.data['equipment']
        if Equipment.objects.filter(equipment=equipment).exists():
            bike.bike_equipment.add(Equipment.objects.get(equipment=equipment).pk)
            return Response(status=status.HTTP_200_OK)
        serializer = EquipmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_equipment = serializer.save()
        bike.bike_equipment.add(new_equipment.pk)
        bike.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, bike_id):
        store = self.request.user.is_staff_of_store()
        equipment = request.data['equipment']
        try:
            bike = Bike.objects.get(pk=bike_id, store=store)
            equipment_remove = Equipment.objects.get(equipment=equipment)
        except ObjectDoesNotExist:
            raise Http404
        if bike.bike_equipment.contains(equipment_remove):
            bike.bike_equipment.remove(equipment_remove)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SelectedBikeAvailability(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request, bike_id):
        store = self.request.user.is_staff_of_store()
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

    def get(self, request):
        store = self.request.user.is_staff_of_store()
        fields_to_include = ['id', 'preferred_username', 'bike', 'begin', 'end',
                             'comment', 'booking_status', 'equipment']
        bookings = Booking.objects.filter(bike__store=store)
        serializer = BookingSerializer(bookings, fields=fields_to_include, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelectedBookingOfStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff & IsAuthenticated & IsVerfied]

    def get(self, request, booking_id):
        store = self.request.user.is_staff_of_store()
        try:
            booking = Booking.objects.get(pk=booking_id, bike__store=store)
        except ObjectDoesNotExist:
            raise Http404
        fields_to_include = ['preferred_username', 'bike', 'begin', 'end',
                             'comment', 'booking_status', 'equipment']
        serializer = BookingSerializer(booking, fields=fields_to_include, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, booking_id):
        store = self.request.user.is_staff_of_store()
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
        send_cancellation_through_store_confirmation(booking)
        merge_availabilities_algorithm(booking)
        return Response(status=status.HTTP_200_OK)


class CommentToBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def patch(self, request, booking_id, *args, **kwargs):
        store = self.request.user.is_staff_of_store()
        fields_to_include = ['comment']
        try:
            booking = Booking.objects.get(pk=booking_id, bike__store=store)
        except ObjectDoesNotExist:
            raise Http404
        partialUpdateInputValidation(request, fields_to_include)
        serializer = BookingSerializer(booking, data=request.data, fields=fields_to_include, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckLocalData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id)
            local_data = LocalData.objects.get(user=booking.user)
        except ObjectDoesNotExist:
            raise Http404
        serializer = LocalDataSerializer(local_data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        if LocalData.objects.filter(user=booking.user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = LocalDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=booking.user, date_of_verification=datetime.now().date() + timedelta(days=180))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, booking_id):
        fields_to_include = ['first_name', 'last_name', 'address', 'id_number']
        try:
            booking = Booking.objects.get(pk=booking_id)
            local_data = LocalData.objects.get(user=booking.user)
        except ObjectDoesNotExist:
            raise Http404
        partialUpdateInputValidation(request, fields_to_include)
        serializer = LocalDataSerializer(local_data, data=request.data, fields=fields_to_include, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(date_of_verification=datetime.now().date() + timedelta(days=180))
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmBikeHandOut(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def post(self, request, booking_id):
        store = self.request.user.is_staff_of_store()
        try:
            booking = Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        if Booking_Status.objects.get(status='Booked') not in booking.booking_status.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        booking.booking_status.remove(Booking_Status.objects.get(status='Booked').pk)
        booking.booking_status.add(Booking_Status.objects.get(status='Picked up').pk)
        booking.save()
        send_bike_pick_up_confirmation(booking)
        return Response(status=status.HTTP_200_OK)


class ConfirmBikeReturn(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def post(self, request, booking_id):
        store = self.request.user.is_staff_of_store()
        try:
            booking = Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        if Booking_Status.objects.get(status='Picked up') not in booking.booking_status.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        booking.booking_status.remove(Booking_Status.objects.get(status='Picked up').pk)
        booking.booking_status.add(Booking_Status.objects.get(status='Returned').pk)
        booking.string = None
        booking.save()
        merge_availabilities_algorithm(booking)
        send_bike_drop_off_confirmation(booking)
        return Response(status=status.HTTP_200_OK)


class FindByQRString(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsStaff & IsVerfied]

    def get(self, request, qr_string):
        store = self.request.user.is_staff_of_store()
        fields_to_include = ['preferred_username', 'assurance_lvl', 'bike', 'begin', 'end',
                             'comment', 'booking_status', 'equipment', 'id']
        try:
            booking = Booking.objects.get(string=qr_string, bike__store=store)
        except ObjectDoesNotExist:
            raise Http404
        serializer = BookingSerializer(booking, fields=fields_to_include, many=False)
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
        store = self.request.user.is_staff_of_store()
        try:
            booking = Booking.objects.get(pk=booking_id)
            user = booking.user
        except ObjectDoesNotExist:
            raise Http404
        user.user_flags.add(User_Flag.objects.get(flag='Reminded'))
        send_user_warning_to_admins(booking)
        return Response(status=status.HTTP_200_OK)

