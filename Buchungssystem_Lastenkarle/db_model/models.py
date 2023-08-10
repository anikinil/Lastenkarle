from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create internal user model here.
class UserManager(BaseUserManager):

    def create_user(self, username, password, **extra_fields):
        user = User.objects.create(**extra_fields.pop('user'))
        user.is_active = True
        user.user_status.set(User_status.objects.filter(user_status='K'))
        if user.is_superuser:
            user.user_status.set(User_status.objects.filter(user_status='I'))
        login_data = self.model(user=user, username=username, **extra_fields)
        login_data.set_password(password)
        login_data.save()
        return login_data




    def create_superuser(self, **extra_fields):
        user_data = extra_fields.pop('user', {})
        user_data['is_staff'] = True
        user_data['is_superuser'] = True
        if user_data.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if user_data.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        extra_fields['user'] = user_data
        return self.create_user(**extra_fields)

def get_store_name_from_flag(user_status_flag, store_flag):
    try:
        for flag_tuple in user_status_flag:
            if flag_tuple[0] == store_flag:
                return flag_tuple[1]
        return None  # If the store_flag is not found in the user_status_flag
    except ValueError:
        return None


class LoginData(AbstractBaseUser):
    user = models.OneToOneField('User', on_delete=models.CASCADE, null=True, blank=True)
    username = models.TextField(max_length=30, unique=True)
    password = models.TextField(default="ERROR")

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def is_staff(self):
        return self.user.is_staff

    def is_staff_of_store(self):
        user_id = self.pk
        store_flag = User.objects.get(pk=user_id).user_status.filter(user_status__startswith='S')
        for first_part, second_part in User_status.USER_STATUS_FLAG:
            if first_part == store_flag.first().user_status:
                store_name = second_part
                return Store.objects.get(name=store_name)
        return None

    def is_superuser(self):
        return self.user.is_superuser


class Store(models.Model):
    REGION = [("KA", "Karlsruhe"), ("ETT", "Ettlingen"), ("BAD", "Baden-Baden"),
              ("BRU", "Bruchsal"), ("MAL", "Malsch"), ]
    region = models.TextField(max_length=3, choices=REGION)
    address = models.TextField(default="ERROR")
    name = models.TextField(default="ERROR", unique=True)


class User_status(models.Model):
    USER_STATUS_FLAG = [
        ('A', 'Authentifiziert'),
        ('L', 'Gelöscht'),
        ('M', 'Ermahnt'),
        ('I', 'Admin'),
        ('B', 'Gebannt'),
        ('S01', 'Laden'),
        ('K', 'Kunde')
    ]
    user_status = models.CharField(max_length=3, choices=USER_STATUS_FLAG)


class User(models.Model):
    ASSURANCE_LEVEL = [
        ("N", "None"), ("L", "Low"), ("M", "Medium"), ("H", "High"),
    ]
    user_status = models.ManyToManyField(User_status)
    assurance_lvl = models.CharField(max_length=1, choices=ASSURANCE_LEVEL)
    year_of_birth = models.IntegerField(null=True)
    contact_data = models.TextField(default="ERROR")

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class OIDCLoginData(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, null=True, blank=True)
    issue = models.TextField(default="ERROR")
    subject = models.TextField(default="ERROR")


class LocalData(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.TextField(default="ERROR")
    last_name = models.TextField(default="ERROR")
    address = models.TextField(default="ERROR")
# do OIDC user also need to show documents on pickup?
# if so date_of_verification should be moved to User model
    date_of_verification = models.DateField(null=True, blank=True)
    id_number = models.TextField(max_length=3)


class Bike(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.TextField(default="ERROR")
    description = models.TextField(default="ERROR")
    image_link = models.TextField(default="ERROR")

class Availability_Status(models.Model):
    AVAILABILITY_STATUS_FLAG = [
                    ('B', 'Gebucht'),
                    ('F', 'Frei')
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
        ('B', 'Gebucht'),
        ('R', 'Reparatur'),
        ('A', 'Abgeholt'),
        ('S', 'Storniert'),
        ('Z', 'Zurückgegeben')
    ]
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS_FLAG)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    begin = models.DateField(null=True)
    end = models.DateField(null=True)
    booking_status = models.ManyToManyField(Booking_Status)


class Mail_Template(models.Model):
    subject = models.TextField(default="ERROR")
    content = models.TextField(default="ERROR")


class Comment(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    content = models.TextField(default="ERROR")
