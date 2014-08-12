#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os


#import steno-keyboard-layout as skl
import IPA_Methods

if len(sys.argv)<=1:
    print ("FEHLER zu wenig Parameter!\n")
    print ("Programm muss mit Ein- und Ausgabedatei aufgerufen werden z.B.:")
    print ("python " + str(sys.argv[0]) + " Eingabedatei Ausgabedatei")
    print ("Keine Ein- und Ausgabedatei angegeben.\n\nProgramm wird abgebrochen")
    sys.exit(0)
 
# Nicht vorhandene Dateien abfangen
if not os.path.exists(sys.argv[1]):
    print ("Eingabedatei nicht vorhanden, breche ab!")
    sys.exit(0)
else :
    print ("Alles okay, Eingabedatei vorhanden!") 
    
# Checken ob Eingabedatei auch wirklich aufgeht und dann öffnen
try:
    eingabedateihandle = open(sys.argv[1],"r")
except:
    print ("Eingabedatei öffnen nicht erfolgreich")
    sys.exit(0)

# Checken ob Ausgabedatei auch wirklich aufgeht und dann öffnen
try:
    ausgabedateihandle = open(sys.argv[2],"a")
except:
    print ("Ausgabedatei öffnen nicht erfolgreich")
    sys.exit(0)
    
# Eingabedatei einlesen und wieder schließen
woerter = eingabedateihandle.readlines()
eingabedateihandle.close()

counter = 0

# Von allen eingelesenen Wörtern die Zeilenende Zeichen abschneiden
while counter < len(woerter):
    woerter[counter]=woerter[counter][0:len(woerter[counter])-1]
    #print (woerter[counter])
    counter += 1
    
#Funktion aufrufen um alle Wörter in IPA umzuwandeln und Häufigkeit und Klasse anzuhängen
ausgabe = IPA_Methods.Get_IPA_and_Frequencies(woerter)

#for i in ausgabe:
#    print (i)
for ebbes in ausgabe:
    ausgabedateihandle.write(ebbes[0]+";"+\
                             ebbes[1]+";"+\
                             ebbes[2]+";"+\
                             ebbes[3]+";"+\
                             ebbes[4]+"\n")
ausgabedateihandle.close()
print ("\nEnde")
    
 
