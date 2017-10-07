#!/usr/bin/env python
# -*- coding:Utf-8 -*-


#script envoie de mail

import smtplib
import RPi.GPIO as GPIO
import time
import socket
import subprocess


GPIO.setmode(GPIO.BCM)

###########################
#Attente d'1min pour lancement connexion internet
###########################
print ("Attente connexion internet 60 secondes")
#time.sleep(10)
#print ("10 sec écoulées")
#time.sleep(10)
#print ("20 sec écoulées")
#time.sleep(10)
#print ("30 sec écoulées")
#time.sleep(10)
#print ("40 sec écoulées")
#time.sleep(10)
#print ("50 sec écoulées")

#time.sleep(10)
#print ("60 sec écoulées")



###########################
#config des ports GPIO
###########################
pin_fin_res = 23
pin_res_full = 24

###########################
#Démarrage de l'additiveur et envoie d'un mail
###########################
    
content =  'additiveur societe X redemarre'
mail = smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
mail.login('expediteur@gmail.com',"mdpexpediteur")
mail.sendmail('expediteur@gmail.com','destinataire@gmail.com',content)
mail.close()
print ("Additiveur redémarré mail envoyé")

time.sleep(5)         # wait 5 seconds  


while True:

    GPIO.setmode(GPIO.BCM)
    
    # Define a threaded callback function to run in another thread when events are detected  
    def my_callback(channel):
        GPIO.input(pin_fin_res)
        
        if GPIO.input(pin_fin_res):
            print ("Contact haut détecté on {0}".format(pin_fin_res))

        else:              
            print ("Contact bas détécté {0}".format(pin_fin_res))

            content =  'Reservoir vide'
            mail = smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.starttls()
            mail.login('expediteur@gmail.com',"mdpexpediteur")
            mail.sendmail('expediteur@gmail.com','destinataire@gmail.com',content)
            mail.close()
            print ("Réservoir vide mail envoyé à expediteur@gmail.com")
            time.sleep(5)
          

    GPIO.setup(pin_fin_res, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin_fin_res,GPIO.BOTH,callback=my_callback,bouncetime=3000)
    try:
        print ("Attente fin de réservoir")
        time.sleep(1)

    finally:
        GPIO.cleanup()
