from datetime import timedelta
from db_model.models import *
from django.db.models import Q
from datetime import datetime

def merge_availabilities_from_until_algorithm(from_date, until_date, store, bike):
    from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
    until_date = datetime.strptime(until_date, '%Y-%m-%d').date()
    interval = Availability.objects.filter(from_date__gte=from_date,
                                           until_date__lte=until_date,
                                           store=store,
                                           bike=bike)
    left_from_date = Availability.objects.get(until_date=(interval.first().from_date - timedelta(days=1)).isoformat(),
                                              store=store,
                                              bike=bike)
    right_from_date = Availability.objects.get(from_date=(interval.last().until_date + timedelta(days=1)).isoformat(),
                                               store=store,
                                               bike=bike)
    interval = Availability.objects.filter(
        Q(from_date__gte=from_date.isoformat(), until_date__lte=until_date.isoformat()) |
        Q(until_date=left_from_date.until_date) |
        Q(from_date=right_from_date.from_date),
        store=store,
        bike=bike
    )
    # issue: filtering for those objects which have availability of B  so the issue is filering the queryset

    filtered_interval = Availability.objects.filter(
        Q(from_date__gte=from_date.isoformat(), until_date__lte=until_date.isoformat()) |
        Q(until_date=left_from_date.until_date) |
        Q(from_date=right_from_date.from_date),
        store=store,
        bike=bike,
        availability_status=Availability_Status.objects.get(availability_status='B'))
    for ava in filtered_interval:
        booking = Booking.objects.filter(begin=ava.from_date.isoformat(),
                                         end=ava.until_date.isoformat(),
                                         bike=ava.bike)
        if booking.filter(booking_status=Booking_Status.objects.get(booking_status='A')).exists():
            return False

    for ava in filtered_interval:
        booking = Booking.objects.get(begin=ava.from_date.isoformat(),
                                      end=ava.until_date.isoformat(),
                                      bike=ava.bike)
        booking.booking_status.clear()
        booking.booking_status.set(Booking_Status.objects.filter(booking_status='S'))
        merge_availabilities_algorithm(booking)
    return True

def merge_availabilities_algorithm(booking):
    begin_booking = booking.begin
    end_booking = booking.end

    booking_availability = Availability.objects.filter(from_date=begin_booking.isoformat(),
                                                       until_date=end_booking.isoformat(),
                                                       bike_id=booking.bike.pk,
                                                       store_id=booking.bike.store.pk)
    left_side = Availability.objects.filter(until_date=(begin_booking - timedelta(days=1)).isoformat(),
                                            bike_id=booking.bike.pk,
                                            store_id=booking.bike.store.pk)

    if left_side.filter(availability_status=Availability_Status.objects.get(availability_status='B')).exists():
        new_from_date = begin_booking
    else:
        new_from_date = left_side.first().from_date
        left_side.delete()

    right_side = Availability.objects.filter(from_date=(end_booking + timedelta(days=1)).isoformat(),
                                             bike_id=booking.bike.pk,
                                             store_id=booking.bike.store.pk)

    if right_side.filter(availability_status=Availability_Status.objects.get(availability_status='B')).exists():
        new_until_date = end_booking
    else:
        new_until_date = right_side.first().until_date
        right_side.delete()

    booking_availability.delete()
    merged_availability = Availability.objects.create(from_date=new_from_date,
                                                      until_date=new_until_date,
                                                      bike_id=booking.bike.pk,
                                                      store_id=booking.bike.store.pk)
    merged_availability.availability_status.set(Availability_Status.objects.filter(availability_status='F'))

def split_availabilities_algorithm(booking):
    begin_booking = booking.begin
    end_booking = booking.end
    to_edit = Availability.objects.filter(from_date__lte=begin_booking.isoformat(),
                                          until_date__gte=end_booking.isoformat(),
                                          bike_id=booking.bike.pk,
                                          store_id=booking.bike.store.pk)
    availability_of_booking = Availability.objects.create(from_date=begin_booking,
                                                          until_date=end_booking,
                                                          bike_id=booking.bike.pk,
                                                          store_id=booking.bike.store.pk)
    availability_of_booking.availability_status.set(Availability_Status.objects.filter(availability_status='B'))
    if not availability_of_booking.from_date == to_edit.first().from_date:
        new_begin = to_edit.first().from_date
        new_end = booking.begin - timedelta(days=1)
        left_side = Availability.objects.create(from_date=new_begin,
                                             until_date=new_end,
                                             bike_id=booking.bike.pk,
                                             store_id=booking.bike.store.pk)
        left_side.availability_status.set(Availability_Status.objects.filter(availability_status='F'))
    if not availability_of_booking.until_date == to_edit.first().until_date:
        new_begin = booking.end + timedelta(days=1)
        new_end = to_edit.first().until_date
        right_side = Availability.objects.create(from_date=new_begin,
                                            until_date=new_end,
                                            bike_id=booking.bike.pk,
                                            store_id=booking.bike.store.pk)
        right_side.availability_status.set(Availability_Status.objects.filter(availability_status='F'))
    to_edit.first().delete()
