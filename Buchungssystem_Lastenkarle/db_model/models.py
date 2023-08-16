from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create internal user model here.


def get_store_name_from_flag(user_status_flag, store_flag):
    try:
        for flag_tuple in user_status_flag:
            if flag_tuple[0] == store_flag:
                return flag_tuple[1]
        return None  # If the store_flag is not found in the user_status_flag
    except ValueError:
        return None


class UserManager(BaseUserManager):

    def create_user(self, username, password, **extra_fields):
        user = User.objects.create(username=username, password=password, **extra_fields)
        user.is_active = True
        user.user_status.set(User_status.objects.filter(user_status='C'))
        if user.is_superuser:
            user.user_status.set(User_status.objects.filter(user_status='I'))
        user.set_password(password)
        user.save()
        return user

    def create_helmholtz_user(self, userinfo):
        user = User.objects.create(username=userinfo['eduperson_unique_id'], password=" ")
        user.is_active = True
        user.user_status.set(User_status.objects.filter(user_status='C'))
        if user.is_superuser:
            user.user_status.set(User_status.objects.filter(user_status='I'))
        return self.update_helmholtz_user(user, userinfo)

    def update_helmholtz_user(self, user, userinfo):
        if 'https://refeds.org/assurance/IAP/high' in userinfo['eduperson_assurance']:
            user.assurance_lvl = 'H'
        elif 'https://refeds.org/assurance/IAP/medium' in userinfo['eduperson_assurance']:
            user.assurance_lvl = 'M'
        else:
            user.assurance_lvl = 'L'
        user.save()
        return user

    def create_superuser(self, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(**extra_fields)


class Store(models.Model):
    REGION = [("KA", "Karlsruhe"), ("ETT", "Ettlingen"), ("BAD", "Baden-Baden"),
              ("BRU", "Bruchsal"), ("MAL", "Malsch"), ]
    region = models.TextField(max_length=3, choices=REGION)
    address = models.TextField(default="ERROR")
    name = models.TextField(default="ERROR", unique=True)


class User_status(models.Model):
    USER_STATUS_FLAG = [
        ('V', 'Verified'),
        ('D', 'Deleted'),
        ('R', 'Reminded'),
        ('A', 'Administrator'),
        ('B', 'Banned'),
        ('S1', 'Store1'),  # S+STORE_ID, STORENAME
        ('S2', 'Store2'),
        ('S3', 'Store3'),
        ('C', 'Customer')
    ]
    user_status = models.CharField(max_length=3, choices=USER_STATUS_FLAG)


class User(AbstractBaseUser):
    ASSURANCE_LEVEL = [
        ("N", "None"), ("L", "Low"), ("M", "Medium"), ("H", "High"),
    ]
    user_status = models.ManyToManyField(User_status, blank=True)
    assurance_lvl = models.CharField(max_length=1, choices=ASSURANCE_LEVEL, null=True, blank=True)
    year_of_birth = models.IntegerField(null=True, blank=True)
    contact_data = models.TextField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = models.TextField(max_length=30, unique=True, null=True, blank=True)
    password = models.TextField(null=True, blank=True)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def anonymize(self):
        self.assurance_lvl = None
        self.year_of_birth = None
        self.contact_data = None
        self.is_superuser = False
        self.is_staff = False
        self.is_active = False
        self.username = None
        self.password = None
        return self

    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def is_staff_of_store(self):
        store_flag = self.user_status.filter(user_status__startswith='S')
        for first_part, second_part in User_status.USER_STATUS_FLAG:
            if first_part == store_flag.first().user_status:
                store_name = second_part
                return Store.objects.get(name=store_name)
        return None


class OIDCLoginData(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, null=True, blank=True)
    issue = models.TextField(default="ERROR")
    subject = models.TextField(default="ERROR")


class LocalData(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.TextField(default="ERROR", null=True, blank=True)
    last_name = models.TextField(default="ERROR", null=True, blank=True)
    address = models.TextField(default="ERROR", null=True, blank=True)
    date_of_verification = models.DateField(null=True, blank=True)
    id_number = models.TextField(max_length=3, null=True, blank=True)

    def anonymize(self):
        self.first_name = None
        self.last_name = None
        self.address = None
        self.date_of_verification = None
        self.id_number = None
        return self


class Bike(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.TextField(default="ERROR")
    description = models.TextField(default="ERROR")
    image_link = models.TextField(default="ERROR")


class Availability_Status(models.Model):
    AVAILABILITY_STATUS_FLAG = [
        ('B', 'Booked'),
        ('A', 'Available')
    ]
    availability_status = models.CharField(max_length=1, choices=AVAILABILITY_STATUS_FLAG)


class Availability(models.Model):
    from_date = models.DateField(null=True)
    until_date = models.DateField(null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    availability_status = models.ManyToManyField(Availability_Status)


class Booking_Status(models.Model):
    BOOKING_STATUS_FLAG = [
        ('B', 'Booked'),
        ('I', 'Internal usage'),
        ('P', 'Picked up'),
        ('C', 'Cancelled'),
        ('R', 'Returned')
    ]
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS_FLAG)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    begin = models.DateField(null=True)
    end = models.DateField(null=True)
    string = models.CharField(max_length=5, null=True, unique=True)
    booking_status = models.ManyToManyField(Booking_Status)


class Mail_Template(models.Model):
    subject = models.TextField(default="ERROR")
    content = models.TextField(default="ERROR")


class Comment(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    content = models.TextField(default="ERROR")
