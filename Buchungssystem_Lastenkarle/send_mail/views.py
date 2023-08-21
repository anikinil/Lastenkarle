from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import HttpResponse
from django.core.mail import EmailMessage

lastenkarle_logo_url = "https://transport.data.kit.edu/static/media/Lastenkarle_header.png"


def send_booking_confirmation(request, booking, user, booking_link, store_openinghours, store_websitelink):
    subject = "Deine Buchung von %s bei %s von %s bis %s" % (
        booking.bike.name, booking.station_name, booking.begin, booking.end)
    # Email-Template für Buchungsbestätigung mit Daten füllen
    html_message = render_to_string("templates/email_templates/BookingMailTemplate.html",
                                    {'username': user.username, 'bike_name': booking.bike.name,
                                     'station_name': booking.station_name, 'booking_link': booking_link,
                                     'start_date': booking.begin, 'end_date': booking.end,
                                     'store_address': booking.bike.store.address,
                                     'store_openinghours': store_openinghours, 'store_websitelink': store_websitelink,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_contact_data': booking.bike.store.contact_data})
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]

    email = EmailMessage(subject, html_message, from_email, recipient_list)
    # QR-Code generieren und in den Anhang als pdf einfügen
    # attachment_path = "/pfad/zur/datei.txt"  # Pfad zur Anhangsdatei anpassen
    # with open(attachment_path, 'rb') as attachment_file:
    #    email.attach("attachment.txt", attachment_file.read(), "text/plain")

    email.send()


def send_user_warning_to_admin(request, booking, user, commentary):
    subject = "Benutzer %s wurde ermahnt" % (user.username)
    # Email-Template für Buchungsbestätigung mit Daten füllen
    html_message = render_to_string("templates/email_templates/AdminUserWarningNotification.html",
                                    {'username': user.username, 'bike_name': booking.bike.name,
                                     'station_name': booking.station_name,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_contact_data': booking.bike.store.contact_data,
                                     'commentary': commentary})
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


def send_bike_drop_off_confirmation(request, booking, user, store_websitelink, commentary):
    subject = "Statuswechsel deiner Buchung: Lastenrad %s wurde zurückgegeben" % (booking.bike.name)
    html_message = render_to_string("templates/email_templates/BikeDropOffConfirmation.html",
                                    {'username': user.username, 'bike_name': booking.bike.name,
                                     'station_name': booking.station_name, 'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_contact_data': booking.bike.store.contact_data,
                                     'commentary': commentary, 'store_websitelink': store_websitelink, })
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


def send_bike_pick_up_confirmation(request, booking, user, store_websitelink, commentary):
    subject = "Statuswechsel deiner Buchung: Lastenrad %s wurde abgeholt" % (booking.bike.name)
    html_message = render_to_string("templates/email_templates/BikeDropOffConfirmation.html",
                                    {'username': user.username, 'bike_name': booking.bike.name,
                                     'station_name': booking.station_name, 'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_contact_data': booking.bike.store.contact_data,
                                     'commentary': commentary, 'store_websitelink': store_websitelink, })
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

