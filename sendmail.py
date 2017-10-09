#!/usr/bin/env python
# -*- coding:utf-8 -*-


# script envoi de mail

import smtplib
import RPi.GPIO as GPIO
import time
import logging

GSM_WAIT_SECONDS = 10
GSM_WAIT_INTERVAL = 1

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'expediteur@gmail.com'
SMTP_PWD = 'mdpexpediteur'

MAIL_FROM = SMTP_USER
MAIL_TO = 'destinataire@gmail.com'

GPIO_PIN_SWITCH_DOWN = 23
GPIO_PIN_SWITCH_UP = 24

GPIO_EVENT_BOUNCETIME = 3000

__logger__ = logging.getLogger(__name__)


def send_email(content):
    """
    Envoi un email avec un contenu spécifique
    :param content: Contenu du mail
    :type content: str
    :return: None
    """
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
        if GPIO.input(GPIO_PIN_SWITCH_UP):  # le capteur haut aussi
            __logger__.error('Tous capteurs fermés, situation anormale')
        else:  # le capteur haut est ouvert
            __logger__.info('Réservoir vide')
            send_email('Reservoir vide')
    elif channel == GPIO_PIN_SWITCH_UP:  # Le capteur haut est fermé
        if GPIO.input(GPIO_PIN_SWITCH_DOWN):  # le capteur bas aussi
            __logger__.error('Tous capteurs fermés, situation anormale')
        else:  # le capteur bas est ouvert
            __logger__.info('Réservoir plein')
            send_email('Reservoir plein')



if __name__ == '__main__':

    # Configuration du niveau de log par défaut
    logging.basicConfig(level=logging.INFO)

    # Boucle pour attendre la connectivité internet (GSM)
    __logger__.info('Attente connectivité internet')
    for i in range(GSM_WAIT_INTERVAL, GSM_WAIT_SECONDS, GSM_WAIT_INTERVAL):
        time.sleep(GSM_WAIT_INTERVAL)
        __logger__.info('%i sec. écoulés' % i)

    send_email('additiveur societe X redemarre')

    # Configuration des ports GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN_SWITCH_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_PIN_SWITCH_UP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Ajout de la callback en cas d'activation du capteur bas
    GPIO.add_event_detect(GPIO_PIN_SWITCH_DOWN, GPIO.RISING, callback=tank_filling_callback, bouncetime=GPIO_EVENT_BOUNCETIME)
    # idem pour le capteur haut
    GPIO.add_event_detect(GPIO_PIN_SWITCH_UP, GPIO.RISING, callback=tank_filling_callback, bouncetime=GPIO_EVENT_BOUNCETIME)

    # Boucle infinie pour laisser le programme en fonction
    # Interception de l'arrêt volontaire (interruption) du programme (CTRL+C) pour un arrêt propre
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()

    send_email('Arret de l\'additiveur')