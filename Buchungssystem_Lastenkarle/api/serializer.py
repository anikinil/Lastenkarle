from rest_framework import serializers
from db_model.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'year_of_birth', 'assurance_lvl', 'contact_data')

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class RegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True, many=False)

    class Meta:
        model = ID_Data
        fields = ('user',
                  'first_name',
                  'last_name',
                  'address',
                  'date_of_verification',
                  'id_number')

    def create(self, validated_data):
        password = self.initial_data['password']
        user = User.objects.create(**validated_data.pop('user', None))
        Local_Data.objects.create(user=user, password=password)
        id_data = ID_Data.objects.create(user=user, **validated_data)
        return id_data

class OIDC_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OIDC_Data
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()




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


class Availability_StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability_Status
        fields = '__all__'
        depth = 1



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class Mail_TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail_Template
        fields = '__all__'
