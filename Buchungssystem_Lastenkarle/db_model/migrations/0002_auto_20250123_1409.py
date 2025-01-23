from django.db import migrations

user_status_labels = ['Verified', 'Deleted', 'Reminded', 'Administrator', 'Banned', 'Customer']
availability_status_labels = ['Booked', 'Available']
booking_status_labels = ['Booked', 'Internal usage', 'Picked up', 'Cancelled', 'Returned']
bike_equipment_labels = ['Lock And Key', 'Child Safety Seat And Seatbelt', 'Tarp', 'Battery', 'Charger']
region_data = [("KA", "Karlsruhe"), ("ETT", "Ettlingen"), ("BAD", "Baden-Baden"), ("BRU", "Bruchsal"), ("MAL", "Malsch"), ]


def populate_region_entries(apps, schema_editor):
    Region = apps.get_model('db_model', 'Region')

    for abbr, name in region_data:
        # Check if the equipment with the given label already exists
        if not Region.objects.filter(abbreviation=abbr, name=name).exists():
            Region.objects.create(name=name, abbreviation=abbr)

def populate_bike_equipment_entries(apps, schema_editor):
    Equipment = apps.get_model('db_model', 'Equipment')

    for label in bike_equipment_labels:
        # Check if the equipment with the given label already exists
        if not Equipment.objects.filter(equipment=label).exists():
            Equipment.objects.create(equipment=label)


def populate_availability_status_entries(apps, schema_editor):
    Availability_Status = apps.get_model('db_model', 'Availability_Status')

    for label in availability_status_labels:
        # Check if the availability status with the given label already exists
        if not Availability_Status.objects.filter(availability_status=label).exists():
            Availability_Status.objects.create(availability_status=label)


def populate_booking_status_entries(apps, schema_editor):
    Booking_Status = apps.get_model('db_model', 'Booking_Status')

    for label in booking_status_labels:
        # Check if the booking status with the given label already exists
        if not Booking_Status.objects.filter(status=label).exists():
            Booking_Status.objects.create(status=label)


def populate_user_status_entries(apps, schema_editor):
    User_Status = apps.get_model('db_model', 'User_Flag')

    for label in user_status_labels:
        # Check if the user status with the given label already exists
        if not User_Status.objects.filter(flag=label).exists():
            User_Status.objects.create(flag=label)


class Migration(migrations.Migration):
    dependencies = [
        ('db_model', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_user_status_entries),
        migrations.RunPython(populate_booking_status_entries),
        migrations.RunPython(populate_availability_status_entries),
        migrations.RunPython(populate_bike_equipment_entries),
        migrations.RunPython(populate_region_entries),
    ]
