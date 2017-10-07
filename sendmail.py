#!/usr/bin/env python
# -*- coding:Utf-8 -*-


#script envoie de mail

import smtplib
#import RPi.GPIO as GPIO
import time
import logging


GSM_WAIT_SECONDS = 60
GSM_WAIT_INTERVAL = 10

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'expediteur@gmail.com'
SMTP_PWD = 'mdpexpediteur'

MAIL_FROM = SMTP_USER
MAIL_TO = 'destinataire@gmail.com'

GPIO_PIN_FIN_RES = 23
GPIO_PIN_RES_FULL = 24

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


def my_callback(channel):
    """
    Callback appelée pour détecter la fin de réservoir
    :param channel:
    :return:
    """
    GPIO.input(GPIO_PIN_FIN_RES)

    if GPIO.input(GPIO_PIN_FIN_RES):
        __logger__.info("Contact haut détecté on %s" % GPIO_PIN_FIN_RES)
    else:
        __logger__.info("Contact bas détécté %s" % GPIO_PIN_FIN_RES)
        send_email('Reservoir vide')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)


    __logger__.info('Attente connectivité internet')
    for i in range(GSM_WAIT_INTERVAL, GSM_WAIT_SECONDS, GSM_WAIT_INTERVAL):
        time.sleep(GSM_WAIT_INTERVAL)
        __logger__.info('%i sec. écoulés' % i)

    send_email('additiveur societe X redemarre')

    time.sleep(5)  # Encore utile ?

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(GPIO_PIN_FIN_RES, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(GPIO_PIN_FIN_RES, GPIO.BOTH, callback=my_callback, bouncetime=3000)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()