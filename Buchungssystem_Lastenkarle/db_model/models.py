from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import date
from api.configs.ConfigFunctions import deleteStoreConfig


class UserManager(BaseUserManager):

    def create_user(self, username, password, **extra_fields):
        user = User(username=username, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save()

        user_status_customer = User_Status.objects.get(user_status='Customer')
        user.user_status.add(user_status_customer)

        if user.is_superuser:
            user_status_admin = User_Status.objects.get(user_status='Administrator')
            user.user_status.add(user_status_admin)

        return user

    def create_helmholtz_user(self, userinfo):
        user = User.objects.create(username=userinfo['eduperson_unique_id'], password=" ")
        user.is_active = True
        user.user_status.add(User_Status.objects.get(user_status='Customer'))
        if user.is_superuser:
            user.user_status.add(User_Status.objects.get(user_status='Administrator'))
        return self.update_helmholtz_user(user, userinfo)

    def update_helmholtz_user(self, user, userinfo):
        if 'https://refeds.org/assurance/IAP/high' in userinfo['eduperson_assurance']:
            user.assurance_lvl = 'H'
        elif 'https://refeds.org/assurance/IAP/medium' in userinfo['eduperson_assurance']:
            user.assurance_lvl = 'M'
        else:
            user.assurance_lvl = 'L'
        user.contact_data = userinfo['email']
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
    store_flag = models.OneToOneField('User_Status', on_delete=models.CASCADE, null=True)
    region = models.TextField(max_length=3, choices=REGION)
    address = models.TextField(default="ERROR")
    phone_number = models.TextField(max_length=256)
    email = models.TextField(max_length=256)
    name = models.TextField(default="ERROR", unique=True)

    def delete(self, *args, **kwargs):
        deleteStoreConfig(store_name=self.name)
        if self.store_flag:
            self.store_flag.delete()
        self.bike_set.all().delete()
        super(Store, self).delete(*args, **kwargs)


class User_Status(models.Model):
    user_status = models.CharField(max_length=32)

    @classmethod
    def custom_create_store_flags(cls, store):
        store_name = store.name
        flag = f"Store: {store_name}"
        instance = cls(user_status=flag)
        instance.save()
        return instance

    @classmethod
    def get_store_of_flag(self):
        if self.user_status.startswith("Store:"):
            flag = self.user_status
            _, store_name = flag.split(":", 1)
            store = Store.objects.get(name=store_name)
            return store
        return None


class User(AbstractBaseUser):
    ASSURANCE_LEVEL = [
        ("N", "None"), ("L", "Low"), ("M", "Medium"), ("H", "High"),
    ]
    user_status = models.ManyToManyField(User_Status, blank=True)
    assurance_lvl = models.CharField(max_length=1, choices=ASSURANCE_LEVEL, default='N', null=True)
    year_of_birth = models.IntegerField(null=True, blank=True)
    contact_data = models.TextField(unique=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = models.TextField(max_length=1028, unique=True, null=True, blank=True)
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
        store_flag = self.user_status.get(user_status__startswith='Store:').user_status
        name_part = store_flag.split(': ')[1]
        store = Store.objects.get(name=name_part)
        return store


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


class Equipment(models.Model):
    equipment = models.TextField(max_length=256, unique=True)


class Bike(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.TextField(default="ERROR")
    description = models.TextField(default="ERROR")
    image_link = models.TextField(default="ERROR")
    equipment = models.ManyToManyField(Equipment)

    def delete(self, *args, **kwargs):
        self.availability_set.all().delete()
        super(Bike, self).delete(*args, **kwargs)


class Availability_Status(models.Model):
    availability_status = models.CharField(max_length=32)


class Availability(models.Model):
    from_date = models.DateField(default=date(1000, 1, 1))
    until_date = models.DateField(default=date(5000, 1, 1))
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    availability_status = models.ManyToManyField(Availability_Status)

    @classmethod
    def create_availability(cls, store, bike):
        instance = cls(store=store, bike=bike)
        instance.save()
        instance.availability_status.set(Availability_Status.objects.filter(availability_status='Available'))
        instance.save()
        return instance


class Booking_Status(models.Model):
    booking_status = models.CharField(max_length=32)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    begin = models.DateField(null=True)
    end = models.DateField(null=True)
    string = models.CharField(max_length=5, null=True, unique=True)
    booking_status = models.ManyToManyField(Booking_Status)
    equipment = models.ManyToManyField(Equipment)


class Mail_Template(models.Model):
    subject = models.TextField(default="ERROR")
    content = models.TextField(default="ERROR")


class Comment(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    content = models.TextField(default="ERROR")
