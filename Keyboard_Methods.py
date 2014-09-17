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
===============================================================================
Klasse um die Tastatur abzubilden mit links 7 Tasten rechts 10 und 4 Tasten für
die Vokale
===============================================================================
"""
class Steno_Keyboard:

# Initialisierungsfunktion    
    def __init__(self, left_keys = [0, 0, 0, 0, 0, 0, 0], middle_keys = [0, 0, 0, 0], right_keys=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], v1 = 0, v2 = 0, v3 = 0 , v4 = 0 ):
        self.l_keys = left_keys
        self.m_keys = middle_keys
        self.r_keys = right_keys
        self.vote1 = 0
        self.vote2 = 0
        self.vote3 = 0
        self.vote4 = 0
        
# Rückgabe als Werte    
    # Linke Tasten als Werte zurück geben
    def l_values(self):
        return self.l_keys
        
    # Mittlere Tasten als Werte zurück geben
    def m_values(self):
        return self.m_keys
    
    # Rechte Tasten als Werte zurück geben
    def r_values(self):
        return self.r_keys

# Rückgabe als Keyb-Codes
    # Linke Tasten als Keyb-Codes zurück geben
    def l_keyb(self):
        back = []
        for i in self.l_keys:
            back.append(value_k[i])
        return back        
    
    # Mittlere Tasten als Keyb-Codes zurück geben    
    def m_keyb(self):
        back = []
        for i in self.m_keys:
            back.append(value_v[i])
        return back        
    
    # Rechte Tasten als Keyb-Codes zurück geben
    def r_keyb(self):
        back = []
        for i in self.r_keys:
            back.append(value_k[i])    
        return back        

# Rückgabe als IPA
    # Linke Tasten als IPA zurück geben    
    def l_ipa(self):
        back = []
        for i in self.l_keys:
            back.append(value_k[i])
        return back       
    
    # Mittlere Tasten als IPA zurück geben    
    def m_ipa(self):
        back = []
        for i in self.m_keys:
            back.append(keyboard_to_ipa_v[value_v[i]])
        return back        
    
    # Rechte Tasten als IPA zurück geben
    def r_ipa(self):    
        back = []
        for i in self.r_keys:
            back.append(value_k[i])
        return back        
    
# Rückgabe als komplette Werte-Liste als Integer    
    def values_list(self):
        back = []
        for i in self.l_keys:
            back.append(i)
        for i in self.m_keys:
            back.append(i)
        for i in self.r_keys:
            back.append(i)
        return back
        
# Rückgabe als komplette Werte-Liste als String    
    def values_str(self):
        back = self.values_list()
        string_back = ""
        for i in back:
            string_back += str(i)
        return string_back    
    
# Rückgabe als Keyboard-Liste
    def keyb_list(self):
        back = []
        for i in self.l_keyb():
            back.append(i)
        for i in self.m_keyb():
            back.append(i)    
        for i in self.r_keyb():
            back.append(i)   
        return back
        
# Rückgabe als Keyboard-String
    def keyb_str(self):
        back = self.keyb_list()
        string_back = ""
        for i in back:
            string_back += str(i)
        return string_back    

# Rückgabe als IPA-Liste
    def ipa_list(self):        
        back = []
        left = self.l_ipa()
        middle = self.m_ipa()
        right = self.r_ipa()
        for i in left:
            back.append(i)
        for i in middle:
            back.append(i)
        for i in right:
            back.append(i)
        return back

# Rückgabe als IPA-String
    def ipa_str(self):        
        back = self.ipa_list()
        string_back = ""
        for i in back:
            string_back += str(i)
        return string_back        

# Operatoren überladen usw
    # Schöne Zusammenfassung
    def __repr__(self):
        rueck = "Tastatur in Werten: " + str(self.values()) +"\n"
        rueck += "Tastatur in Keyboard-Layout: " + str(self.keyb()) + "\n"
        rueck += "Tastatur in IPA: " + str(self.ipa()) + "\n"
        rueck += "Aktueller Counterstand: " + str(self.vote())
        return rueck
        
    # Ausgabe für print() in IPA
    def __str__(self):
        return self.ipa()
    
    # "=" überladen: Vergleich ob zwei Tastaturlayouts gleich sind, vote ist egal
    def __eq__(self,  other):
        if (self.l_keys == other.l_keys) and \
            (self.m_keys == other.m_keys) and \
            (self.r_keys == other.r_keys):
            return True
        else:            
            return False
    # ">" überladen
    def __gt__(self, other):
        if self.l_keys > other.l_keys:
            return True
        elif self.l_keys < other.l_keys:
            return False
        elif self.l_keys == other.l_keys:
            if self.m_keys > other.m_keys:
                return True
            elif self.m_keys < other.m_keys:
                return False
            elif self.m_keys == other.m_keys:
                if self.r_keys > other.r_keys:
                    return True
                elif self.r_keys < other.r_keys:
                    return False
                elif self.r_keys == other.r_keys:
                    return False
                else:
                    return False    
            else:
                return False
        else:
            return False
    
    # "<" überladen    
    def __lt__(self):    
        if self.l_keys < other.l_keys:
            return True
        elif self.l_keys > other.l_keys:
            return False
        elif self.l_keys == other.l_keys:
            if self.m_keys < other.m_keys:
                return True
            elif self.m_keys > other.m_keys:
                return False
            elif self.m_keys == other.m_keys:
                if self.r_keys < other.r_keys:
                    return True
                elif self.r_keys > other.r_keys:
                    return False
                elif self.r_keys == other.r_keys:
                    return False
                else:
                    return False    
            else:
                return False
        else:
            return False
        
    # "!=" überladen
    def __ne__(self,  other):
        return not (self == other)

    # ">=" überladen
    def __ge__(self,  other):
        if self > other:
            return True
        elif self == other:
            return True
        else:    
            return False
    
    # "<=" überladen
    def __le__(self):
        if self < other:
            return True
        elif self == other:
            return True
        else:
            return False
    
    # Tastaturlayout plus Eins 
    def increment(self):
        # Zähler durch alle Teile vom rechten/mittleren/linken Tastaturteil
        counter_r = len(self.r_keys)-1
        counter_m = len(self.m_keys)-1
        counter_l = len(self.l_keys)-1
        # Zähler für maximale Größe für Vokale und Konsonanten für Modulo-Rechnung
        modulo_v = len(value_v)
        modulo_k = len(value_k)
                
        # Übertrag ist zu Beginn eins, da Increment
        uebertrag = 1
        
        while counter_r >= 0:
            if uebertrag == 1:
                self.r_keys[counter_r] += 1
            if self.r_keys[counter_r] >= modulo_k:
                uebertrag = 1
                self.r_keys[counter_r] -= modulo_k
            else:
                uebertrag = 0
                break            
            counter_r -= 1
        #Falls immer noch ein Übertrag übrig ist bei den mittleren Tasten weiter machen
        if uebertrag == 1:
            self.m_keys[len(self.m_keys)-1] += 1
            while counter_m >= 0:
                if uebertrag == 1:
                    self.m_keys[counter_m] += 1
                if self.m_keys[counter_m] >= modulo_v:
                    uebertrag = 1
                    self.m_keys[counter_m] -= modulo_v
                else:
                    uebertrag = 0
                    break
        # Falls immer noch ein Übertrag übrig ist bei den linken Tasten weiter machen
        if uebertrag == 1:
            self.l_keys[len(self.l_keys)-1] += 1
            while counter_l >= 0:
                if uebertrag == 1:
                    self.l_keys[counter_l] += 1
                if self.l_keys[counter_l] >= modulo_k:
                    uebertrag = 1
                    self.l_keys[counter_l] -= modulo_k
                else:
                    uebertrag = 0
                    break
        # Falls immer noch ein Übertrag vorhanden ist (also Zahlenüberlauf) dann alles auf Null setzen
        if uebertrag ==1:
            for i in self.l_keys:
                i = 0
            for i in self.m_keys:
                i = 0
            for i in self.r_keys:
                i = 0
            
    # Linke Tastaturseite auf Validität überprüfen
    def valid_l(self):
        back = valid(self.l_keys)
        return back
    
    # Mittlere Tastaturseite auf Validität überprüfen
    def valid_m(self):
        return valid(self.m_keys)
        
    # Rechte Tastaturseite auf Validität überprüfen
    def valid_r(self):
        return valid(self.r_keys)
    
    # Komplette Tastatur auf Gültigkeit überprüfen
    def valid(self):
        if self.valid_l() == self.valid_m() == self.valid_r() == True:
            return True
        else:
            return False
        
        #for counter < len(l_keys):
    
