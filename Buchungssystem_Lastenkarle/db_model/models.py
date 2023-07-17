from django.db import models


# Create your models here.
class User(models.Model):
    ASSURANCE_LEVEL = [
        ("N", "None"), ("L", "Low"), ("M", "Medium"), ("H", "High"),
    ]
    username = models.TextField(max_length=30)
    year_of_birth = models.IntegerField()
    assurance_lvl = models.CharField(max_length=1, choices=ASSURANCE_LEVEL)
    contact_data = models.TextField(default="ERROR")


class ID_Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.TextField(default="ERROR")
    last_name = models.TextField(default="ERROR")
    address = models.TextField(default="ERROR")
    date_of_verification = models.DateField(auto_now=True)
    id_number = models.TextField(max_length=3)


class OIDC_Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.TextField(default="ERROR")
    subject = models.TextField(default="ERROR")


class Local_Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.TextField(default="ERROR")
    contact_data = models.TextField(default="ERROR")


class User_Flag(models.Model):
    meaning = models.TextField(default="ERROR")


class User_Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flag = models.ForeignKey(User_Flag, on_delete=models.CASCADE)


class Store(models.Model):
    REGION = [("KA", "Karlsruhe"), ("ETT", "Ettlingen"), ("BAD", "Baden-Baden"),
              ("BRU", "Bruchsal"), ("MAL", "Malsch"), ]
    opening_hours = models.TextField(default="ERROR")
    preparation_time = models.IntegerField(default="ERROR")
    region = models.TextField(max_length=3, choices=REGION)
    address = models.TextField(default="ERROR")
    name = models.TextField(default="ERROR")


class Bike(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
