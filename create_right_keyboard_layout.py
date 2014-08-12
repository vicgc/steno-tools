#!/usr/bin/python3
# -*- coding: utf-8 -*-
# storage-2.server.selfnet.de 141.70.127.236

#import sys
#import os
#import IPA_Methods
import Keyboard_Methods
#import threading
#import queue
import copy
import multiprocessing

debug = True

# Funktionen ===================================================================

# Zahlensysteme umwandeln
def baseN(num, base, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    if num == 0:
        return "0"

    if num < 0:
        return '-' + baseN((-1) * num, base, numerals)

    if not 2 <= base <= len(numerals):
        raise ValueError('Base must be between 2-%d' % len(numerals))

    left_digits = num // base
    if left_digits == 0:
        return numerals[int(num % base)]
    else:
        return baseN(left_digits, base, numerals) + numerals[int(num % base)]




# Hauptprogramm ================================================================

max_layouts = 19**10
basis= int(19)
cores = 24           # Muss mindestens 2 sein!
links_grenzen_base_10 = []
links_grenzen_base_19 = []
ausgabefile = []

# nach Menge der cores, gesamten Range aufteilen
counter = 0
while counter < cores:
    # Startpunkte für Threads ausrechnen
    links_grenzen_base_10.append(int(counter * max_layouts / cores))
    # Startpunkte für Threads in Base 19 umrechnen
    links_grenzen_base_19.append(baseN(links_grenzen_base_10[counter], basis))
    # Ausgabefile Namen generieren
    ausgabefile.append("rechtes_layout_file_"+str(counter)+".txt")
    counter += 1
    
print("Schleife für Abstände generieren ist durch")
# Alles in String mit ; als Trennzeichen umwandeln

tastatur_grenzen=[]

for jedes in links_grenzen_base_19:
    # In "Keyboard"-Speicher-Schreibweise umbauen
    jedes = jedes.replace("0","0;")
    jedes = jedes.replace("1","1;")
    jedes = jedes.replace("2","2;")
    jedes = jedes.replace("3","3;")
    jedes = jedes.replace("4","4;")
    jedes = jedes.replace("5","5;")
    jedes = jedes.replace("6","6;")
    jedes = jedes.replace("7","7;")
    jedes = jedes.replace("8","8;")
    jedes = jedes.replace("9","9;")
    jedes = jedes.replace("a","10;")
    jedes = jedes.replace("b","11;")
    jedes = jedes.replace("c","12;")
    jedes = jedes.replace("d","13;")
    jedes = jedes.replace("e","14;")
    jedes = jedes.replace("f","15;")
    jedes = jedes.replace("g","16;")
    jedes = jedes.replace("h","17;")
    jedes = jedes.replace("i","18;")
    #Letzten Strichpunkt abschneiden
    jedes = jedes[:-1]
    # führende Nullen ergänzen damit es "Keyboard-CSV-Layout" hat
    while jedes.count(";") < 9:
        jedes = "0;"+jedes
    # Auftrennen in Unterliste wie CSV
    jedes = copy.deepcopy(jedes.split(";"))
    print("In Erstellungsscheilfe: ", jedes)
    tastatur_grenzen.append(copy.deepcopy(jedes))
    print("Tastatur_grenzen nach deepcopy: ", tastatur_grenzen)

# Aufbereitung der Grenzen abgeschlossen =======================================

# Funktion für Threads, dafür threading Klasse überladen
# eigentliche Thread-Funktion
def create_valid_layouts(argument):
    name ,  id ,  start,  end,  output_file = argument
    print ("Starting Name: " + name + " ID: " + str(id)) 
    # Ausgabedatei öffnen versuchen   
    try:
        output_file_handle = open(output_file,"w")
        print ("Ausgabefile: " + output_file + " geöffnet.")
    except:
        print ("Ausgabedatei öffnen nicht erfolgreich!")
        sys.exit(0)
    
    flush_counter = 0
    
    # eigentlicher Unterabschnitt der die Tastaturlayouts kreirt und raus schreibt bei Gültigkeit    
    while True:
        # Aufhören wenn Endwert erreicht ist
        if start == end:
            print ("Bin durch in " + self.name)
            break
        start = Keyboard_Methods.increment(start, basis)
        valide = Keyboard_Methods.valid(start)
        if valide == True:
            output_file_handle.write(\
                str(start[0])+";"+\
                str(start[1])+";"+\
                str(start[2])+";"+\
                str(start[3])+";"+\
                str(start[4])+";"+\
                str(start[5])+";"+\
                str(start[6])+";"+\
                str(start[7])+";"+\
                str(start[8])+";"+\
                str(start[9])+"\n")
            flush_counter += 1
            if flush_counter == 99:
                flush_counter = 0
                output_file_handle.flush()
    
    output_file_handle.close()
    print("Datei geschlossen: "+output_file)
    print("Finished: " + name)
    return True

for jedes in links_grenzen_base_19:
    print("Nochmal: ", jedes)

def main():
    print("Alle Prozesse anlegen..")
    mein_process_0 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 0",\
                            0,\
                            tastatur_grenzen[0],\
                            tastatur_grenzen[1],\
                            ausgabefile[0])] )
    mein_process_1 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 1",\
                            1,\
                            tastatur_grenzen[1],\
                            tastatur_grenzen[2],\
                            ausgabefile[1])] )
    mein_process_2 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 2",\
                            2,\
                            tastatur_grenzen[2],\
                            tastatur_grenzen[3],\
                            ausgabefile[2])] )
    mein_process_3 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 3",\
                            3,\
                            tastatur_grenzen[3],\
                            tastatur_grenzen[4],\
                            ausgabefile[3])] )
    mein_process_4 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 4",\
                            4,\
                            tastatur_grenzen[4],\
                            tastatur_grenzen[5],\
                            ausgabefile[4])] )
    mein_process_5 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 5",\
                            5,\
                            tastatur_grenzen[5],\
                            tastatur_grenzen[6],\
                            ausgabefile[5])] )
    mein_process_6 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 6",\
                            6,\
                            tastatur_grenzen[6],\
                            tastatur_grenzen[7],\
                            ausgabefile[6])] )
    mein_process_7 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 7",\
                            7,\
                            tastatur_grenzen[7],\
                            tastatur_grenzen[8],\
                            ausgabefile[7])] )
    mein_process_8 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 8",\
                            8,\
                            tastatur_grenzen[8],\
                            tastatur_grenzen[9],\
                            ausgabefile[8])] )
    mein_process_9 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 9",\
                            9,\
                            tastatur_grenzen[9],\
                            tastatur_grenzen[10],\
                            ausgabefile[9])] )
    mein_process_10 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 10",\
                            10,\
                            tastatur_grenzen[10],\
                            tastatur_grenzen[11],\
                            ausgabefile[10])] )
    mein_process_11 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 11",\
                            11,\
                            tastatur_grenzen[11],\
                            tastatur_grenzen[12],\
                            ausgabefile[11])] )
    mein_process_12 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 12",\
                            12,\
                            tastatur_grenzen[12],\
                            tastatur_grenzen[13],\
                            ausgabefile[12])] )
    mein_process_13 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 13",\
                            13,\
                            tastatur_grenzen[13],\
                            tastatur_grenzen[14],\
                            ausgabefile[13])] )
    mein_process_14 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 14",\
                            14,\
                            tastatur_grenzen[14],\
                            tastatur_grenzen[15],\
                            ausgabefile[14])] )
    mein_process_15 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 15",\
                            15,\
                            tastatur_grenzen[15],\
                            tastatur_grenzen[16],\
                            ausgabefile[15])] )
    mein_process_16 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 16",\
                            16,\
                            tastatur_grenzen[16],\
                            tastatur_grenzen[17],\
                            ausgabefile[16])] )
    mein_process_17 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 17",\
                            17,\
                            tastatur_grenzen[17],\
                            tastatur_grenzen[18],\
                            ausgabefile[17])] )
    mein_process_18 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 18",\
                            18,\
                            tastatur_grenzen[18],\
                            tastatur_grenzen[19],\
                            ausgabefile[18])] )
    mein_process_19 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 19",\
                            19,\
                            tastatur_grenzen[19],\
                            tastatur_grenzen[20],\
                            ausgabefile[19])] )
    mein_process_20 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 20",\
                            20,\
                            tastatur_grenzen[20],\
                            tastatur_grenzen[21],\
                            ausgabefile[20])] )
    mein_process_21 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 21",\
                            21,\
                            tastatur_grenzen[21],\
                            tastatur_grenzen[22],\
                            ausgabefile[21])] )
    mein_process_22 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 22",\
                            22,\
                            tastatur_grenzen[22],\
                            tastatur_grenzen[23],\
                            ausgabefile[22])] )
    mein_process_23 = multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread 23",\
                            23,\
                            tastatur_grenzen[23],\
                            tastatur_grenzen[0],\
                            ausgabefile[23])] )
    print("Alle Prozese angelegt..")
    print ("Alle Prozesse starten...")
    mein_process_0.start()
    mein_process_1.start()
    mein_process_2.start()
    mein_process_3.start()
    mein_process_4.start()
    mein_process_5.start()
    mein_process_6.start()
    mein_process_7.start()
    mein_process_8.start()
    mein_process_9.start()
    mein_process_10.start()
    mein_process_11.start()
    mein_process_12.start()
    mein_process_13.start()
    mein_process_14.start()
    mein_process_15.start()
    mein_process_16.start()
    mein_process_17.start()
    mein_process_18.start()
    mein_process_19.start()
    mein_process_20.start()
    mein_process_21.start()
    mein_process_22.start()
    mein_process_23.start()
    print("Alle Prozesse gestartet")    
    
    """
    
    while counter < cores:
        if counter != cores -1 :
            mein_process.append(\
                    multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread "+str(counter),\
                            counter,\
                            tastatur_grenzen[counter],\
                            tastatur_grenzen[counter+1],\
                            ausgabefile[counter])] ) )
        elif counter == cores -1:
            mein_process.append(\
                    multiprocessing.Process(\
                        target=create_valid_layouts,args=[(\
                            "Thread "+str(counter),\
                            counter,\
                            tastatur_grenzen[counter],\
                            tastatur_grenzen[0],\
                            ausgabefile[counter])] ) )
    """
   
    print("Alles fertig!")

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()

print("BaseN: ", baseN(123, 19))
print ("Programm ist durchgelaufen!")
"""
for i in range(cores):
    links_grenzen.append(baseN(int(i*(max_layouts/cores)), basis))
    print (baseN(links_grenzen[i], basis))
    print (i, links_grenzen[i])
    print (type(links_grenzen[i]))

"""












