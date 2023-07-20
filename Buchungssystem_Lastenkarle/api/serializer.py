from rest_framework import serializers
from db_model.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'year_of_birth',
                  'assurance_lvl',
                  'contact_data')

class ID_DataSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = ID_Data
        fields = ('user',
                  'first_name',
                  'last_name',
                  'address',
                  'date_of_verification',
                  'id_number')

    def create(self, validated_data):
        return User.objects.create(
            username=validated_data['username'],
            year_of_birth=validated_data['year_of_birth'],
            assuarance_lvl=validated_data['assurance_lvl'],
            contact_data=validated_data['contact_data'],
            user=validated_data['user'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            address=validated_data['address'],
            date_of_verification=validated_data['date_of_verification'],
            id_number=validated_data['id_number']
        )



class OIDC_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OIDC_Data
        fields = '__all__'


class Local_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local_Data
        fields = '__all__'


class User_StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Status
        fields = '__all__'
        depth = 1



class User_FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Flag
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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ID_Data
        fields = '__all__'
        depth = 1

class Availability_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Availability
        fields = '__all__'


class Availability_StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability_Status
        fields = '__all__'
        depth = 1


class Availability_FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability_Flag
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
