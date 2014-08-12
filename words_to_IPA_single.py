#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Skript holt für Liste an Wörtern alle vermfügbaren Infos ein, aber einzeln pro Wort
"""
import sys
import os
import IPA_Methods
#reload(sys)
#sys.setdefaultencoding('utf-8')
#import locale
#import unicodedata
debug = True

print ("\nDieses Skript holt die absolute Häufigkeit und die Häufigkeitsklasse eines Wortes vom Server der Uni Leipzig aus deren Datenbank.\n")

#print "Menge der Argumente: " + str(len(sys.argv)) + "\n"

# Fehlende Argumente abfangen
if len(sys.argv)<=1:
    print ("FEHLER zu wenig Parameter!\n")
    print ("Programm muss mit Ein- und Ausgabedatei aufgerufen werden z.B.:")
    print ("python " + str(sys.argv[0]) + " Eingabedatei Ausgabedatei")
    print ("Keine Ein- und Ausgabedatei angegeben.\n\nProgramm wird abgebrochen")
    sys.exit(0)

if debug: print ("Eingabedatei" + sys.argv[1])
if debug: print ("Ausgabedatei" + sys.argv[2])

# Nicht vorhandene Dateien abfangen
if not os.path.exists(sys.argv[1]):
    print ("Eingabedatei nicht vorhanden, breche ab!")
    sys.exit(0)
else :
    print ("Alles okay, Eingabedatei vorhanden")

# Lib die sich mit dem Server verbindet erst öffnen wenn wirklich gebraucht    
#from libleipzig import *

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

# Ergebnis Array anlegen
woerter_haeufigkeiten_und_klassen=[]

# Zeilenendezeichen enfernen:
#for wort in woerter:
#    wort = wort[0:len(wort)-1]

# Perl Skript nur einmal aufrufen
#ipa_perl = IPA_Methods.Get_IPA_from_Perl_script(woerter)

counter = 0
while counter < len(woerter):
    #Rückgabe Liste eine Unter-Liste anhängen
    woerter_haeufigkeiten_und_klassen.append([])
    
    #Zeilenendezeichen aus Datei abschneiden:
    woerter[counter] = woerter[counter][0:len(woerter[counter])-1]
    
    # Rückgabe aus sämtlichen anderen Skripten:
    ipa_perl = IPA_Methods.Get_IPA_from_Perl_script(woerter[counter])
    ipa_online = IPA_Methods.Get_IPA_from_online(woerter[counter])
    freq_class = IPA_Methods.Get_Frequencies_and_class(woerter[counter])

    # Aus jedem Einzelergebnis Array bauen
    woerter_haeufigkeiten_und_klassen[counter].append(woerter[counter])
    woerter_haeufigkeiten_und_klassen[counter].append(ipa_perl[0])
    woerter_haeufigkeiten_und_klassen[counter].append(ipa_online[0])
    woerter_haeufigkeiten_und_klassen[counter].append(freq_class[0][0])
    woerter_haeufigkeiten_und_klassen[counter].append(freq_class[0][1])    
    
    # Debug Ausgabe für jede Zeile
    if debug: print(counter,": ",woerter_haeufigkeiten_und_klassen[counter][0]," ",\
        woerter_haeufigkeiten_und_klassen[counter][1]," ",\
        woerter_haeufigkeiten_und_klassen[counter][2]," ",\
        woerter_haeufigkeiten_und_klassen[counter][3]," ",\
        woerter_haeufigkeiten_und_klassen[counter][4],end="")
    # Alles in Ausgabedatei schreiben
    ausgabedateihandle.write(woerter_haeufigkeiten_und_klassen[counter][0]+";"+\
        woerter_haeufigkeiten_und_klassen[counter][1]+";"+\
        woerter_haeufigkeiten_und_klassen[counter][2]+";"+\
        woerter_haeufigkeiten_und_klassen[counter][3]+";"+\
        woerter_haeufigkeiten_und_klassen[counter][4]+"\n")
    
    # Debug Ausgabe für raus geschrieben in Dateihandle
    if debug: print(" S ",end="" )
    # Ausgabedatei geflusht
    ausgabedateihandle.flush()
    if counter % 10 == 0:
        #os.fsync(ausgabedateihandle.fileno())
        if debug: print("F")
    else:
        if debug: print("")
    counter +=1 

ausgabedateihandle.close()
print ("\nEnde")
