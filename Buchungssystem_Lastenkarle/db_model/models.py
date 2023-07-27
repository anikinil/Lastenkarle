from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create internal user model here.
class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff = True")

        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser = True")
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    ASSURANCE_LEVEL = [
        ("N", "None"), ("L", "Low"), ("M", "Medium"), ("H", "High"),
    ]
    username = models.TextField(max_length=30, unique=True)
    year_of_birth = models.IntegerField(null=True)
    assurance_lvl = models.CharField(default="N", max_length=1, choices=ASSURANCE_LEVEL)
    contact_data = models.TextField(default="ERROR")
    first_name = models.TextField(default="ERROR")
    last_name = models.TextField(default="ERROR")
    address = models.TextField(default="ERROR")
    date_of_verification = models.DateField(auto_now=True)
    id_number = models.TextField(max_length=3)
    password = models.TextField(default="ERROR")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True


# Create your models here.

class UserI(models.Model):
    ASSURANCE_LEVEL = [
        ("N", "None"), ("L", "Low"), ("M", "Medium"), ("H", "High"),
    ]
    username = models.TextField(max_length=30)
    year_of_birth = models.IntegerField()
    assurance_lvl = models.CharField(max_length=1, choices=ASSURANCE_LEVEL)
    contact_data = models.TextField(default="ERROR")


class ID_Data(models.Model):
    user = models.ForeignKey(UserI, on_delete=models.CASCADE)
    first_name = models.TextField(default="ERROR")
    last_name = models.TextField(default="ERROR")
    address = models.TextField(default="ERROR")
    date_of_verification = models.DateField(auto_now=True)
    id_number = models.TextField(max_length=3)


class Local_Data(models.Model):
    user = models.ForeignKey(UserI, on_delete=models.CASCADE)
    password = models.TextField(default="ERROR")


class OIDC_Data(models.Model):
    user = models.ForeignKey(UserI, on_delete=models.CASCADE)
    issue = models.TextField(default="ERROR")
    subject = models.TextField(default="ERROR")


class User_Flag(models.Model):
    meaning = models.TextField(default="ERROR")


class User_Status(models.Model):
    user = models.ForeignKey(UserI, on_delete=models.CASCADE)
    flag = models.ForeignKey(User_Flag, on_delete=models.CASCADE)


class Store(models.Model):
    REGION = [("KA", "Karlsruhe"), ("ETT", "Ettlingen"), ("BAD", "Baden-Baden"),
              ("BRU", "Bruchsal"), ("MAL", "Malsch"), ]
    region = models.TextField(max_length=3, choices=REGION)
    address = models.TextField(default="ERROR")
    name = models.TextField(default="ERROR")


class Bike(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.TextField(default="ERROR")
    description = models.TextField(default="ERROR")
    image_link = models.TextField(default="ERROR")


class Availability(models.Model):
    from_date = models.DateField(auto_now=True)
    until_date = models.DateField(auto_now=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)


class Availability_Flag(models.Model):
    meaning = models.TextField(default="ERROR")


class Availability_Status(models.Model):
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    flag = models.ForeignKey(Availability_Flag, on_delete=models.CASCADE)


class Booking(models.Model):
    user = models.ForeignKey(UserI, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    begin = models.DateField(auto_now=True)
    end = models.DateField(auto_now=True)


class Booking_Flag(models.Model):
    meaning = models.TextField(default="ERROR")


class Booking_Status(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    flag = models.ForeignKey(Booking_Flag, on_delete=models.CASCADE)


class Mail_Template(models.Model):
    subject = models.TextField(default="ERROR")
    content = models.TextField(default="ERROR")


class Comment(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    content = models.TextField(default="ERROR")
