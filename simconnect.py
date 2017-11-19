#!/usr/bin/env python
# -*- coding:Utf-8 -*-


import RPi.GPIO as GPIO
import time
import socket

GPIO.setmode(GPIO.BCM)

###########################
#Démarrage carte SIM800 pour connexion internet
###########################


GPIO.setup(17, GPIO.IN) 
state = GPIO.input(17)


if (state is True):
    print ("Carte SIM800 déjà démarrée")

else:
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, True)
    time.sleep(1)
    print ("Carte SIM800 démarrée")

GPIO.cleanup()
