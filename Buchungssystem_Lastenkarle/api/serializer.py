from rest_framework import serializers
from django.contrib.auth import authenticate
from db_model.models import *


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Status
        fields = ['user_status']


class UserSerializer(serializers.ModelSerializer):
    user_status = UserStatusSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            for field_name in set(self.fields.keys()) - set(fields):
                self.fields.pop(field_name)



class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('contact_data',
                  'year_of_birth',
                  'username',
                  'password')

    def validate(self, attrs):
        username = attrs.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists.')
        return attrs

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        if username and password:
            auth_user = User.objects.create_user(username, password, **validated_data)
            return auth_user

        return


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type':'password'}, trim_whitespace=False)


    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Please give both username and password')

        if not User.objects.filter(username=username).exists():
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


class LocalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalData
        fields = ('first_name',
                  'last_name',
                  'address',
                  'date_of_verification',
                  'id_number')

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance


class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = '__all__'


class BikeSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Bike
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            for field_name in set(self.fields.keys()) - set(fields):
                self.fields.pop(field_name)


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            for field_name in set(self.fields.keys()) - set(fields):
                self.fields.pop(field_name)


class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_Status
        fields = ['booking_status']


class MakeBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    booking_status = BookingStatusSerializer(many=True, read_only=True)
    equipment = serializers.ListField(child=serializers.CharField(max_length=256))  # Keep this for validation

    class Meta:
        model = Booking
        fields = '__all__'

    def create(self, validated_data):
        equipment_data = validated_data.pop('equipment', [])
        booking = Booking.objects.create(**validated_data)
        for equipment_name in equipment_data:
            equipment, _ = Equipment.objects.get_or_create(equipment=equipment_name)
            booking.equipment.add(equipment)
        return booking


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    booking_status = BookingStatusSerializer(many=True, read_only=True)
    equipment = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            for field_name in set(self.fields.keys()) - set(fields):
                self.fields.pop(field_name)


class AvailabilityStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability_Status
        fields = ['availability_status']

class AvailabilitySerializer(serializers.ModelSerializer):
    availability_status = AvailabilityStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Availability
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            for field_name in set(self.fields.keys()) - set(fields):
                self.fields.pop(field_name)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            for field_name in set(self.fields.keys()) - set(fields):
                self.fields.pop(field_name)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance