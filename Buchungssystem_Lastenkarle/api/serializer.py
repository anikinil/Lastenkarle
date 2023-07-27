from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from db_model.models import *


class InternalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username',
                  'year_of_birth',
                  'assurance_lvl',
                  'contact_data',
                  'first_name',
                  'last_name',
                  'address',
                  'date_of_verification',
                  'id_number',
                  'password',
                  'is_staff',
                  'is_superuser',
                  'is_active')

    def create(self, validated_data):
        return UserI.objects.create(**validated_data)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


    def validate(self, attrs):
        username = attrs.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('User with username already exists.')
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        dbuser = UserI.objects.create(username=user.username,
                             year_of_birth=user.year_of_birth,
                             assurance_lvl=user.assurance_lvl,
                             contact_data=user.contact_data)
        Local_Data.objects.create(user=dbuser, password=user.password)
        ID_Data.objects.create(user=dbuser, first_name=user.first_name,
                               last_name=user.last_name, address=user.address,
                               date_of_verification=user.date_of_verification,
                               id_number=user.id_number)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username',
                  'year_of_birth',
                  'assurance_lvl',
                  'contact_data',
                  'first_name',
                  'last_name',
                  'address',
                  'date_of_verification',
                  'id_number',
                  'password',
                  'is_staff',
                  'is_superuser',
                  'is_active')

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance


class UserDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserI
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type':'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Please give both username and password')

        if not CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username not found enter correct credentials')
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
            )
        if not user:
            raise serializers.ValidationError('Wrong credentials')
        attrs['user'] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):
    user = UserDBSerializer()
    class Meta:
        model = ID_Data
        fields = ('user',
                  'first_name',
                  'last_name',
                  'address',
                  'date_of_verification',
                  'id_number')


class OIDC_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OIDC_Data
        fields = '__all__'


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['REGION']


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Status
        fields = '__all__'
        depth = 1


class Availability_StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability_Status
        fields = '__all__'
        depth = 1


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

