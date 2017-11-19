#!/usr/bin/env python
# -*- coding:utf-8 -*-


# script envoi de mail

import smtplib
import RPi.GPIO as GPIO
import time
import os
import logging

GSM_WAIT_HOST = 'google.com'
GSM_WAIT_INTERVAL = 1

SEND_EMAIL = False

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'user@gmail.com'
SMTP_PWD = 'password'

MAIL_FROM = SMTP_USER
MAIL_TO = 'recipient@gmail.com'

GPIO_PIN_SWITCH_DOWN = 23
GPIO_PIN_SWITCH_UP = 24

GPIO_EVENT_BOUNCETIME = 3000

__logger__ = logging.getLogger(__name__)


def ping(host):
    """
    Ping un domaine donné pour vérifier la connectivité
    :param str host: Domaine à tester
    :rtype: bool
    """

    return os.system('ping -c 1 %s >/dev/null 2>&1' % host) == 0


def send_email(content):
    """
    Envoi un email avec un contenu spécifique
    :param content: Contenu du mail
    :type content: str
    :return: None
    """

    if not SEND_EMAIL:
        return None

    __logger__.info('Send an email for %s' % content)
    mail = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    mail.ehlo()
    mail.starttls()
    mail.login(SMTP_USER, SMTP_PWD)
    mail.sendmail(MAIL_FROM, MAIL_TO, content)
    mail.close()
    __logger__.info('Mail sent')


def tank_filling_callback(channel):
    """
    Callback déclenchée en cas de passage d'un des capteur en état fermé
    :param channel: Canal GPIO ayant déclenché la callback
    :return:
    """

    # Conditions sur les différents états possible avec un capteur fermé
    if channel == GPIO_PIN_SWITCH_DOWN:  # Le capteur bas s'est fermé
        if GPIO.input(GPIO_PIN_SWITCH_UP):  # le capteur haut s'est ouvert
            __logger__.info('Réservoir vide')
            send_email('Reservoir vide')
        else:  # le capteur haut est fermé
            __logger__.error('Tous capteurs fermés, situation anormale')
    elif channel == GPIO_PIN_SWITCH_UP:  # Le capteur haut est fermé
        if GPIO.input(GPIO_PIN_SWITCH_DOWN):  # le capteur bas est ouvert
            __logger__.info('Réservoir plein')
            send_email('Reservoir plein')
        else:  # le capteur bas est fermé
            __logger__.error('Tous capteurs fermés, situation anormale')



if __name__ == '__main__':

    # Configuration du niveau de log par défaut
    log_format = '%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)

    # Boucle pour attendre la connectivité internet (GSM)
    __logger__.info('Attente connectivité internet')
    while not ping(GSM_WAIT_HOST):
        time.sleep(GSM_WAIT_INTERVAL)

    __logger__.info('Additiveur démarré')
    send_email('additiveur societe X redemarre')

    # Configuration des ports GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN_SWITCH_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_PIN_SWITCH_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Ajout de la callback en cas d'activation du capteur bas
    GPIO.add_event_detect(GPIO_PIN_SWITCH_DOWN, GPIO.FALLING, callback=tank_filling_callback, bouncetime=GPIO_EVENT_BOUNCETIME)
    # idem pour le capteur haut
    GPIO.add_event_detect(GPIO_PIN_SWITCH_UP, GPIO.FALLING, callback=tank_filling_callback, bouncetime=GPIO_EVENT_BOUNCETIME)

    # Boucle infinie pour laisser le programme en fonction
    # Interception de l'arrêt volontaire (interruption) du programme (CTRL+C) pour un arrêt propre
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()

    __logger__.info('Additiveur arreté')
    send_email('Arret de l\'additiveur')
