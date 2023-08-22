from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import HttpResponse
from django.core.mail import EmailMessage
from Buchungssystem_Lastenkarle.settings import EMAIL_HOST_USER
#TODO: Admin Email Adresse im Env_vars file eintragen
from Buchungssystem_Lastenkarle.settings import ADMIN_CONTACT

lastenkarle_logo_url = "https://transport.data.kit.edu/static/Lastenkarle_header.png"
spenden_link = "https://lastenkarle.de/spenden"
lastenkarle_contact_data = "Lastenrad-Initiative für die Region Karlsruhe e. V;Kronenstraße 9;76133 Karlsruhe;post@lastenkarle.de"
splitted_lastenkarle_contact_data = split_string_by_delimiter(lastenkarle_contact_data, ";")


# TEST FUNKTION
def send_test_emails(request):
    from_email = EMAIL_HOST_USER
    recipient_list = ["carolin.schmuck@web.de"]
    store_address = "Storestr. 1;01234 Storehausen"
    store_contact_data = "store@mail.com;012345678"
    store_opening_hours = "Montag: 08:00 - 18:00;Dienstag: 08:00 - 20:00;..."
    splitted_store_address = split_string_by_delimiter(store_address, ";")
    splitted_lastenkarle_contact_data = split_string_by_delimiter(lastenkarle_contact_data, ";")
    splitted_store_contact_data = split_string_by_delimiter(store_contact_data, ";")
    splitted_store_opening_hours = split_string_by_delimiter(store_opening_hours, ";")


    subject = "Buchungsbestätigung"
    html_message = render_to_string("email_templates/BookingMailTemplate.html",
                                    {'username': "Hildegard von Obertupfingen",
                                     'bike_name': "feuerspuckendes Lastenfahrrad",
                                     'station_name': "Tante Ernas Sexshop",
                                     'start_date': "20.08.2023",
                                     'end_date': "21.08.2023",
                                     'store_address': splitted_store_address,
                                     'store_contact_data': splitted_store_contact_data,
                                     'store_website_link': "https://www.google.de/",
                                     'booking_link': "https://im-efahrer.chip.de/files/crashtest-zweispur2-2107-w83ust-6124b8f146f79.jpg?imPolicy=IfOrientation&width=720&height=405&color=%23000000&hash=83d67f1026f41d15e329202363cb4ec43d271ecf3d29815de7a4477d8705b17a",
                                     'store_opening_hours': splitted_store_opening_hours,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'spenden_link': spenden_link,
                                     'lastenkarle_contact_data': splitted_lastenkarle_contact_data,
                                     'commentary': "User hat das Rad beschädigt zurückgegeben"})
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML
    email.send()
    return HttpResponse("gesendet")


def split_string_by_delimiter(input_string, delimiter):
    if not input_string:
        return []  # Return an empty list if the input string is empty
    elif not delimiter:
        return input_string
    split_array = input_string.split(delimiter)  # Split the input string using a comma as the delimiter
    split_array = [item.strip() for item in split_array]  # Remove leading and trailing whitespaces from each item
    return split_array

def send_booking_confirmation(request, booking, user, booking_link, store_opening_hours, store_website_link):
    subject = "Deine Buchung von %s bei %s von %s bis %s" % (
        booking.bike.name, booking.station_name, booking.begin, booking.end)
    # Email-Template für Buchungsbestätigung mit Daten füllen

    store_address = booking.bike.store.address
    store_contact_data = booking.bike.store.contact_data
    splitted_store_address = split_string_by_delimiter(store_address, ";")
    splitted_store_contact_data = split_string_by_delimiter(store_contact_data, ";")
    splitted_store_opening_hours = split_string_by_delimiter(store_opening_hours, ";")

    html_message = render_to_string("email_templates/BookingMailTemplate.html",
                                    {'username': user.username,
                                     'bike_name': booking.bike.name,
                                     'station_name': booking.station_name,
                                     'booking_link': booking_link,
                                     'start_date': booking.begin,
                                     'end_date': booking.end,
                                     'store_address': splitted_store_address,
                                     'store_opening_hours': splitted_store_opening_hours,
                                     'store_website_link': store_website_link,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_contact_data': splitted_store_contact_data,
                                     'spenden_link': spenden_link,
                                     'lastenkarle_contact_data': splitted_lastenkarle_contact_data})
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML

    email.send()


def test_send_booking_confirmation(request):
    subject = "Deine Buchung von %s bei %s von %s bis %s" % (
        "feuerspuckendes Lastenfahrrad", "Tante Ernas Sexshop", "20.08.2023", "21.08.2023")
    html_message = render_to_string("email_templates/BookingMailTemplate.html",
                                    {'username': "Hildegard von Obertupfingen",
                                     'bike_name': "feuerspuckendes Lastenfahrrad",
                                     'station_name': "Tante Ernas Sexshop",
                                     'pickup_adress': "irgendeine Abhol Straße",
                                     'start_date': "20.08.2023", 'end_date': "21.08.2023",
                                     'store_contact_data': "Store Contakt juhu",
                                     'store_website_link': "https://www.google.de/",
                                     'booking_link': "https://im-efahrer.chip.de/files/crashtest-zweispur2-2107-w83ust-6124b8f146f79.jpg?imPolicy=IfOrientation&width=720&height=405&color=%23000000&hash=83d67f1026f41d15e329202363cb4ec43d271ecf3d29815de7a4477d8705b17a",
                                     'store_openinghours': "immer",
                                     })
    from_email = EMAIL_HOST_USER
    recipient_list = ["carolin.schmuck@web.de"]
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML

    email.send()

    return HttpResponse("Email gesendet")


def send_user_warning_to_admin(request, booking, user, commentary):
    subject = "Benutzer %s wurde ermahnt" % (user.username)
    # Email-Template für Buchungsbestätigung mit Daten füllen
    html_message = render_to_string("templates/email_templates/AdminUserWarningNotification.html",
                                    {'username': user.username,
                                     'station_name': booking.station_name,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_contact_data': splitted_store_contact_data,
                                     'commentary': commentary})
    from_email = EMAIL_HOST_USER
    recipient_list = [ADMIN_CONTACT]
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML

    email.send()


def send_bike_drop_off_confirmation(request, booking, user):
    subject = "Statuswechsel deiner Buchung: Lastenrad %s wurde zurückgegeben" % (booking.bike.name)
    html_message = render_to_string("templates/email_templates/BikeDropOffConfirmation.html",
                                    {'username': user.username,
                                     'bike_name': booking.bike.name,
                                     'station_name': booking.station_name,
                                     'store_website_link': store_website_link,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_contact_data': splitted_store_contact_data})
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


def send_bike_pick_up_confirmation(request, booking, user):
    subject = "Statuswechsel deiner Buchung: Lastenrad %s wurde abgeholt" % (booking.bike.name)
    html_message = render_to_string("templates/email_templates/BikeDropOffConfirmation.html",
                                    {'username': user.username,
                                     'bike_name': booking.bike.name,
                                     'station_name': booking.station_name,
                                     'store_website_link': store_website_link,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_contact_data': splitted_store_contact_data})
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


def send_cancellation_confirmation(request, booking, user):
    subject = "Stornierung von Buchung %s von %s bis %s" % (booking.pk, booking.begin, booking.end)
    html_message = render_to_string("templates/email_templates/CancellationConfirmation.html",
                                    {'username': user.username, 'bike_name': booking.bike.name,
                                     'station_name': booking.station_name, 'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'start_date': booking.begin, 'end_date': booking.end})
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


def send_cancellation_through_store_confirmation(request, booking, user):
    subject = "Stornierung von Buchung %s von %s bis %s" % (booking.pk, booking.begin, booking.end)
    html_message = render_to_string("templates/email_templates/CancellationThroughStoreConfirmation.html",
                                    {'username': user.username, 'bike_name': booking.bike.name,
                                     'station_name': booking.station_name, 'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'start_date': booking.begin, 'end_date': booking.end})
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


def send_banned_mail_to_user(request, booking, user):
    subject = "Statuswechsel deines Accounts: Du wurdest gebannt"
    html_message = render_to_string("templates/email_templates/UserBannedMail.html",
                                    {'username': user.username, 'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_contact_data': booking.bike.store.contact_data})
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


def send_user_registered_confirmation(request, user, registration_link):
    subject = "Dein Account bei Lastenkarle: Bitte bestätige deine E-Mail"
    html_message = render_to_string("templates/email_templates/UserRegisteredConfirmation.html",
                                    {'username': user.username, 'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'registration_link': registration_link})
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


def send_user_verified_confirmation(request, booking, user, admin_contact_data):
    subject = "Statuswechsel deines Accounts: Du bist verifiziert"
    html_message = render_to_string("templates/email_templates/UserVerifiedConfirmation.html",
                                    {'username': user.username, 'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'admin_contact_data': admin_contact_data})
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


def send_user_warning(request, booking, user, admin_contact_data, commentary):
    subject = "Statuswechsel deines Accounts: Du wurdest ermahnt"
    html_message = render_to_string("templates/email_templates/UserWarning.html",
                                    {'username': user.username,
                                     'station_name': booking.station_name,
                                     'commentary': commentary,
                                     'station_contact_data': booking.bike.store.contact_data,
                                     'lastenkarle_logo_url': lastenkarle_logo_url})
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
