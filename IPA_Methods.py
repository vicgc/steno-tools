#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Diverse Funktionen für die Umwandlung von Wörtern in IPA

"""

import urllib.request, urllib.parse,  os,  sys,  libleipzig,  time

modulo = 1
time_modulo = 50
"""
Funktion um mit der Hilfe von der Seite http://tools.webmasterei.com/mbrolatester/
IPA für einzelnes Wort zu erhalten
Aus der Rückgabe werden alle Leerzeichen entfernt, auch wenn es mehrere Wörter waren
Rückgabe ist ein String
"""
def Get_IPA_for_word_online(word):
    input = {b"foo":word}
    data = bytes(urllib.parse.urlencode(input), "UTF-8")
    u = urllib.request.urlopen("http://tools.webmasterei.com/mbrolatester/text2pho.php", data)
    bytes_output = u.readlines()
    u.close()
    string_output = bytes_output[0].decode("UTF-8")
    wort_ipa = string_output[string_output.rfind(".innerHTML=\'")+12:string_output.rfind("\';</script>")-1]
    wort_ipa = wort_ipa.replace(" ","")
    return wort_ipa

"""
Funktion um mit der Hilfe von der Seite http://tools.webmasterei.com/mbrolatester/
IPA für einzelne Wörter oder Listen zu holen
Aus der Rückgabe werden alle Leerzeichen entfernt, auch wenn es mehrere Wörter waren
Rückgabe ist immer eine Liste
"""
def Get_IPA_from_online(word):
    rueck_liste = []
    #Für einzelnen String
    if type(word)==type("Wort"):
        rueck_liste.append(Get_IPA_for_word_online(word))
    if type(word)==type([]):
        i = 0
        for w in word:
            rueck_liste.append(Get_IPA_for_word_online(w))
            i+=1
            #if i % modulo == 0: print ("IPA Online Durchgang: "+str(i))
            #if i % time_modulo ==0: time.sleep(2)
    return rueck_liste
    
"""
Funktion die IPA aus dem Perl Skript holt mit dem Umweg über eine temporäre Eingabe-Datei
Rückgabe ist immer eine Liste
"""    
def Get_IPA_from_Perl_script(word):
    #Debug-Hilfe
    debug = False
    #Temporärer Input kommt in temp_input.txt
    temp_inputfile = "temp_input.txt"
    
    # Nachsehen ob die Temp-Datei nicht existiert sonst abbrechen
    if os.path.exists(temp_inputfile):
        print("Fehler: temporäres File "+temp_inputfile+" schon vorhanden, breche ab!")
        sys.exit(0)
        
    # Datei öffnen
    input = open(temp_inputfile,"w")
    if (debug):
        print ("Typ Eingabe: "+str(type(word)))
    #Je nachdem ob Eingabe ein String oder Liste ist, das in die Datei schreiben
    if type(word)==type("String"):
        input.write(word+"\n")
        if debug: print ("Erstes if")
    elif type(word)==type([]):
        for j in word:
            input.write(j+"\n")
        #input.writelines(word)
        if debug: print ("Zweites IF")

    #Input-Datei schließen damit die Datei in das Perl Skript gegeben werden kann
    input.close()

    #Perl Skript ausgeben und was auf Kommandozeile raus kommt wieder einsammeln
    output = os.popen("perl Text2IPA_German.pl "+temp_inputfile).readlines()
    #Leere Liste für Perl Ausgabe anlegen
    format_output = []
    #Liste mit zeilenweise Ausgabe von Perl Skript füllen ohne Zeilenende Zeichen
    for j in output:
        format_output.append(j[0:-1]) 
    
    if debug: 
        for xy in format_output:
            print (xy)
            
    #Temporäres Eingabefile wieder löschen        
    os.remove(temp_inputfile)
    return format_output
"""
Skript holt für eine Liste an Wörtern (oder auch nur einzelne Wörter) die IPA Schreibweise nach beiden Varianten zurück
Rückgabe ist eine Liste mit Zeilen aus:
"Wort" "IPA nach Perl-Skript" "IPA nach Online"
"""
    
def Get_IPA_Perl_and_online(word):
    rueck = []
    debug = False
    if debug: print ("Typ Eingabe: ", type(word))
    if type(word) == type("String"):
        rueck.append([word, Get_IPA_from_Perl_script(word)[0],Get_IPA_from_online(word)[0]])
    elif type(word) == type([]):
        perl_output = Get_IPA_from_Perl_script(word)
        online_output = Get_IPA_from_online(word)
        counter = 0
        while counter < len(word):
            rueck.append([word[counter], perl_output[counter], online_output[counter]])
            counter +=1
#        for i in word:
#            rueck.append([i, Get_IPA_from_Perl_script(i)[0],Get_IPA_from_online(i)[0]])    
    return rueck
"""
Funktion gibt für eine Liste an Wörtern einen Zeilenweisen Array zurück:
Wort, IPA aus Perl-Skript, IPA von Online,Häufigkeit, Häufigkeitsklasse
"""    
def Get_IPA_and_Frequencies(word):
    debug = True
    if type(word)==type("String"):
        word = [word]
    if debug: print("Starte Perl-Skript")
    perl_output = Get_IPA_from_Perl_script(word)
    if debug: print("Starte IPA-Online")
    online_output = Get_IPA_from_online(word)
    rueck = []
    counter = 0
    if debug: print("Starte Rückgabearray bauen mit Häufigkeiten:")
    # Für alle Wörter noch die Häufigkeite einholen und in Rückgabe Liste schreiben
    while counter < len(word):
        # Ergibt leere Liste falls das Wort nicht in der DB enthalten ist
        r = libleipzig.Frequencies(word[counter])
        # Falls Häufigkeit und Klasse verfügbar ist
        if r!=[]:
            rueck.append([word[counter], \
            perl_output[counter],\
            online_output[counter],r[0][0],r[0][1]])
        # Falls keine Häufigkeit und Klasse zu dem Wort verfügbar ist
        elif r==[]:
            rueck.append([word[counter], \
            perl_output[counter],\
            online_output[counter],"",""])
        if counter % modulo==0: print ("Speicher-Durchgang: "+str(counter))
        counter +=1
        if counter % 25: time.sleep(1)
    
    return rueck
"""
Nur Frequenz und Häufigkeitsklasse zurück geben
"""
def Get_Frequencies_and_class(word):
    if type(word)==type("String"):
        word = [word]
    rueck = []
    counter = 0
    # Für alle Wörter die Häufigkeit und Klasse einholen und in Rückgabe Liste schreiben
    while counter < len(word):
        r = libleipzig.Frequencies(word[counter])
        rueck.append([])
        # Falls Häufigkeit und Klasse verfügbar ist
        if r!=[]:
            rueck[counter].append(r[0][0])
            rueck[counter].append(r[0][1])
        # Falls keine Häufigkeit und Klasse zu dem Wort verfügbar ist
        elif r==[]:
            rueck[counter].append("")
            rueck[counter].append("")
        counter +=1
    return rueck
    
"""
print ("Erste Version mit einem Wort Nähmaschine")
print (Get_IPA_from_Perl_script("Nähmaschine"))
print ("Erste Version auch mit anderem IPA-Generator: ")
print (Get_IPA_from_online("Nähmaschine"))
print ("\n\nZweite Version mit Liste [Haus, Name]")
print (Get_IPA_from_Perl_script(["Haus", "Namen"]))
print ("Zweite Version auch mit anderem IPA-Generator: ")
print (Get_IPA_from_online(["Haus", "Namen"]))
"""
#meine_Liste = Get_IPA_Perl_and_online("Nähmaschine")
#print (Get_IPA_Perl_and_online(["Nähmaschine", "Autohaus"]))
