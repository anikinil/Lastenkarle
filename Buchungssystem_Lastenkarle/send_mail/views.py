from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import HttpResponse
from django.core.mail import EmailMessage
from Buchungssystem_Lastenkarle.settings import EMAIL_HOST_USER
from Buchungssystem_Lastenkarle.settings import CANONICAL_HOST
import pyqrcode
import os
import string
import magic
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
import urllib.parse
import api.configs.ConfigFunctions
from db_model.models import User_Status
from db_model.models import User
from configs.global_variables import lastenkarle_logo_url
from configs.global_variables import spenden_link
from configs.global_variables import lastenkarle_contact_data


def send_booking_confirmation(booking):
    # Prepare the booking link
    booking_link = urllib.parse.urljoin(urllib.parse.urljoin(CANONICAL_HOST, "booking/"), booking.string)
    generate_qrcode(booking_link, booking.string)
    # fill attachment template
    attachment_html = fill_booking_attachment_template(booking.string, booking.bike.name, booking.bike.store.name,
                                                       booking.begin, booking.end, booking.user.username)
    # create attachment
    attachment_path = create_and_save_booking_pdf_from_html(attachment_html, booking.string)
    with open(attachment_path, 'rb') as file:
        file_content = file.read()
    mime_type = magic.from_buffer(file_content, mime=True)

    # Extract the filename from the attachment_path
    file_name = os.path.basename(attachment_path)
    # get the formatted, readable opening hours for the store
    opening_hours = api.configs.ConfigFunctions.format_opening_hours(booking.bike.store.name)
    # set email subject
    subject = "Deine Buchung von %s bei %s von %s bis %s" % (
        booking.bike.name, booking.bike.store.name, booking.begin, booking.end)
    # fill email message template with content
    html_message = render_to_string("email_templates/BookingMailTemplate.html",
                                    {'username': booking.user.username,
                                     'bike_name': booking.bike.name,
                                     'store_name': booking.bike.store.name,
                                     'booking_link': booking_link,
                                     'start_date': booking.begin,
                                     'end_date': booking.end,
                                     'store_opening_hours': opening_hours,
                                     'booking_equipment': format_equipment(booking.equipment.all()),
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_address': booking.bike.store.address,
                                     'store_phone_number': booking.bike.store.phone_number,
                                     'store_email': booking.bike.store.email,
                                     'spenden_link': spenden_link,
                                     'lastenkarle_contact_data': split_string_by_delimiter(lastenkarle_contact_data,
                                                                                           ";")})
    # set email-address to send from
    from_email = EMAIL_HOST_USER
    # set email-address to send at
    recipient_list = [booking.user.contact_data]
    # create email
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'
    # add attachment
    email.attach(file_name, file_content, mime_type)
    # send email
    email.send()


def send_user_warning_to_admins(booking):
    # set email subject
    subject = "Benutzer %s wurde ermahnt" % (booking.user.username)
    # fill email template with content
    html_message = render_to_string("email_templates/AdminUserWarningNotification.html",
                                    {'username': booking.user.username,
                                     'store_name': booking.bike.store.name,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_address': booking.bike.store.address,
                                     'store_phone_number': booking.bike.store.phone_number,
                                     'store_email': booking.bike.store.email,
                                     'comment': booking.comment})
    # set email-address to send from
    from_email = EMAIL_HOST_USER
    # set email-address to send at
    recipient_list = list_admin_emails()
    # create email
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'
    # send email
    email.send()


def send_bike_drop_off_confirmation(booking):
    # set email subject
    subject = "Statuswechsel deiner Buchung: Lastenrad %s wurde zurückgegeben" % (booking.bike.name)
    # fill email template with content
    html_message = render_to_string("email_templates/BikeDropOffConfirmation.html",
                                    {'username': booking.user.username,
                                     'bike_name': booking.bike.name,
                                     'store_name': booking.bike.store.name,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_address': booking.bike.store.address,
                                     'store_phone_number': booking.bike.store.phone_number,
                                     'store_email': booking.bike.store.email})
    # set email-address to send from
    from_email = EMAIL_HOST_USER
    # set email-address to send at
    recipient_list = [booking.user.contact_data]
    # create email
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'
    # send email
    email.send()


def send_bike_pick_up_confirmation(booking):
    # set email subject
    subject = "Statuswechsel deiner Buchung: Lastenrad %s wurde abgeholt" % (booking.bike.name)
    # fill email template with content
    html_message = render_to_string("email_templates/BikePickUpConfirmation.html",
                                    {'username': booking.user.username,
                                     'bike_name': booking.bike.name,
                                     'store_name': booking.bike.store.name,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'store_address': booking.bike.store.address,
                                     'store_phone_number': booking.bike.store.phone_number,
                                     'store_email': booking.bike.store.email
                                     })
    # set email-address to send from
    from_email = EMAIL_HOST_USER
    # set email-address to send at
    recipient_list = [booking.user.contact_data]
    # create email
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'
    # send email
    email.send()


def send_cancellation_confirmation(booking):
    # set email subject
    subject = "Stornierung deiner Buchung von %s bis %s" % (booking.begin, booking.end)
    # fill email template with content
    html_message = render_to_string("email_templates/CancellationConfirmation.html",
                                    {'username': booking.user.username,
                                     'bike_name': booking.bike.name,
                                     'store_name': booking.bike.store.name,
                                     'start_date': booking.begin,
                                     'end_date': booking.end,
                                     'lastenkarle_logo_url': lastenkarle_logo_url})
    # set email-address to send from
    from_email = EMAIL_HOST_USER
    # set email-address to send at
    recipient_list = [booking.user.contact_data]
    # create email
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'
    # send email
    email.send()


def send_cancellation_through_store_confirmation(booking):
    # set email subject
    subject = "Stornierung deiner Buchung von %s bis %s" % (booking.begin, booking.end)
    # fill email template with content
    html_message = render_to_string("email_templates/CancellationThroughStoreConfirmation.html",
                                    {'username': booking.user.username,
                                     'bike_name': booking.bike.name,
                                     'store_name': booking.bike.store.name,
                                     'start_date': booking.begin,
                                     'end_date': booking.end,
                                     'lastenkarle_logo_url': lastenkarle_logo_url})
    # set email-address to send from
    from_email = EMAIL_HOST_USER
    # set email-address to send at
    recipient_list = [booking.user.contact_data]
    # create email
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'
    # send email
    email.send()


def send_banned_mail_to_user(user):
    # set email subject
    subject = "Statuswechsel deines Accounts: Du wurdest gebannt"
    # fill email template with content
    html_message = render_to_string("email_templates/UserBannedMail.html",
                                    {'username': user.username,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'lastenkarle_contact_data': split_string_by_delimiter(lastenkarle_contact_data,
                                                                                           ";")})
    # set email-address to send from
    from_email = EMAIL_HOST_USER
    # set email-address to send at
    recipient_list = [user.contact_data]
    # create email
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'
    # send email
    email.send()


def send_user_registered_confirmation(user, registration_link):
    # set email subject
    subject = "Dein Account bei Lastenkarle: Bitte bestätige deine E-Mail"
    # fill email template with content
    html_message = render_to_string("email_templates/UserRegisteredConfirmation.html",
                                    {'username': user.username,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'registration_link': registration_link})
    # set email-address to send from
    from_email = EMAIL_HOST_USER
    # set email-address to send at
    recipient_list = [user.contact_data]
    # create email
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'
    # send email
    email.send()


def send_user_verified_confirmation(user):
    registration_link = urllib.parse.urljoin(urllib.parse.urljoin(CANONICAL_HOST, user.pk), user.verification_string)
    # set email subject
    subject = "Statuswechsel deines Accounts: Du bist verifiziert"
    # fill email template with content
    html_message = render_to_string("email_templates/UserVerifiedConfirmation.html",
                                    {'username': user.username,
                                     'registration_link': registration_link,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'lastenkarle_contact_data': split_string_by_delimiter(lastenkarle_contact_data,
                                                                                           ";")})
    # set email-address to send from
    from_email = EMAIL_HOST_USER
    # set email-address to send at
    recipient_list = [user.contact_data]
    # create email
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'
    # send email
    email.send()


def send_user_changed_mail(user):
    verification_link = urllib.parse.urljoin(urllib.parse.urljoin(CANONICAL_HOST, user.pk), user.verification_string)
    # set email subject
    subject = "Dein Account bei Lastenkarle: Bitte bestätige deine E-Mail"
    # fill email template with content
    html_message = render_to_string("email_templates/EmailChangedTemplate.html",
                                    {'username': user.username,
                                     'verification_string': verification_link,
                                     'lastenkarle_logo_url': lastenkarle_logo_url,
                                     'registration_link': registration_link})
    # set email-address to send from
    from_email = EMAIL_HOST_USER
    # set email-address to send at
    recipient_list = [user.contact_data]
    # create email
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'
    # send email
    email.send()



def send_user_warning(booking):
    # set email subject
    subject = "Statuswechsel deines Accounts: Du wurdest ermahnt"
    # fill email template with content
    html_message = render_to_string("email_templates/UserWarning.html",
                                    {'username': booking.user.username,
                                     'store_name': booking.bike.store.name,
                                     'comment': booking.comment,
                                     'store_address': booking.bike.store.address,
                                     'store_phone_number': booking.bike.store.phone_number,
                                     'store_email': booking.bike.store.email,
                                     'lastenkarle_logo_url': lastenkarle_logo_url})
    # set email-address to send from
    from_email = EMAIL_HOST_USER
    # set email-address to send at
    recipient_list = [booking.user.contact_data]
    # create email
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html'
    # send email
    email.send()


def split_string_by_delimiter(input_string, delimiter):
    if not input_string:
        return []  # Return an empty list if the input string is empty
    elif not delimiter:
        return input_string
    split_array = input_string.split(delimiter)  # Split the input string using the delimiter
    split_array = [item.strip() for item in split_array]  # Remove leading and trailing whitespaces from each item
    return split_array


def generate_qrcode(string, booking_string):
    # Create a QR code instance
    qr = pyqrcode.create(string)
    # Get the absolute path of the project directory
    project_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), ".."))
    # Join the project directory with the subdirectories to save the qr-code files at
    folder_path = os.path.join(project_dir, 'media', 'qr-codes')
    # make directory if it does not exist yet
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # name the qr-code file with unique name booking_string.png
    qr_filename = f"{booking_string}.png"
    qr_path = os.path.join(folder_path, qr_filename)
    # create qr-code
    qr.png(qr_path, scale=10)
    # return path to qr-code file
    return qr_path


def fill_booking_attachment_template(booking_string, bike_name, store_name, start_date, end_date, username):
    # Define the path to the template for the attachment content
    template_path = 'email_templates/BookingresponseQR.html'
    # Prepare the context with data to be filled into the template
    context = {
        'header_image': lastenkarle_logo_url,
        'bike_name': bike_name,
        'store_name': store_name,
        'start_date': start_date,
        'end_date': end_date,
        'username': username,
        'booking_string': booking_string,
        'qr_path': os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "media", "qr-codes", "%s.png" % booking_string))
    }
    # Render the HTML content by filling the template with context data
    html_content = render_to_string(template_path, context)
    # return the filled HTML content
    return html_content


def create_and_save_booking_pdf_from_html(html_content, booking_string):
    # Get the directory path of the current file
    project_dir = os.path.abspath(
        os.path.dirname(__file__))
    # Construct the output PDF path
    output_pdf_path = os.path.join(project_dir, 'pdf', f'{booking_string}.pdf')
    # Open the PDF file for writing
    pdf_file = open(output_pdf_path, "wb")
    # Generate the PDF using xhtml2pdf library
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
    # Close the PDF file
    pdf_file.close()
    # Error Handling
    if pisa_status.err:
        return HttpResponse("Fehler beim Erstellen des PDFs")
    return output_pdf_path


def format_equipment(equipment_queryset):
    # convert equipment queryset into a list
    equipment_list = list(equipment_queryset)
    # convert to string and join them
    equipment_strings = [str(equipment) for equipment in equipment_list]
    return ', '.join(equipment_strings)


def list_admin_emails():
    # get the User_Status object for "Administrator"
    admin_status = User_Status.objects.get(user_status="Administrator")
    # Query the User model to get users with the "Administrator" status
    users_with_admin_status = User.objects.filter(user_status=admin_status)
    # Extract email addresses from the list of administrators
    email_list = [user.contact_data for user in list(users_with_admin_status)]
    return email_list
