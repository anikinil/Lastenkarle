from datetime import timedelta
from db_model.models import *
from django.db.models import Q
from datetime import datetime
from send_mail.views import send_cancellation_through_store_confirmation


def merge_availabilities_from_until_algorithm(from_date, until_date, store, bike):
    from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
    until_date = datetime.strptime(until_date, '%Y-%m-%d').date()
    interval = Availability.objects.filter(from_date__gte=from_date,
                                           until_date__lte=until_date,
                                           store=store,
                                           bike=bike)
    filtered_interval = None
    if interval.exists():
        left_from_date = Availability.objects.get(until_date=(interval.first().from_date - timedelta(days=1)).isoformat(),
                                                  store=store,
                                                  bike=bike)
        right_from_date = Availability.objects.get(from_date=(interval.last().until_date + timedelta(days=1)).isoformat(),
                                                   store=store,
                                                   bike=bike)
        filtered_interval = Availability.objects.filter(
            Q(from_date__gte=from_date.isoformat(), until_date__lte=until_date.isoformat()) |
            Q(until_date=left_from_date.until_date) |
            Q(from_date=right_from_date.from_date),
            store=store,
            bike=bike,
            availability_status=Availability_Status.objects.get(availability_status='Booked'))
    else:
        left_availability = Availability.objects.filter(
            Q(from_date__lt=from_date.isoformat()) &
            Q(store=store) &
            Q(bike=bike)
        ).order_by('from_date').last()

        if left_availability is not None and not \
                left_availability.availability_status == Availability_Status.objects.get(availability_status='Booked'):
            left_availability = None

        right_availability = Availability.objects.filter(
            Q(from_date__gte=from_date.isoformat()) &
            Q(store=store) &
            Q(bike=bike),
        ).order_by('from_date').first()

        if right_availability is not None and not \
                right_availability.availability_status == Availability_Status.objects.get(availability_status='Booked'):
            right_availability = None

        if left_availability is not None and right_availability is not None:
            filtered_interval = [left_availability, right_availability]
        elif left_availability is not None:
            filtered_interval = [left_availability]
        elif right_availability is not None:
            filtered_interval = [right_availability]
        else:
            return True
    if filtered_interval is None:
        return True
    for ava in filtered_interval:
        booking = Booking.objects.filter(begin=ava.from_date.isoformat(),
                                         end=ava.until_date.isoformat(),
                                         bike=ava.bike)
        if booking.filter(booking_status=Booking_Status.objects.get(booking_status='Picked up')).exists():
            return False
    for ava in filtered_interval:
        booking = Booking.objects.get(
            Q(begin=ava.from_date.isoformat()) &
            Q(end=ava.until_date.isoformat()) &
            Q(bike=ava.bike) &
            (Q(booking_status__booking_status='Booked') | Q(booking_status__booking_status='Internal usage'))
        )
        booking.booking_status.clear()
        booking.booking_status.set(Booking_Status.objects.filter(booking_status='Cancelled'))
        send_cancellation_through_store_confirmation(booking)
        booking.string = None
        booking.save()
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

    new_from_date = booking.begin.isoformat()
    new_until_date = booking.end.isoformat()
    if left_side.filter(availability_status=Availability_Status.objects.get(availability_status='Booked')).exists():
        new_from_date = begin_booking
    else:
        if left_side.filter(availability_status=Availability_Status.objects.get(availability_status='Available')).exists():
            new_from_date = left_side.first().from_date
            left_side.delete()

    right_side = Availability.objects.filter(from_date=(end_booking + timedelta(days=1)).isoformat(),
                                             bike_id=booking.bike.pk,
                                             store_id=booking.bike.store.pk)

    if right_side.filter(availability_status=Availability_Status.objects.get(availability_status='Booked')).exists():
        new_until_date = end_booking
    else:
        if right_side.filter(availability_status=Availability_Status.objects.get(availability_status='Available')).exists():
            new_until_date = right_side.first().until_date
            right_side.delete()

    merged_availability = Availability.objects.create(from_date=new_from_date,
                                                      until_date=new_until_date,
                                                      bike_id=booking.bike.pk,
                                                      store_id=booking.bike.store.pk)
    merged_availability.availability_status.set(Availability_Status.objects.filter(availability_status='Available'))
    booking_availability.delete()


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
    availability_of_booking.availability_status.set(Availability_Status.objects.filter(availability_status='Booked'))
    if not availability_of_booking.from_date == to_edit.first().from_date:
        new_begin = to_edit.first().from_date
        new_end = booking.begin - timedelta(days=1)
        left_side = Availability.objects.create(from_date=new_begin,
                                             until_date=new_end,
                                             bike_id=booking.bike.pk,
                                             store_id=booking.bike.store.pk)
        left_side.availability_status.set(Availability_Status.objects.filter(availability_status='Available'))
    if not availability_of_booking.until_date == to_edit.first().until_date:
        new_begin = booking.end + timedelta(days=1)
        new_end = to_edit.first().until_date
        right_side = Availability.objects.create(from_date=new_begin,
                                            until_date=new_end,
                                            bike_id=booking.bike.pk,
                                            store_id=booking.bike.store.pk)
        right_side.availability_status.set(Availability_Status.objects.filter(availability_status='Available'))
    to_edit.first().delete()
