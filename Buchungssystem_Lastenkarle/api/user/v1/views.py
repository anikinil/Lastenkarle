from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import *
from authlib.integrations.django_client import OAuth
from django.http import Http404

from api.serializer import *
from db_model.models import *

from Buchungssystem_Lastenkarle.settings import CANONICAL_HOST
from send_mail.views import send_cancellation_confirmation
from send_mail.views import send_user_changed_mail
from send_mail.views import send_user_registered_confirmation
from django.shortcuts import redirect

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
        print(response)
        print( {
            'state': {'token': response.data.get('token')}})
        token_value = response.data.get('token')
        redirect_url = f"{CANONICAL_HOST}/menu/?token={token_value}"

        return redirect(redirect_url)


class RegistrateUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
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
            user = User.objects.get(pk=user_id, verification_string=verification_string)
        except ObjectDoesNotExist:
            raise Http404
        user.user_flags.add(User_Flag.objects.get(flag='Verified'))
        user.verification_string = None
        user.save()
        return Response(status=status.HTTP_200_OK)


class UpdateUserData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if serializer.validated_data.get('contact_data', None) is not None:
            send_user_changed_mail(user)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request, serializer.validated_data['user'])
        response = super(LoginView, self).post(request, format=None)
        return Response({'token': response.data.get('token')}, status=status.HTTP_200_OK)


class AllBookingsFromUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingFromUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, user=request.user)
        except ObjectDoesNotExist:
            raise Http404
        serializer = BookingSerializer(booking, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, user=request.user)
        except ObjectDoesNotExist:
            raise Http404
        if ([Booking_Status.objects.get(status='Picked up')] in booking.booking_status.all())\
                or Booking_Status.objects.get(status='Booked') not in booking.booking_status.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        booking.cancel_booking()
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
        serializer = StoreSerializer(booking.bike.store, exclude=['store_flag'], many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDataOfUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteUserAccount(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        if Booking.objects.filter(user=request.user, booking_status=Booking_Status.objects.get(status='Picked up')).exists():
            return Response({'Account deletion not possible whilst having picked up a bike.'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.user_flags.contains(User_Flag.objects.get(flag='Administrator')) and User.objects.filter(user_flags__flag='Administrator').count() < 2:
            return Response({'Account deletion not possible as only administrator.'}, status=status.HTTP_400_BAD_REQUEST)
        if LocalData.objects.filter(user=request.user).exists():
            LocalData.objects.get(user=request.user).anonymize().save()
        for booking in Booking.objects.filter(user=request.user, booking_status=Booking_Status.objects.get(status='Booked')):
            booking.cancel_booking()
        request.user.anonymize().save()
        return Response(status=status.HTTP_200_OK)
