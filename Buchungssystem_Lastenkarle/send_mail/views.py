from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import HttpResponse
from django.core.mail import EmailMessage
from Buchungssystem_Lastenkarle.settings import EMAIL_HOST_USER
from Buchungssystem_Lastenkarle.settings import ADMIN_CONTACT
from Buchungssystem_Lastenkarle.settings import CANONICAL_HOST
import pyqrcode
import os
import string
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
import urllib.parse

lastenkarle_logo_url = "https://transport.data.kit.edu/static/Lastenkarle_header.png"
spenden_link = "https://lastenkarle.de/spenden"
lastenkarle_contact_data = "Lastenrad-Initiative für die Region Karlsruhe e. V;Kronenstraße 9;76133 Karlsruhe;post@lastenkarle.de"


def testmethode(request):
    booking_ascii_string = "abcde"
    qr_code_string = urllib.parse.urljoin(urllib.parse.urljoin(CANONICAL_HOST, "booking/"), booking_ascii_string)

    return HttpResponse(qr_code_string)


def split_string_by_delimiter(input_string, delimiter):
    if not input_string:
        return []  # Return an empty list if the input string is empty
    elif not delimiter:
        return input_string
    split_array = input_string.split(delimiter)  # Split the input string using the delimiter
    split_array = [item.strip() for item in split_array]  # Remove leading and trailing whitespaces from each item
    return split_array


# TEST FUNKTION
def send_test_emails(request):
    from_email = EMAIL_HOST_USER
    recipient_list = ["carolin.schmuck@web.de"]
    store_opening_hours = "Montag: 08:00 - 18:00;Dienstag: 08:00 - 20:00;..."

    subject = "EmailTest"
    html_message = render_to_string("email_templates/AdminUserWarningNotification.html",
                                    {'username': "Hildegard von Obertupfingen",
                                     'bike_name': "feuerspuckendes Lastenfahrrad",
                                     'station_name': "Tante Ernas Sexshop",
                                     'start_date': "20.08.2023",
                                     'end_date': "21.08.2023",
                                     'store_address': "Storestraße 1, 01234 Storehausen",
                                     'store_phone_number': "012345678",
                                     'store_email': "store@mail.com",
                                     'store_opening_hours': split_string_by_delimiter(store_opening_hours, ";"),
                                     'store_website_link': "https://www.google.de/",
                                     'booking_link': "https://im-efahrer.chip.de/files/crashtest-zweispur2-2107-w83ust-6124b8f146f79.jpg?imPolicy=IfOrientation&width=720&height=405&color=%23000000&hash=83d67f1026f41d15e329202363cb4ec43d271ecf3d29815de7a4477d8705b17a",
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'spenden_link': spenden_link,
                                     'lastenkarle_contact_data': split_string_by_delimiter(lastenkarle_contact_data,
                                                                                           ";"),
                                     'admin_contact_data': ADMIN_CONTACT,
                                     'commentary': "User hat das Rad beschädigt zurückgegeben"})
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML
    email.send()
    return HttpResponse("gesendet")


def generate_qrcode(string, booking_string, bike_name, station_name, start_date, end_date, username):
    # Create a QR code instance
    qr = pyqrcode.create(string)

    # Get the absolute path of the project directory
    project_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), ".."))  # Assuming this code is in a .py file

    # Join the project directory with the desired subdirectories
    folder_path = os.path.join(project_dir, 'media', 'qr-codes')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    qr_filename = f"{booking_string}.png"
    qr_path = os.path.join(folder_path, qr_filename)
    qr.png(qr_path, scale=8)
    return qr_path


def fill_booking_attachment_template(booking_string, bike_name, station_name, start_date, end_date, username):
    template_path = 'email_templates/BookingresponseQR.html'
    context = {
        'header_image': lastenkarle_logo_url,
        'bike_name': bike_name,
        'station_name': station_name,
        'start_date': start_date,
        'end_date': end_date,
        'username': username,
        'qr_path': os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "media", "qr-codes", "%s.png" % booking_string))
    }

    html_content = render_to_string(template_path, context)
    return html_content


def create_and_save_booking_pdf_from_html(html_content, booking_string):
    project_dir = os.path.abspath(
        os.path.dirname(__file__))
    output_pdf_path = project_dir + '/pdf/%s.pdf' % (booking_string)  # Passe den Pfad an

    print(output_pdf_path)

    pdf_file = open(output_pdf_path, "wb")
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

    pdf_file.close()

    if pisa_status.err:
        return HttpResponse("Fehler beim Erstellen des PDFs")
    return output_pdf_path


def send_booking_confirmation(request, booking, user, booking_link, store_opening_hours, booking_ascii_string):
    qr_code_string = urllib.parse.urljoin(CANONICAL_HOST, "booking/", booking_ascii_string)
    qr_path = generate_qrcode(qr_code_string, booking_ascii_string, booking.bike.name, booking.station_name,
                              booking.begin, booking.end, user.username)
    attachment_html = fill_booking_attachment_template(booking_ascii_string, booking.bike.name, booking.station_name,
                                                       booking.begin, booking.end, user.username)
    attachment_path = create_and_save_booking_pdf_from_html(attachment_html, booking_ascii_string)
    with open(attachment_path, 'rb') as file:
        file_content = file.read()
    mime_type = magic.from_buffer(file_content, mime=True)

    # Extract the filename from the attachment_path
    file_name = os.path.basename(attachment_path)

    subject = "Deine Buchung von %s bei %s von %s bis %s" % (
        booking.bike.name, booking.station_name, booking.begin, booking.end)
    # Email-Template für Buchungsbestätigung mit Daten füllen
    html_message = render_to_string("email_templates/BookingMailTemplate.html",
                                    {'username': user.username,
                                     'bike_name': booking.bike.name,
                                     'station_name': booking.station_name,
                                     'booking_link': booking_link,
                                     'start_date': booking.begin,
                                     'end_date': booking.end,
                                     'store_opening_hours': split_string_by_delimiter(store_opening_hours, ";"),
                                     'store_website_link': store_website_link,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_address': booking.bike.store.address,
                                     'store_phone_number': booking.bike.store.phone_number,
                                     'store_email': booking.bike.store.email,
                                     'spenden_link': spenden_link,
                                     'lastenkarle_contact_data': split_string_by_delimiter(lastenkarle_contact_data,
                                                                                           ";")})
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML
    email.attach(file_name, file_content, mime_type)
    email.send()


def send_user_warning_to_admin(request, booking, user, commentary):
    subject = "Benutzer %s wurde ermahnt" % (user.username)
    # Email-Template für Buchungsbestätigung mit Daten füllen
    html_message = render_to_string("email_templates/AdminUserWarningNotification.html",
                                    {'username': user.username,
                                     'station_name': booking.station_name,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_address': booking.bike.store.address,
                                     'store_phone_number': booking.bike.store.phone_number,
                                     'store_email': booking.bike.store.email,
                                     'commentary': commentary})
    from_email = EMAIL_HOST_USER
    recipient_list = [ADMIN_CONTACT]
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML

    email.send()


def send_bike_drop_off_confirmation(request, booking, user):
    subject = "Statuswechsel deiner Buchung: Lastenrad %s wurde zurückgegeben" % (booking.bike.name)
    html_message = render_to_string("email_templates/BikeDropOffConfirmation.html",
                                    {'username': user.username,
                                     'bike_name': booking.bike.name,
                                     'station_name': booking.station_name,
                                     'store_website_link': store_website_link,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_address': booking.bike.store.address,
                                     'store_phone_number': booking.bike.store.phone_number,
                                     'store_email': booking.bike.store.email})
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML

    email.send()


def send_bike_pick_up_confirmation(request, booking, user):
    subject = "Statuswechsel deiner Buchung: Lastenrad %s wurde abgeholt" % (booking.bike.name)
    html_message = render_to_string("email_templates/BikeDropOffConfirmation.html",
                                    {'username': user.username,
                                     'bike_name': booking.bike.name,
                                     'station_name': booking.station_name,
                                     'store_website_link': store_website_link,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_address': booking.bike.store.address,
                                     'store_phone_number': booking.bike.store.phone_number,
                                     'store_email': booking.bike.store.email
                                     })
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML

    email.send()


def send_cancellation_confirmation(request, booking, user):
    subject = "Stornierung von Buchung %s von %s bis %s" % (booking.pk, booking.begin, booking.end)
    html_message = render_to_string("email_templates/CancellationConfirmation.html",
                                    {'username': user.username,
                                     'bike_name': booking.bike.name,
                                     'station_name': booking.station_name,
                                     'start_date': booking.begin,
                                     'end_date': booking.end,
                                     'lastenkarle_logo_url': lastenkarle_logo_url})
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML

    email.send()


def send_cancellation_through_store_confirmation(request, booking, user):
    subject = "Stornierung von Buchung %s von %s bis %s" % (booking.pk, booking.begin, booking.end)
    html_message = render_to_string("email_templates/CancellationThroughStoreConfirmation.html",
                                    {'username': user.username,
                                     'bike_name': booking.bike.name,
                                     'station_name': booking.station_name,
                                     'start_date': booking.begin,
                                     'end_date': booking.end,
                                     'lastenkarle_logo_url': lastenkarle_logo_url})
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML

    email.send()


def send_banned_mail_to_user(request, booking, user):
    subject = "Statuswechsel deines Accounts: Du wurdest gebannt"
    html_message = render_to_string("email_templates/UserBannedMail.html",
                                    {'username': user.username,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'lastenkarle_contact_data': split_string_by_delimiter(lastenkarle_contact_data,
                                                                                           ";")})
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML

    email.send()


def send_user_registered_confirmation(request, user, registration_link):
    subject = "Dein Account bei Lastenkarle: Bitte bestätige deine E-Mail"
    html_message = render_to_string("email_templates/UserRegisteredConfirmation.html",
                                    {'username': user.username,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'registration_link': registration_link})
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML

    email.send()


def send_user_verified_confirmation(request, booking, user):
    subject = "Statuswechsel deines Accounts: Du bist verifiziert"
    html_message = render_to_string("email_templates/UserVerifiedConfirmation.html",
                                    {'username': user.username,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'lastenkarle_contact_data': split_string_by_delimiter(lastenkarle_contact_data,
                                                                                           ";")})
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML

    email.send()


def send_user_warning(request, booking, user, commentary):
    subject = "Statuswechsel deines Accounts: Du wurdest ermahnt"
    html_message = render_to_string("email_templates/UserWarning.html",
                                    {'username': user.username,
                                     'station_name': booking.station_name,
                                     'commentary': commentary,
                                     'store_address': booking.bike.store.address,
                                     'store_phone_number': booking.bike.store.phone_number,
                                     'store_email': booking.bike.store.email,
                                     'lastenkarle_logo_url': lastenkarle_logo_url})
    from_email = EMAIL_HOST_USER
    recipient_list = [user.contact_data]
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'  # Setze den Inhaltstyp auf HTML

    email.send()
