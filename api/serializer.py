from rest_framework import serializers
from db_model.models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ID_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ID_Data
        fields = '__all__'


class OIDC_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OIDC_Data
        fields = '__all__'


class Local_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local_Data
        fields = '__all__'


class User_FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Flag
        fields = '__all__'


class User_StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Status
        fields = '__all__'


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class Availability_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'


class Availability_StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability_Status
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class Booking_FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_Flag
        fields = '__all__'


class Booking_StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_Status
        fields = '__all__'


class Mail_TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail_Template
        fields = '__all__'
