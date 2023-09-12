from django.contrib.auth import authenticate
from db_model.models import *
from rest_framework import serializers
from validate_email import validate_email
from datetime import datetime, date, time, timedelta
from django.utils import timezone


def weekday_prefix_of_date(date_obj):
    if date_obj:
        try:
            # Convert the date object to a datetime object
            date = datetime(date_obj.year, date_obj.month, date_obj.day)

            # Extract the weekday as a string
            weekday = date.strftime("%a")

            return weekday
        except ValueError:
            # Handle invalid date format
            return None
    else:
        # Handle missing date parameter
        return None


def partialUpdateInputValidation(request, fields_to_include):
    for field_name in request.data.keys():
        if field_name not in fields_to_include:
            raise serializers.ValidationError('Updating field is not allowed.')


def partialUpdateOfBike(request, bike):
    fields_to_include = ['name', 'description', 'image']
    partialUpdateInputValidation(request, fields_to_include)
    serializer = BikeSerializer(bike, data=request.data, fields=fields_to_include, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def partialUpdateOfStore(request, store):
    fields_to_include = ['address', 'phone_number', 'email', 'prep_time',
                         'mon_opened', 'mon_open', 'mon_close',
                         'tue_opened', 'tue_open', 'tue_close',
                         'wed_opened', 'wed_open', 'wed_close',
                         'thu_opened', 'thu_open', 'thu_close',
                         'fri_opened', 'fri_open', 'fri_close',
                         'sat_opened', 'sat_open', 'sat_close',
                         'sun_opened', 'sun_open', 'sun_close']
    partialUpdateInputValidation(request, fields_to_include)
    serializer = StoreSerializer(store, data=request.data, fields=fields_to_include, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Status
        fields = ['user_status']


class UserSerializer(serializers.ModelSerializer):
    user_status = UserStatusSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, attrs):
        username = attrs
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists.')
        return attrs

    def validate_contact_data(self, attrs):
        contact_data = attrs
        if not validate_email(contact_data):
            raise serializers.ValidationError('Contact data is not an valid email')
        if User.objects.filter(contact_data=contact_data).exists():
            raise serializers.ValidationError('Contact data already exists.')
        return attrs

    def validate_password(self, attrs):
        password = attrs
        if password is None:
            raise serializers.ValidationError('Password required.')
        return attrs

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
        username = attrs.get('username', None)
        if username is None:
            raise serializers.ValidationError('Username required.')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists.')
        contact_data = attrs.get('contact_data', None)
        if contact_data is None:
            raise serializers.ValidationError('Contact data required.')
        if not validate_email(contact_data):
            raise serializers.ValidationError('Contact data is not an valid email')
        if User.objects.filter(contact_data=contact_data).exists():
            raise serializers.ValidationError('Contact data already exists.')
        password = attrs.get('password', None)
        if password is None:
            raise serializers.ValidationError('Password required.')
        year_of_birth = attrs.get('year_of_birth', None)
        if year_of_birth is not None and year_of_birth < datetime.now().year - 122:
            raise serializers.ValidationError('You are definitely not older than Jeanne Calment.')
        if year_of_birth is not None and year_of_birth > datetime.now().year + 1:
            raise serializers.ValidationError('You are definitely not born in the future.')
        return attrs

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        if username:
            auth_user = User.objects.create_user(username, password, **validated_data)
            return auth_user


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

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            for field_name in set(self.fields.keys()) - set(fields):
                self.fields.pop(field_name)


class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = '__all__'


class BikeSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    image = serializers.ImageField()

    class Meta:
        model = Bike
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            for field_name in set(self.fields.keys()) - set(fields):
                self.fields.pop(field_name)

    def update(self, instance, validated_data):
        if validated_data.get('image', None) is not None:
            instance.image.delete()
        instance = super().update(instance, validated_data)
        return instance


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

    def validate_email(self, attrs):
        if not validate_email(attrs):
            raise serializers.ValidationError('Not an valid email.')
        return attrs

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            for field_name in set(self.fields.keys()) - set(fields):
                self.fields.pop(field_name)

    def exclude_fields(self, excluded_fields):
        if excluded_fields:
            for field_name in excluded_fields:
                self.fields.pop(field_name)


class BookingStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking_Status
        fields = ['booking_status']


class MakeBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    booking_status = BookingStatusSerializer(many=True, read_only=True)
    equipment = serializers.ListField(child=serializers.CharField(max_length=256))

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, attrs):
        begin = attrs.get('begin')
        end = attrs.get('end')
        no_limit = self.context.get('no_limit')
        if not no_limit:
            if (end - begin).days > 7:
                raise serializers.ValidationError('Customers are not allowed to make booking of attempted length.')
        bike = attrs.get('bike')
        store = bike.store
        left = Availability.objects.filter(until_date__gte=end,
                                           store=bike.store,
                                           bike=bike,
                                           availability_status=
                                           Availability_Status.objects.get(availability_status='Available'))
        if not no_limit:
            if not left.exists():
                raise serializers.ValidationError('Bike not available in selected time frame.')
            availability = left.order_by('until_date').first()
            if not availability.from_date <= begin or not availability.until_date >= end:
                raise serializers.ValidationError('Bike not available in selected time frame.')
        if begin > end:
            raise serializers.ValidationError('Time travel is not permitted.')
        day_prefix_begin = weekday_prefix_of_date(begin)
        settings_for_day = store.get_settings_for_day(day_prefix_begin)
        if not settings_for_day[0]:
            raise serializers.ValidationError('Store closed on starting day of booking.')
        prep_time = store.prep_time
        current_time = timezone.now()
        earliest_booking_begin = current_time + timedelta(hours=prep_time.hour, minutes=prep_time.minute)
        start_time = datetime.strptime(settings_for_day[1], "%H:%M").time()
        start_booking = timezone.make_aware(datetime.combine(begin, start_time), timezone.get_current_timezone())
        if earliest_booking_begin > start_booking:
            raise serializers.ValidationError('Store does not provide bike this early.')
        day_prefix_end = weekday_prefix_of_date(end)
        settings_for_day = store.get_settings_for_day(day_prefix_end)
        if not settings_for_day[0]:
            raise serializers.ValidationError('Store closed on ending day of booking.')
        return attrs

    def create(self, validated_data):
        equipment_data = validated_data.pop('equipment', [])
        booking = Booking.objects.create(**validated_data)
        for equipment_name in equipment_data:
            equipment, _ = Equipment.objects.get_or_create(equipment=equipment_name)
            booking.equipment.add(equipment)
        return booking

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            for field_name in set(self.fields.keys()) - set(fields):
                self.fields.pop(field_name)


class BookingSerializer(serializers.ModelSerializer):
    preferred_username = serializers.ReadOnlyField(source='user.preferred_username')
    assurance_lvl = serializers.ReadOnlyField(source='user.assurance_lvl')
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
