from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
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

    def get(self, request, format=None):
        token = oauth.helmholtz.authorize_access_token(request)
        userinfo = oauth.helmholtz.userinfo(request=request, token=token)
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
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.verification_string = generate_random_string(30)
            user.save()
            send_user_registered_confirmation(user)
            #TODO: view for redirect page and set user as verified
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def post(self, request, user_id, verification_string):
        if User.objects.filter(pk=user_id, verification_string=verification_string).exists():
            user = User.objects.get(pk=user_id)
            user.user_status.add(User_Status.objects.get(user_status='Verified'))
            user.verification_string = None
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateUserData(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.request.user
        print("i am here 1")
        if request.data.get('contact_data') is not None:
            print("i am here 2")
            user = request.user
            if user.user_status.contains(User_Status.objects.get(user_status='Verified')):
                user.user_status.remove(User_Status.objects.get(user_status='Verified'))
                user.verification_string = generate_random_string(30)
                print("i am here 3")
                user.save()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_user_changed_mail(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super(LoginView, self).post(request, format=None)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response.data, status=status.HTTP_200_OK)

class AllBookingsFromUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fields_to_include = ['id', 'begin', 'end', 'booking_status']
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookingFromUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        fields_to_include = ['id', 'begin', 'end', 'booking_status']
        booking = Booking.objects.get(pk=booking_id)
        serializer = BookingSerializer(booking, many=False, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id)
        except ObjectDoesNotExist:
            raise Http404
        booking = Booking.objects.get(pk=booking_id)
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
            Booking.objects.get(pk=booking_id).bike
        except ObjectDoesNotExist:
            raise Http404
        fields_to_include = ['id', 'name', 'description', 'image_link']
        bike = Booking.objects.get(pk=booking_id).bike
        serializer = BikeSerializer(bike, many=False, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StoreOfBookedBike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            Booking.objects.get(pk=booking_id).bike.store
        except ObjectDoesNotExist:
            raise Http404
        fields_to_include = ['id', 'region', 'address', 'name']
        store = Booking.objects.get(pk=booking_id).bike.store
        serializer = StoreSerializer(store, many=False, fields=fields_to_include)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LocalDataOfUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            local_data = LocalData.objects.get(user=User.objects.get(pk=self.request.user.pk))
        except ObjectDoesNotExist:
            raise Http404
        serializer = LocalDataSerializer(local_data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDataOfUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_data = User.objects.get(pk=self.request.user.pk)
        except ObjectDoesNotExist:
            raise Http404
        serializer = UserSerializer(user_data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteUserAccount(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        if LocalData.objects.filter(user=user).exists():
            LocalData.objects.get(user=user).anonymize().save()
        user.anonymize().save()
        user.user_status.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
