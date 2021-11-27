# -*- coding: utf-8 -*-

import pandas as pd
from os import system, listdir, mkdir, rename
import pickle
from time import sleep
from random import randint
import matplotlib.pyplot as plt
from datetime import datetime
import xlwt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
pd.options.mode.chained_assignment = None  # default='warn'


### DEFINITION DES LISTES GLOBALES ###

def to_rgb_dec(r,g,b):
    return(float(r)/255.0 , float(g)/255.0 , float(b)/255.0)

list_months = ["Janvier","Fevrier","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Decembre"]
dico_COLORS = { "green_1" : to_rgb_dec(0,128,0) , "green_2" : to_rgb_dec(0,200,0) ,
                "orange_1" : to_rgb_dec(255,165,0) , "orange_2" : to_rgb_dec(255,235,20) ,
                "red_1" : to_rgb_dec(255,0,0) , "red_2" : to_rgb_dec(200,0,200) }
les_chiffres = ['0','1','2','3','4','5','6','7','8','9']


### FONCTIONS OUTILS ###

def already_exists(file_name,place="."):
    existing_files = listdir(place)
    for a_file in existing_files:
        if a_file == file_name:
            return(True)
    return(False)

def get_files_on_type(type_list):
    """ Récupère les fichiers dans l'emplacement local dont l'extension est dans 'type_list'. """
    existing_files = listdir(".") ; the_files = []
    for ext in type_list:
        for elt in existing_files:
            if (len(elt)>len(ext)) and (elt[-len(ext):]==ext):
                try:
                    # unicode(elt) # Plante ici si il y a un accent ds elt
                    the_files.append(elt)
                except:
                    pass
    return(the_files)

def get_parameters(nom_fichier = "parametres.txt"):
    """ Renvoie le dico dico_param construit à partir des infos de fichier 'nom_fichier'. """
    if already_exists(nom_fichier,"./FILES"):
        with open("./FILES/"+nom_fichier,'rb') as param_file:
            outil = pickle.Unpickler(param_file)
            d = outil.load()
        return(d)
    else: # On a besoin de créer le fichier ET de renvoyer des paramètres
        d = defaut_param()
        with open("./FILES/"+nom_fichier,'wb') as param_file:
            outil = pickle.Pickler(param_file)
            outil.dump(d)
        return(d)
    
def defaut_param():
    """ Renvoie le dictionnaires des paramètres par défaut pour init 'paramètres.txt'. """
    dico_param = {'dt_1': 10, 'temps_mini': 10, 'temps_ok': 20, 'dt_2' : 5, 'temps_vert_max': 30, 'temps_orange_max': 60, "barre_cible" : 30, "barre_camion":6}
    return(dico_param)

def init_parameters():
    """ Renvoie le dico dico_param construit à partir des infos du fichier 'parametres.txt'. """
    with open("parametres.txt",'wb') as param_file:
        outil = pickle.Pickler(param_file)
        outil.dump(defaut_param())

def alea_col():
    return( ( float(randint(0,255))/255.0 , float(randint(0,255))/255.0 , float(randint(0,255))/255.0 ) )

def time_to_min(a_time):
    """ Prend time une str sous la forme 'MM:SS' et renvoie SS+60*MM. """
    coord = a_time.split(":") ### coord est une liste du type [16,36] pour 16h36 mais dès fois du type [16,36,22] pour 22 sec ?????!!! ###
    return(int(coord[1]) + 60*int(coord[0]))

def dateday_to_int(date_and_time):
    """ Transforme un objet 'Timestamp' en des entiers donnant le jour, le mois, l'année et l'heure en minutes.
        Timestamp('2020-06-02 00:00:00') """
    [date,time] = str(date_and_time).split(" ")
    [y_,m_,d_] = date.split("-")
    # Traitement de l'heure inexploité ici
    # l = time.split(":")
    # minutes = (int(l[0])*60)+int(l[1])
    return( (int(d_),int(m_),int(y_)) )

def date_inout_to_int(date_inout):
    """ Recoit une chaine de caractère du type "02/06/2020 06:57" et renvoie l'heure associée en minutes. """
    l = date_inout.split(" ")[1].split(":") # 2 ou 3 éléments ds la liste l, cela dépend de l'existence des secondes ou non
    return( int(l[0])*60 + int(l[1]) )

def print_a_time(minutes,extension="min"):
    """ Mets en forme une durée donnée en minutes qui n'excede pas 1j=24*60min. """
    if minutes<60:
        return(str(minutes)+extension)
    else:
        str_min = str(minutes%60)
        if len(str_min)==1: # Un seul chiffre entre 0 et 9
            str_min = "0" + str_min
        return("{0}h".format(str(minutes//60)) + str_min)

def sort_elts(liste,ind_tri):
    """ 'ind_tri' indique sur quelle composante des éléments de liste il faut trier. """
    sorted_list = []
    while len(liste)>=1:
        (element, liste) = extraire_min(liste,ind_tri)
        sorted_list.append(element)
    return(sorted_list)

def extraire_min(liste,num):
    """ Extrait le min de 'liste' par rapport à sa 'num'ieme composante. """
    if liste == []:
        return( (None,[]) )
    else:
        mini = liste[0][num]
        rang = 0
        for indice in range(1,len(liste)):
            if liste[indice][num] < mini:
                mini = liste[indice][num]
                rang = indice
        elt = liste.pop(rang)
        return( (elt,liste) )

def is_int(x):
    """ Vérifie si la chaîne de caractères 'x' est une chaîne d'entiers. """
    if x != "":
        for elt in x:
            if not(elt in les_chiffres):
                return(False)
        return(True)
    else:
        return(False)

def get_max(liste):
    le_max = liste[0]
    for elt in liste:
        if elt > le_max:
            le_max = elt
    return(le_max)

def reverse_list(liste):
    L = []
    for k in range(1,len(liste)+1):
        L.append(liste[len(liste)-k])
    return(L)

def sum_list(liste):
    S = 0
    for x in liste:
        S += x
    return(S)

def mean_list(liste):
    if liste == []:
        return(0)
    S = sum_list(liste)
    return( int( float(S)/float(len(liste)) ) )

def moy_pond(liste_of_couples):
    """ liste_of_couples = [[v1,p1],[v2,p2],...] et renvoie la moyenne des vi pondérés par les poids pi. """
    S = 0 ; poids_tot = 0
    for [vi,pi] in liste_of_couples:
        S += vi*pi ; poids_tot += pi
    return(float(S)/float(poids_tot))

def PICONI_to_PICCONI(x):
    if x == "PICONI":
        return("PICCONI")
    return("COCHU")

def int_stat(repartition):
    """ Renvoie L tq L[k] est le pourcentage de 'repartition[k]' dans 'total' arrondi à l'entier inf ou sup de manière à avoir un total de 100%. """
    total = sum_list(repartition)
    stat_naive = [] # Stat naïves obtenus en arrondissant à l'entier inférieur
    for val in repartition:
        stat_naive.append( int(100*float(val)/float(total)) ) # En pour 100
    lack = 100-sum_list(stat_naive) # Pourcentage manquant
    
    stat_float = [] # Statistiques en flottants à deux chiffres après la virgule enregistrés en pour 1000 (12.12 -> 1212)
    for val in repartition:
        stat_float.append( int(10000*float(val)/float(total)) ) # En pour 10000
    for k in range(0,len(stat_float)):
        stat_float[k] = [k,stat_float[k]//100,stat_float[k]%100]
    stat_float_sorted = reverse_list(sort_elts(stat_float,2)) # On trie par ordre décroissant
    
    stat_int = [None for k in range(0,len(stat_naive))] # On créé la liste qui accueillera les stats
    i = 0
    while i<len(stat_float_sorted):
        [k,stat_k,_] = stat_float_sorted[i]
        if i<lack: # lack=2 => il faut rehausser seulement l'indice 0 et 1 de stat_float_sorted
            stat_int[k] = stat_k+1
        else:
            stat_int[k] = stat_k
        i+=1
    return(stat_int)

def deux_dec_stat(repartition):
    """ Renvoie les pourcentages à deux chiffres après la virgule. """
    total = sum_list(repartition)
    if sum_list(repartition) != total:
        print("\n--> Erreur de comptage des camions dans leur catégorie !")
    stat_float = []
    for val in repartition:
        stat_float.append( float(int(10000*float(val)/float(total)))/100 )
    return(stat_float)    

def most_present_value(liste,ind):
    """ ind=1 pour recenser les mois et ind=2 pour recenser les années. """
    dico_count = {}
    for triplet in liste:
        if triplet[ind] in dico_count.keys():
            dico_count[triplet[ind]] += 1
        else:
            dico_count[triplet[ind]] = 1
    L = []
    for (key,val) in dico_count.items():
        L.append([key,val])
    sorted_L = sort_elts(L,1) # On trie sur la première composante (ordre croissant)
    return(reverse_list(sorted_L)[0][0]) # On renvoie le numéro du mois ou de l'année qui apparait le plus

def update_loading_1(window,x):
    """ Actualise l'affichage de la barre de chargement sur la fenêtre d'accueil 'window' avel la valeur x en %.
        create_rectangle(topleft_x,top_left_y,bottomright_x,bottom_right_y) """
    window.cnv.itemconfigure(1, text="CHARGEMENT : " + str(x) + "%")
    window.cnv.delete("loading_green_rect") # On remplace les rectangles verts au lieu d'en créer des tonnes
    window.cnv.create_rectangle(20,40,20+2*x,70, fill="green", tag="loading_green_rect") ; window.root.update()

def update_loading_2(window,x):
    """ Actualise l'affichage de la barre de chargement sur la fenêtre de menu 'window' avel la valeur x en %. """
    window.cnv.itemconfigure(1, text="Enregistrement en cours : " + str(x) + "%")
    window.cnv.delete("loading_green_rect") # On remplace les rectangles verts au lieu d'en créer des tonnes
    window.cnv.create_rectangle(100,40,100+2*x,70, fill="green", tag="loading_green_rect") ; window.root.update()



