from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import *
from authlib.integrations.django_client import OAuth
from django.http import Http404

from api.algorithm import merge_availabilities_algorithm
from api.serializer import *
from db_model.models import *

from Buchungssystem_Lastenkarle.settings import CANONICAL_HOST
from send_mail.views import send_banned_mail_to_user
from send_mail.views import send_user_registered_confirmation
from send_mail.views import send_cancellation_confirmation
from send_mail.views import send_user_changed_mail
from send_mail.views import send_user_registered_confirmation

oauth = OAuth()

oauth.register(name="helmholtz")


class HelmholtzLoginView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        redirect_uri = CANONICAL_HOST + '/api/user/v1/helmholtz/auth'
        return oauth.helmholtz.authorize_redirect(request, redirect_uri)


class HelmholtzAuthView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            token = oauth.helmholtz.authorize_access_token(request)
            userinfo = oauth.helmholtz.userinfo(request=request, token=token)
        except ObjectDoesNotExist:
            raise Http404
        if User.objects.filter(username=userinfo['eduperson_unique_id']).exists() is False:
            user = User.objects.create_helmholtz_user(userinfo)
        else:
            user = User.objects.filter(username=userinfo['eduperson_unique_id']).first()
            user = User.objects.update_helmholtz_user(user, userinfo)
        login(request, user)
        response = super(HelmholtzAuthView, self).post(request, format=None)
        return Response(response.data, status=status.HTTP_200_OK)


class RegistrateUser(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_user_registered_confirmation(user)
        return Response(status=status.HTTP_201_CREATED)


class ConfirmEmail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def post(self, request, user_id, verification_string):
        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            raise Http404
        if User.objects.filter(pk=user_id, verification_string=verification_string).exists():
            user.user_status.add(User_Status.objects.get(user_status='Verified'))
            user.verification_string = None
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateUserData(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        fields_to_include = ['contact_data', 'username', 'password']
        partialUpdateInputValidation(request, fields_to_include)
        serializer = UserSerializer(self.request.user, data=request.data, fields=fields_to_include, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if serializer.validated_data.get('contact_data', None) is not None:
            user.user_status.remove(User_Status.objects.get(user_status='Verified'))
            user.verification_string = generate_random_string(30)
            user.save()
            send_user_changed_mail(user)
        if serializer.validated_data.get('password', None) is not None:
            user.set_password(user.password)
            user.save()
        data = UserSerializer(user, many=False, fields=['contact_data', 'username']).data
        return Response(data, status=status.HTTP_200_OK)


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        response = super(LoginView, self).post(request, format=None)
        return Response({'token': response.data.get('token')}, status=status.HTTP_200_OK)


class AllBookingsFromUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fields_to_include = ['id', 'bike', 'begin', 'end', 'booking_status', 'equipment']
        bookings = Booking.objects.filter(user=self.request.user)
        serializer = BookingSerializer(bookings, fields=fields_to_include, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingFromUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, user=request.user)
        except ObjectDoesNotExist:
            raise Http404
        fields_to_include = ['id', 'bike', 'begin', 'end', 'booking_status', 'equipment']
        serializer = BookingSerializer(booking, fields=fields_to_include, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, user=request.user)
        except ObjectDoesNotExist:
            raise Http404
        if not booking.booking_status.contains(Booking_Status.objects.get(booking_status='Booked')):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        booking.booking_status.clear()
        booking.booking_status.add(Booking_Status.objects.get(booking_status='Cancelled'))
        booking.string = None
        booking.save()
        merge_availabilities_algorithm(booking)
        send_cancellation_confirmation(booking)
        return Response(status=status.HTTP_200_OK)


class BookedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, user=request.user)
        except ObjectDoesNotExist:
            raise Http404
        serializer = BikeSerializer(booking.bike, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreOfBookedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, user=request.user)
        except ObjectDoesNotExist:
            raise Http404
        serializer = StoreSerializer(booking.bike.store, many=False)
        serializer.exclude_fields(['store_flag'])
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDataOfUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fields_to_include = ['contact_data', 'username', 'user_status']
        serializer = UserSerializer(self.request.user, many=False, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteUserAccount(DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if Booking.objects.filter(user=user, booking_status=Booking_Status.objects.get(booking_status='Picked up')).exists():
            raise serializers.ValidationError('Account deletion not possible whilst having picked up a bike.')
        if user.user_status.contains(User_Status.objects.get(user_status='Administrator')) and \
                User.objects.filter(user_status__user_status='Administrator').count() == 1:
            raise serializers.ValidationError('Account deletion not possible as only administrator.')
        if LocalData.objects.filter(user=user).exists():
            LocalData.objects.get(user=user).anonymize().save()
        bookings = Booking.objects.filter(user=user, booking_status=Booking_Status.objects.get(booking_status='Booked'))
        for booking in bookings:
            booking.booking_status.clear()
            booking.booking_status.add(Booking_Status.objects.get(booking_status='Cancelled'))
            booking.string = None
            booking.save()
            merge_availabilities_algorithm(booking)
        user.anonymize().save()
        user.user_status.clear()
        return Response(status=status.HTTP_200_OK)