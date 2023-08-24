from django.db import migrations

user_status_labels = ['Verified', 'Deleted', 'Reminded', 'Administrator', 'Banned', 'Customer']
availability_status_labels = ['Booked', 'Available']
booking_status_labels = ['Booked', 'Internal usage', 'Picked up', 'Cancelled', 'Returned']
bike_equipment_labels = ['Lock And Key', 'Child Safety Seat And Seatbelt', 'Tarp', 'Battery', 'Charger']


def populate_bike_equipment_entries(apps, schema_editor):
    Equipment = apps.get_model('db_model', 'Equipment')

    for label in bike_equipment_labels:
        Equipment.objects.create(equipment=label)


def populate_availability_status_entries(apps, schema_editor):
    Availability_Status = apps.get_model('db_model', 'Availability_Status')

    for label in availability_status_labels:
        Availability_Status.objects.create(availability_status=label)


def populate_booking_status_entries(apps, schema_editor):
    Booking_Status = apps.get_model('db_model', 'Booking_Status')

    for label in booking_status_labels:
        Booking_Status.objects.create(booking_status=label)


def populate_user_status_entries(apps, schema_editor):
    User_Status = apps.get_model('db_model', 'User_Status')

    for label in user_status_labels:
        User_Status.objects.create(user_status=label)




class Migration(migrations.Migration):

    dependencies = [
        ('db_model', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_user_status_entries),
        migrations.RunPython(populate_booking_status_entries),
        migrations.RunPython(populate_availability_status_entries),
        migrations.RunPython(populate_bike_equipment_entries),
    ] 