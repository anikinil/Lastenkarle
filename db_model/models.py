from django.db import models


# Create your models here.
class User(models.Model):
    ASSURANCE_LEVEL = [
        ("N", "None"), ("L", "Low"), ("M", "Medium"), ("H", "High"),
    ]
    username = models.TextField(max_length=30)
    year_of_birth = models.IntegerField
    assurance_lvl = models.CharField(max_length=1, choices=ASSURANCE_LEVEL)
    contact_data = models.TextField()


class ID_Data(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.TextField
    last_name = models.TextField
    address = models.TextField
    date_of_verification = models.DateField
    id_number = models.TextField(max_length=3)


class OIDC_Data(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.TextField
    subject = models.TextField


class Local_Data(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.TextField
    contact_data = models.TextField


class User_Flag(models.Model):
    meaning = models.TextField


class User_Status(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    flag_ID = models.ForeignKey(User_Flag, on_delete=models.CASCADE)


class Store(models.Model):
    REGION = [("KA", "Karlsruhe"), ("ETT", "Ettlingen"), ("BAD", "Baden-Baden"),
              ("BRU", "Bruchsal"), ("MAL", "Malsch"), ]
    opening_hours = models.TextField
    preparation_time = models.IntegerField
    region = models.TextField(max_length=3, choices=REGION)
    address = models.TextField


class Comment(models.Model):
    from_store_ID = models.ForeignKey(Store, on_delete=models.CASCADE)
    to_user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField


class Bike(models.Model):
    store_ID = models.ForeignKey(Store, on_delete=models.CASCADE)
    description = models.TextField
    image_link = models.TextField


class Availability(models.Model):
    from_date = models.DateField
    until_date = models.DateField
    store_ID = models.ForeignKey(Store, on_delete=models.CASCADE)
    bike_ID = models.ForeignKey(Bike, on_delete=models.CASCADE)


class Availability_Flag(models.Model):
    meaning = models.TextField


class Availability_Status(models.Model):
    availability_ID = models.ForeignKey(Availability, on_delete=models.CASCADE)
    flag_ID = models.ForeignKey(Availability_Flag, on_delete=models.CASCADE)


class Booking(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    bike_ID = models.ForeignKey(Bike, on_delete=models.CASCADE)
    begin = models.DateField
    end = models.DateField


class Booking_Flag(models.Model):
    meaning = models.TextField


class Booking_Status(models.Model):
    booking_ID = models.ForeignKey(Booking, on_delete=models.CASCADE)
    flag_ID = models.ForeignKey(Booking_Flag, on_delete=models.CASCADE)


class Mail_Template(models.Model):
    subject = models.TextField
    content = models.TextField
