import smtplib
from json import dumps
from httplib2 import Http
from jinja2 import Template
from flask import render_template
from email.mime.text import MIMEText
from flask import current_app as app
from email.mime.multipart import MIMEMultipart, MIMEBase
from email import encoders

# SMPTP_SERVER_HOST = 'localhost'
SMPTP_SERVER_HOST = '127.0.0.1'
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "mail@cards.com"
SENDER_PASSWORD = ''


def webhook(hook, message):
    message = {'text': message}
    headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()
    response = http_obj.request(
        uri=hook, method='POST', headers=headers, body=dumps(message))

    return response


def dailyRemainderEmail(name, email):
    with open(f'{app.config["EMAIL_TEMPLATE"]}daily.rem.html') as file:
        template = Template(file.read())
        message = template.render(name=name)

    mail(email, 'Daily Reminder', message)


def dailyRemainderChat(name, hook):
    message = '*Hi {}*,\n\nYou haven\'t revised today. Learning every day helps keep your concepts clear.\nSo login now to continue learning. '.format(
        name)
    webhook(hook, message)


def ExportNotificationMail(deck, url, email):
    with open(f'{app.config["EMAIL_TEMPLATE"]}export.not.html') as file:
        template = Template(file.read())
        message = template.render(name=email.split(
            '@')[0].capitalize(), deck=deck, url=url)

    mail(email, 'Export Complete', message)


def ExportNotificationChat(name, deck, url, hook):
    message = '*Hi {}*,\n\nExport for Deck *{}* is complete. You can download CSV File.\n{} '.format(
        name, deck, url)
    webhook(hook, message)


def ImportNotificationMail(deck, email):
    with open(f'{app.config["EMAIL_TEMPLATE"]}import.not.html') as file:
        template = Template(file.read())
        message = template.render(name=email.split(
            '@')[0].capitalize(), deck=deck)

    mail(email, 'Import Complete', message)


def ImportNotificationChat(name, deck, hook):
    message = '*Hi {}*,\n\nYou Deck *{}* is Imported. '.format(name, deck)
    webhook(hook, message)


def mail(user_mail, subject, message, file_name=None):

    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = user_mail
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    if file_name:
        pdf_report = f'{app.config["PDF_FOLDER"]}{file_name}'

        with open(pdf_report, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(file_name))
            encoders.encode_base64(part)
            msg.attach(part)

    server = smtplib.SMTP(SMPTP_SERVER_HOST, SMPTP_SERVER_PORT)
    server.login(SENDER_ADDRESS, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()

    return 'Mail Sent'
