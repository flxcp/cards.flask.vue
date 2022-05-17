from .workers import celery
from app.message import dailyRemainderChat, dailyRemainderEmail, mail, ImportNotificationChat, ImportNotificationMail, ExportNotificationChat, ExportNotificationMail
from app.access import acs_user_all, acs_userprofile_userid, acs_loginledger_id, acs_user_id, acs_deck_id, acs_user_all
from app.db import Deck, Cards, User, CardResponse
from flask import current_app as app, url_for
from jinja2 import Template
from app.db import db
from celery.schedules import crontab
from app.cache import cache
from weasyprint import HTML
import datetime
import csv


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(day_of_month=1, month_of_year='*'),
        monthlyMail.s(),
    )
    sender.add_periodic_task(
        crontab(minute=0, hour=18, day_of_month='*'),
        dailyRemainder.s(),
    )


@celery.task()
def sendRemainder(id):
    userprof = acs_userprofile_userid(id)
    user = acs_user_id(id)
    name = user.email.split('@')[0].capitalize()
    if userprof.communication_preference == 'chat':
        dailyRemainderChat(name, userprof.webhook_url)
    else:
        dailyRemainderEmail(name, user.email)

    return 'Remainder sent'


@celery.task()
def sendMonthlyMail(id, email):
    name = email.split('@')[0].capitalize()
    no_of_decks = db.session.query(
        Deck).filter_by(user_id=id).count()
    completed_deck = db.session.query(
        Deck).filter_by(user_id=id, status=1).count()
    no_of_cards = db.session.query(
        Cards).filter_by(user_id=id).count()
    respose_with_one = db.session.query(CardResponse).filter_by(
        user_id=id, response=1).count()
    respose_with_two = db.session.query(CardResponse).filter_by(
        user_id=id, response=2).count()
    respose_with_three = db.session.query(CardResponse).filter_by(
        user_id=id, response=3).count()

    userprof = acs_userprofile_userid(id)
    if userprof.email_format == 'email':
        with open(f'{app.config["EMAIL_TEMPLATE"]}report.mail.html') as file:
            template = Template(file.read())
            message = template.render(name=name, no_decks=no_of_decks, no_completed_deck=completed_deck, no_incomplete_deck=(no_of_decks - completed_deck), no_cards=no_of_cards,
                                      cards_hard=respose_with_one, cards_med=respose_with_two, cards_easy=respose_with_three, cards_total=(respose_with_one + respose_with_two + respose_with_three))

        mail(email, 'Monthly Review Report', message)
    else:
        with open(f'{app.config["EMAIL_TEMPLATE"]}report.mail.pdf.html') as file:
            pdf_template = Template(file.read())
            pdf_message = pdf_template.render(name=name, no_decks=no_of_decks, no_completed_deck=completed_deck, no_incomplete_deck=(no_of_decks - completed_deck), no_cards=no_of_cards,
                                              cards_hard=respose_with_one, cards_med=respose_with_two, cards_easy=respose_with_three, cards_total=(respose_with_one + respose_with_two + respose_with_three))
            html = HTML(string=pdf_message)
            html.write_pdf(
                target=f'{app.config["PDF_FOLDER"]}user.{id}.report.pdf')

        with open(f'{app.config["EMAIL_TEMPLATE"]}monthly.report.html') as file:
            template = Template(file.read())
            message = template.render(name=name)

        mail(email, 'Monthly Review Report', message, f'user.{id}.report.pdf')

    return 'Sent Mail'


@celery.task()
def monthlyMail():
    users = acs_user_all()

    for user in users:
        sendMonthlyMail.delay(user.id, user.email)

    return 'Monthly Mail Sent'


@celery.task()
def dailyRemainder():
    for user in acs_user_all():
        loginledger = acs_loginledger_id(user.id)

        if loginledger:
            diff = datetime.datetime.now() - loginledger.last_active_time
            if diff.total_seconds() < 86400:
                sendRemainder.delay(user.id)
        else:
            sendRemainder.delay(user.id)

    return 'Daily Remainder sent'


@celery.task()
def importDeck(deck_id, id, email):
    deck = acs_deck_id(deck_id, id)
    existing_cards = [card.question for card in deck.deckcards]

    cards = csv.reader(
        open(f'{app.config["UPLOAD_FOLDER"]}file.csv', 'r'))
    for card in cards:
        if card[0] not in existing_cards:
            existing_cards.append(card[0])
            db.session.add(Cards(user_id=user.id,
                                 deck_id=deck_id, question=card[0], answer=card[1]))

    cache.delete_memoized(acs_deck_id, deck_id, id)
    cache.delete_memoized(acs_user_id, id)

    db.session.commit()

    userprof = acs_userprofile_userid(id)
    if userprof.communication_preference == 'chat':
        ImportNotificationChat(email.split(
            '@')[0].capitalize(), deck.name, userprof.webhook_url)
    else:
        ImportNotificationMail(deck.name, email)

    return 'Deck imported'


@celery.task()
def exportDeck(file_name, deck_id, id, email, url):
    deck = acs_deck_id(deck_id, id)

    export_file = open(f'{app.config["UPLOAD_FOLDER"]}{file_name}', 'w')
    writer = csv.writer(export_file)

    for card in deck.deckcards:
        writer.writerow([card.question, card.answer])

    export_file.close()

    userprof = acs_userprofile_userid(id)
    if userprof.communication_preference == 'chat':
        ExportNotificationChat(email.split(
            '@')[0].capitalize(), deck.name, url, userprof.webhook_url)
    else:
        ExportNotificationMail(deck.name, url, email)

    return 'Deck exported'
