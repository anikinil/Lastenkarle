from rest_framework import serializers
from django.contrib.auth import authenticate
from db_model.models import User, LoginData, Booking, LocalData, Bike, Store, User_status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('assurance_lvl',
                  'year_of_birth',
                  'contact_data')

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance

class LoginDataSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = LoginData
        fields = '__all__'

"""
JSON format for user creation:

{
    "local_data":{
        "first_name":"",
        "last_name":"",
        "address":"",
        "date_of_verification":"",
        "id_number":""
    },
    "user": {
        "assurance_lvl": "",
        "year_of_birth": ,
        "contact_data": ""
    },
    "username": "",
    "password": ""
}
"""
class RegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = LoginData
        exclude = ['last_login']

    def validate(self, attrs):
        username = attrs.get('username')
        if LoginData.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists.')
        return attrs

    def to_internal_value(self, data):
        local_data = data.pop('local_data', {})
        validated_data = super().to_internal_value(data)
        validated_data['local_data'] = local_data
        return validated_data

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        if username and password:
            auth_user = LoginData.objects.create_user(username, password, **validated_data)
            return auth_user
        # logic for oidc user creation data handling
        return


class UpdateLoginDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginData
        fields = ('username',
                  'password')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance


class UpdateLocalDataSerializer(serializers.ModelSerializer):
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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type':'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Please give both username and password')

        if not LoginData.objects.filter(username=username).exists():
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


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = '__all__'

class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_status
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['REGION']



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
