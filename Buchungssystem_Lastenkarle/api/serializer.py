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


class UserFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Flag
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude', None)
        super(UserFlagSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)


class UserSerializer(serializers.ModelSerializer):
    user_flags = UserFlagSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude', None)
        super(UserSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)

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


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['contact_data', 'username', 'password']

    def validate(self, attrs):
        if not len(attrs.items())>0:
            raise serializers.ValidationError('Supply data')
        for key, value in attrs.items():
            if key not in set(self.fields.keys()):
                raise serializers.ValidationError('WRONG KEY')
            if value is None:
                raise serializers.ValidationError('WRONG INPUT')
        contact_data = attrs.get('contact_data', None)
        if contact_data is not None and User.objects.filter(contact_data=contact_data).exists():
            raise serializers.ValidationError('Contact data already used.')
        username = attrs.get('username', None)
        if username is not None and User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already used.')
        return attrs

    def update(self, instance, validated_data):
        contact_data = validated_data.get('contact_data', None)
        username = validated_data.get('username', None)
        password = validated_data.get('password', None)
        if username is not None:
            instance.username = username
        if password is not None:
            instance.set_password(instance.password)
        if contact_data is not None:
            instance.user_flags.remove(User_Flag.objects.get(flag='Verified'))
            instance.verification_string = generate_random_string(30)
        instance.save()
        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['contact_data',
                  'year_of_birth',
                  'username',
                  'password']

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
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

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
        fields = ['first_name',
                  'last_name',
                  'address',
                  'date_of_verification',
                  'id_number']

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude', None)
        super(LocalDataSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)

    def validate(self, attrs):
        for key, value in attrs.items():
            if key not in set(self.fields.keys()):
                raise serializers.ValidationError('WRONG KEY')
            if value is None:
                raise serializers.ValidationError('WRONG INPUT')
        return attrs

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude', None)
        super(EquipmentSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)


class RemoveEquipmentSerializer(serializers.Serializer):
    bike_id = serializers.IntegerField()
    equipment = serializers.CharField()

    def validate(self, attrs):
        bike_id = attrs.get('bike_id', None)
        equipment = attrs.get('equipment', None)
        if None in [bike_id, equipment]:
            raise serializers.ValidationError('WRONG INPUT')
        if not Bike.objects.filter(pk=bike_id).exists():
            raise serializers.ValidationError('Bike does not exist.')
        if not Equipment.objects.filter(equipment=equipment).exists():
            raise serializers.ValidationError('Equipment does not exist.')
        return attrs

    def create(self, validated_data):
        bike = Bike.objects.get(pk=validated_data.get('bike_id'))
        bike.bike_equipment.remove(Equipment.objects.get(equipment=validated_data.get('equipment')))
        return bike


class BikeSerializer(serializers.ModelSerializer):
    bike_equipment = EquipmentSerializer(many=True, read_only=True)
    image = serializers.ImageField()

    class Meta:
        model = Bike
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude', None)
        super(BikeSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)

    def validate(self, attrs):
        for key, value in attrs.items():
            if key not in set(self.fields.keys()):
                raise serializers.ValidationError('WRONG KEY')
            if value is None:
                raise serializers.ValidationError('REQUIRED FIELD')
        return attrs

    def update(self, instance, validated_data):
        if validated_data.get('image', None) is not None:
            instance.image.delete()
        instance = super().update(instance, validated_data)
        return instance


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude', None)
        super(RegionSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)


class StoreSerializer(serializers.ModelSerializer):
    region = RegionSerializer(many=False, read_only=True)

    class Meta:
        model = Store
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude', None)
        super(StoreSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)


class CreateStoreSerializer(serializers.ModelSerializer):
    region = RegionSerializer(many=False, read_only=True)

    class Meta:
        model = Store
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude', None)
        super(CreateStoreSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)

    def validate(self, attrs):
        region = self.initial_data.get('region', None)
        address = attrs.get('address', None)
        email = attrs.get('email', None)
        name = attrs.get('name', None)
        if region is None:
            raise serializers.ValidationError('Region must not be empty.')
        if None in (region, address, email, name):
            raise serializers.ValidationError('Not all necessary information provided.')
        if Store.objects.filter(name=name).exists():
            raise serializers.ValidationError('Store with given name already exists.')
        if not Region.objects.filter(name=region).exists():
            raise serializers.ValidationError('Region does not exist.')
        if not validate_email(email):
            raise serializers.ValidationError('Not an valid email.')
        if Store.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already used.')
        attrs['region'] = Region.objects.get(name=region)
        return attrs


class UpdateStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['phone_number', 'email', 'prep_time',
                  'mon_opened', 'mon_open', 'mon_close',
                  'tue_opened', 'tue_open', 'tue_close',
                  'wed_opened', 'wed_open', 'wed_close',
                  'thu_opened', 'thu_open', 'thu_close',
                  'fri_opened', 'fri_open', 'fri_close',
                  'sat_opened', 'sat_open', 'sat_close',
                  'sun_opened', 'sun_open', 'sun_close']

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude', None)
        super(UpdateStoreSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)

    def validate(self, attrs):
        for key, value in self.initial_data.items():
            if key not in set(self.fields.keys()):
                raise serializers.ValidationError('Updating ' + key + ' is forbidden.')
        return attrs

    def update(self, instance, validated_data):
        instance = super(UpdateStoreSerializer, self).update(instance, validated_data)
        return instance


class UpdateBikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ['name', 'description', 'image']

    def validate(self, attrs):
        for key, value in self.initial_data.items():
            if key not in set(self.fields.keys()):
                raise serializers.ValidationError('Updating ' + key + ' is forbidden.')
        return attrs

    def update(self, instance, validated_data):
        if validated_data.get('image', None) is not None:
            instance.image.delete()
        instance = super(UpdateBikeSerializer, self).update(instance, validated_data)
        return instance


class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_Status
        fields = ['status']

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude', None)
        super(BookingStatusSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)


class MakeBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    booking_status = BookingStatusSerializer(many=True, read_only=True)
    equipment = EquipmentSerializer(many=True, read_only=True)

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
            booking.item.add(equipment)
        booking.booking_status.add(Booking_Status.objects.get(status='Booked').pk)
        booking.string = generate_random_string(5)
        booking.save()
        return booking


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    booking_status = BookingStatusSerializer(many=True, read_only=True)
    equipment = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude', None)
        super(BookingSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)


class UpdateCommentOfBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['comment']

    def validate(self, attrs):
        for key, value in self.initial_data.items():
            if key not in set(self.fields.keys()):
                raise serializers.ValidationError('Updating ' + key + ' is forbidden.')
        return attrs


class AvailabilityStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability_Status
        fields = ['availability_status']

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude', None)
        super(AvailabilityStatusSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)


class AvailabilitySerializer(serializers.ModelSerializer):
    availability_status = AvailabilityStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Availability
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude', None)
        super(AvailabilitySerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field in exclude_fields:
                self.fields.pop(field, None)


class EnrollmentSerializer(serializers.Serializer):
    contact_data = serializers.EmailField()
    flag = serializers.CharField(max_length=1024)

    def validate(self, attrs):
        enrolling_user = self.context.get('user')
        contact_data = attrs.get('contact_data', None)
        flag = attrs.get('flag', None)
        if None in [flag, contact_data]:
            raise serializers.ValidationError('Invalid input.')
        if not User_Flag.objects.filter(flag=flag).exists():
            raise serializers.ValidationError('Flag does not exist.')
        if not User.objects.filter(contact_data=contact_data).exists():
            raise serializers.ValidationError('User does not exist.')
        if not enrolling_user.user_flags.filter(flag__in=['Administrator', flag]).exists():
            raise serializers.ValidationError('Not permitted to access flag.')
        invalid_flags = ['Verified', 'Deleted', 'Reminded', 'Banned', 'Customer']
        if flag in invalid_flags:
            raise serializers.ValidationError('Cannot enroll user as ' + flag + '.')
        if User.objects.filter(contact_data=contact_data, user_flags__flag=flag).exists():
            raise serializers.ValidationError('User already enrolled as ' + flag + '.')
        return attrs

    def update(self, instance, validated_data):
        instance = User.objects.get(contact_data=validated_data.get('contact_data'))
        user_flag = User_Flag.objects.get(flag=validated_data.get('flag'))
        instance.user_flags.add(user_flag.pk)
        if user_flag.flag.startswith('Store:') and not instance.is_staff:
            instance.is_staff = True
        if user_flag == User_Flag.objects.get(flag='Administrator') and not instance.is_superuser:
            instance.is_superuser = True
        instance.save()
        return instance


class BanningSerializer(serializers.Serializer):
    contact_data = serializers.EmailField()

    def validate(self, attrs):
        contact_data = attrs.get('contact_data')
        if not User.objects.filter(contact_data=contact_data).exists():
            raise serializers.ValidationError('User does not exist.')
        if User.objects.filter(contact_data=contact_data,
                               user_flags__flag=User_Flag.objects.get(flag='Banned').flag).exists():
            raise serializers.ValidationError('User already banned.')
        return attrs

    def create(self, validated_data):
        instance = User.objects.get(contact_data=self.validated_data.get('contact_data'))
        instance.user_flags.add(User_Flag.objects.get(flag='Banned'))
        instance.is_superuser = False
        instance.is_staff = False
        instance.is_active = False
        instance.save()
        return instance


class BikeCreationSerializer(serializers.ModelSerializer):
    bike_equipment = EquipmentSerializer(many=True, read_only=True)
    image = serializers.ImageField()

    class Meta:
        model = Bike
        fields = '__all__'
        extra_kwargs = {
            'store': {'required': False}
        }

    def validate(self, attrs):
        store = self.context.get('store', None)
        name = attrs.get('name', None)
        description = attrs.get('description', None)
        image = attrs.get('image', None)
        if None in (store, name, description, image):
            raise serializers.ValidationError('Insufficient data provided.')
        allowed_content_types = ['image/jpeg', 'image/png']
        if image.content_type not in allowed_content_types:
            raise serializers.ValidationError("Invalid image file format. Only JPEG and PNG images are allowed.")
        attrs['store'] = store
        return attrs

    def update(self, instance, validated_data):
        if validated_data.get('image', None) is not None:
            instance.image.delete()
        instance = super().update(instance, validated_data)
        return instance
