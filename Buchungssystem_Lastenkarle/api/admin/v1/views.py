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
from api.configs.ConfigFunctions import *


class AllUserFlags(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request):
        user_status = User_Status.objects.all()
        serializer = UserStatusSerializer(user_status, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        contact_data = request.data['contact_data']
        user_flag = request.data['user_status']
        user = User.objects.get(contact_data=contact_data)
        user.user_status.add(User_Status.objects.get(user_status=user_flag).pk)
        if user_flag.startswith("Store:"):
            user.is_staff = True
            user.save()
        return Response(status=status.HTTP_202_ACCEPTED)


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
        booking = Booking.objects.get(pk=booking_id)
        booking.booking_status.clear()
        booking.booking_status.set(Booking_Status.objects.filter(booking_status='Cancelled'))
        booking.string = None
        booking.save()
        merge_availabilities_algorithm(booking)
        #TODO: cancellation throught store confirmation mail call
        return Response(status=status.HTTP_202_ACCEPTED)


class CommentOfBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request, booking_id):
        if not Comment.objects.filter(booking_id=booking_id).exists():
            raise Http404
        comment = Comment.objects.get(booking_id=booking_id)
        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def post(self, request, store_id):
        additional_data = {
            'store': store_id,
        }
        data = {**request.data, **additional_data}
        serializer = BikeSerializer(data=data)
        if serializer.is_valid():
            bike = serializer.save()
            store = Store.objects.get(pk=store_id)
            Availability.create_availability(store, bike)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteBike(DestroyAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def perform_destroy(self, instance):
        instance.delete()


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


class UpdateSelectedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def patch(self, request, bike_id, *args, **kwargs):
        instance = Bike.objects.get(pk=bike_id)
        serializer = BikeSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EquipmentOfBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def post(self, request, bike_id):
        bike = Bike.objects.get(pk=bike_id)
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


class RegisteredEquipment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request):
        equipment = Equipment.objects.all()
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailabilityOfBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request, bike_id):
        availability = Availability.objects.filter(bike_id=bike_id)
        serializer = AvailabilitySerializer(availability, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            store = serializer.save()
            store_flag = User_Status.custom_create_store_flags(store)
            store.store_flag = store_flag
            store.save()
            add_store(store.name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteStore(DestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def perform_destroy(self, instance):
        instance.delete()


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


class UpdateSelectedStore(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def patch(self, request, store_id, *args, **kwargs):
        instance = Store.objects.get(pk=store_id)
        serializer = StoreSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
        user.user_status.add(User_Status.objects.get(user_status='Banned').pk)
        user.is_active = False
        user.save()
        #TODO: User banned mail call
        return Response(status=status.HTTP_202_ACCEPTED)


class AllStoreConfigurations(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request):
        return Response(getAllStoresConfig(), status=status.HTTP_200_OK)


class SelectedStoreConfiguration(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsSuperUser]

    def get(self, request, store_id):
        store = Store.objects.get(pk=store_id)
        return Response(getStoreConfig(store.name), status=status.HTTP_200_OK)

    def patch(self, request, store_id):
        store = Store.objects.get(pk=store_id)
        update_store_config(store.name, request.data)
        return Response(getStoreConfig(store.name), status=status.HTTP_200_OK)