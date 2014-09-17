
#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""

Diverse Funktionen und Keyboard-Klasse für die Überprüfung von einem Korpus
Wörtern

konvertiert in misshandeltes IPA und überprüft Kompatibilität mit Keyboard

"""
import copy
import re

# Reg-Ex-Dictionary für IPA-Aufbereitung noch vor Umwandlung in Keyboard-Zeichen
additional_substitutions={\
    "ʒ":"ʃ", \
    "x":"ç", \
    "ʀ":"r", \
    "ʁ":"r", \
    "ə":"ɛ", \
    "z":"s"  \
    }

# Dictionary um Diphthongs von IPA in Keyboard-Zeichen umzuwandeln
# Wichtig und muss vor normalen Vokalen gemacht werden
# Für Rückumwandlung nicht nötig, da da die Zeichen eindeutig sind
ipa_to_keyboard_diph = {\
    "aʊ":"Ä", \
    "aɪ":"Ü", \
    "ɔʏ":"Ö"\
    }

# Dictionary um 2-stellige Vokale von IPA in Keyboard-Zeichen umzuwandeln ohne Diphthongs!
ipa_to_keyboard_v2 = {\
    "aː":"A", \
    "eː":"E", \
    "iː":"I", \
    "oː":"O", \
    "uː":"U", \
    "ɛː":"ä", \
    "øː":"ø", \
    "yː":"Y" \
    }
# Dictionary um 1-stellige Vokale von IPA in Keyboard-Zeichen umzuwandeln ohne Diphthongs!
ipa_to_keyboard_v1 = {\
    "a":"a", \
    "ɛ":"ɛ", \
    "ɪ":"ɪ", \
    "ɔ":"ɔ", \
    "ʊ":"ʊ", \
    "œ":"œ", \
    "ʏ":"ʏ", \
    }

# Dictionary um 1-stellige Konsonanten von IPA in Keyboard-Zeichen umzuwandeln -nur die die abweichen
ipa_to_keyboard_k = {\
    "z":"s", \
    "ɛ":"ɛ", \
    "ɪ":"ɪ", \
    "ɔ":"ɔ", \
    "ʊ":"ʊ", \
    "œ":"œ", \
    "ʏ":"ʏ", \
    }


# Dictionary um Vokale von Keyboard-Zeichen in IPA umzuwandeln
keyboard_to_ipa_v = {
    "a":"a", \
    "A":"aː", \
    "ɛ":"ɛ", \
    "E":"eː", \
    "ɪ":"ɪ", \
    "I":"iː", \
    "ɔ":"ɔ", \
    "O":"oː", \
    "ʊ":"ʊ", \
    "U":"uː", \
    "ä":"ɛː", \
    "œ":"œ", \
    "ø":"øː", \
    "ʏ":"ʏ", \
    "Y":"yː", \
    "Ä":"aʊ", \
    "Ü":"aɪ", \
    "Ö":"ɔʏ" \
    }
    
# Dictionary für welche Wertigkeit zu welchem Vokal-Key gehört
value_v = {\
    0:"a", \
    1:"A", \
    2:"ɛ", \
    3:"E", \
    4:"ɪ", \
    5:"I", \
    6:"ɔ", \
    7:"O", \
    8:"ʊ", \
    9:"U", \
    10:"ä", \
    11:"œ", \
    12:"ø", \
    13:"ʏ", \
    14:"Y", \
    15:"Ä", \
    16:"Ü", \
    17:"Ö" \
    }

# Dictionary für welche Wertigkeit zu welchem Konsonant-Key gehört
value_k = {\
    0:"b", \
    1:"ç", \
    2:"d", \
    3:"ʃ", \
    4:"f", \
    5:"g", \
    6:"h", \
    7:"j", \
    8:"k", \
    9:"l", \
    10:"m", \
    11:"n", \
    12:"ŋ", \
    13:"p", \
    14:"r", \
    15:"ɐ", \
    16:"s", \
    17:"t", \
    18:"v" \
    }
    
# Dictionary für welche Wertigkeit zu welchem Vokal-Key gehört
v_value = {\
    "a":0, \
    "A":1, \
    "ɛ":2, \
    "E":3, \
    "ɪ":4, \
    "I":5, \
    "ɔ":6, \
    "O":7, \
    "ʊ":8, \
    "U":9, \
    "ä":10, \
    "œ":11, \
    "ø":12, \
    "ʏ":13, \
    "Y":14, \
    "Ä":15, \
    "Ü":16, \
    "Ö":17 \
    }

# Dictionary für welche Wertigkeit zu welchem Konsonant-Key gehört
k_value = {\
    "b":0, \
    "ç":1, \
    "d":2, \
    "ʃ":3, \
    "f":4, \
    "g":5, \
    "h":6, \
    "j":7, \
    "k":8, \
    "l":9, \
    "m":10, \
    "n":11, \
    "ŋ":12, \
    "p":13, \
    "r":14, \
    "ɐ":15, \
    "s":16, \
    "t":17, \
    "v":18 \
    }

# Funktion um zu überprüfen ob in einer Liste ein Element doppelt vorkommt
def valid(input):
    val = True
    counter1 = 0
    max_length_counter2 = len(input)
    max_length_counter1 = max_length_counter2 - 1
    
    while counter1 < max_length_counter1 :
        counter2 = counter1 + 1
        while counter2 < max_length_counter2:
            if input[counter1] == input[counter2]:
                val = False
                break
            counter2 += 1
        if val == False:
            break
        counter1 += 1
    return val
        
# Tastatur um ein element inkrementieren
def increment(input,  modulo):
    for i in input:
        i = int(i)
    # Zähler durch alle Teile vom rechten/mittleren/linken Tastaturteil
    counter = len(input)-1
    # Zähler für maximale Größe für Vokale und Konsonanten für Modulo-Rechnung
    # siehe Input-Variable Modulo
    
    # Übertrag ist zu Beginn eins, da Increment
    uebertrag = 1
        
    while counter >= 0:
        if uebertrag == 1:
            input[counter] = int(input[counter])+1
        if input[counter] >= modulo:
            uebertrag = 1
            input[counter] = int(input[counter]) - modulo
        else:
            uebertrag = 0
            break            
        counter -= 1
    
    # Falls immer noch ein Übertrag vorhanden ist (also Zahlenüberlauf) dann nochmal die Funktion aufrufen
    if uebertrag == 1:
        for i in input:
            i = 0
        #input = increment(input, modulo).copy()
    return copy.deepcopy(input)
    
# Funktion gibt Liste zurück die alle gültigen Tastatur Layouts enthält mit den Werten
# start_val: Startliste, break_val: Stop-Liste, max: "Zahlensystem" des Layout = 
# Anzahl verschiedener Werte die pro Stelle im Layout möglich sind.
def partial_layouts_partial_cycle(start_val, break_val, max):
    debug = False
    back = []
    valide = False
    if debug: print("Start_val: ", start_val)
    if debug: print("End_val: ", break_val)
    while True:
        # Erst nachsehen ob schon der Endwert erreicht ist, denn der ist nicht eingeschlossen
        # Wenn ja dann hier aufhören
        print (start_val)
        if start_val == break_val:
            break
        # Wert inkrementieren
        start_val = increment(start_val, max)
        # Überprüfen ob die Ausgabe gültig ist als Tastatur-Layout
        valide = valid(start_val)
        # Falls das Layout gültig ist, raus speichern
        print (valid, )
        if valide == True:
            back.append(start_val[:])            
    return copy.deepcopy(back)
    
# Funktion gibt Liste zurück die alle gültigen Tastatur Layouts enthält mit den Werten
# start_val: Startliste, break_val: Stop-Liste, max: "Zahlensystem" des Layout = 
# Anzahl verschiedener Werte die pro Stelle im Layout möglich sind.
def partial_layouts_complete_cycle(start_val, max):
    debug = False
    back = []
    counter = 0
    max_counter = max**(len(start_val))
    if debug: print ("Max-Counter: ", max_counter)
    while counter < max_counter:
        if debug: print("Anfang while: ", start_val)
        # Überprüfen ob die Ausgabe gültig ist als Tastatur-Layout
        valide = valid(start_val)
        if debug: print("Start_Val nach valid testen: ", start_val)
        # Falls das Layout gültig ist, raus speichern
        if valide:
            if debug: print("Vor anhängen: ", start_val)
            back.append(start_val[:])
            if debug: print("back: ", back[len(back)-1])
            if debug: print("Das angehängt: ", start_val)
        if debug: print(counter, valide, start_val)
        # Wert inkrementieren
        if debug: print("Vor inkrement: ", start_val)
        start_val = increment(start_val, max)
        if debug: print("Vor nach inkrement: ", start_val)
        if debug: print("Vor counter: ", start_val, "\n")
        print(counter)
        counter += 1
    return copy.deepcopy(back)

# Funktion wandelt IPA String (nach Leipziger Variante) in Keyboard-Layout um:
def ipa_to_keyb(ipa_string):
    keyb  = copy.deepcopy(ipa_string)
    # zuerst doppelte Zeichen ersetzen, Beginn mit Diphthongs
    for key in ipa_to_keyboard_diph.keys():
        keyb = keyb.replace(key, ipa_to_keyboard_diph[key])
    # dann doppelte Zeichen die kein Diphthongs sind
    for key in ipa_to_keyboard_v2.keys():
        keyb = keyb.replace(key, ipa_to_keyboard_v2[key])
    # einzelne Zeichen wie Anfang von "Dschungel"
    for key in additional_substitutions.keys():
        keyb = keyb.replace(key, additional_substitutions[key])
    return keyb    
    
"""
================================================================================
Klasse um die Wörter wiederzugeben
================================================================================
"""
class word:
# Initialisierungsfunktion    
    def __init__(self, word = "", ipa_perl = "",  ipa_leipzig = "",\
        frequency = "", frequency_class = "", keyb_code = "",\
        regex ="", values = 0):
        self.word = word
        self.ipa_perl = ipa_perl
        self.ipa_leipzig = ipa_leipzig
        self.frequency = frequency
        self.frequency_class = frequency_class
        self.keyb = keyb_code
        self.regex = regex
        self.values = values
    
    # Funktion um aus ipa_leipzig keyb_code zu machen
    def ipa_to_keyb(self):
        keyb = copy.deepcopy(self.ipa_leipzig)
        return ipa_to_keyb(keyb)            
        
    # Funktion um aus keyboard_code regex zu machen
    def keyb_to_regex(self):
        if self.keyb == "":
            self.ipa_to_keyb()
        regex = ".*"
        for zeichen in self.keyb:
            regex = regex + zeichen + ".*"
        self.regex = regex
        return self.regex

"""
================================================================================
Weitere Funktionen z.B. um Wörter aus Files einzulesen
================================================================================
"""
def read_words_from_file(file_name, word_de = True, ipa_perl = True,\
    ipa_leipzig = True, frequency = True,  frequency_class = True, \
    keyb_code = True, regex = True):
    
    
    
    
    pass
    
    
def write_words_to_file(file_name, words):    
    
    pass
    
    
