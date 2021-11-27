# -*- coding: utf-8 -*-


from Code_outils import *


### FONCTIONS PRINCIPALES DE TRAITEMENT DES DONNEES ###

def get_dataframe(nom_fichier = "GYPSE 06.xlsx"):
    """ Renvoie la dataframe associée aux données de 'nom_fichier' et aux 4 champs précisés. """
    input_df = pd.read_excel(nom_fichier, delimiter=';')
    df = input_df[["Plaque camion","Date","Date du poids d'entree","Date du poids de sortie","Code transporteur"]]
    """
    # df.drop(df.loc[df["Plaque camion"]=="nan"].index, inplace=True)
    # df["Plaque camion"].dropna()
    """
    # On va parcourir la dataframe à l'envers pour enlever toutes les lignes vides
    lignes_vides = list(pd.isna(df["Plaque camion"])) ; n = len(lignes_vides) ; ind = n-1
    while lignes_vides[ind] and ind>=0: # Tant qu'on a affaire à une ligne vide
        df.drop(ind,inplace=True)
        ind -= 1
    return(df)


def historique_of_the_day(df,the_day = 2,the_month = 6,the_year = 2020):
    """ Retourne une liste dont chaque élément correspond à une entrée ou une sortie le jour correspondant.
        On stocke avec 'IN' le temps passé au fond (en min) pour le camion. On ne stocke rien avec 'OUT'. """
    day_resume = [] ; this_day = (the_day,the_month,the_year)
    for (ind_ligne,contenu_ligne) in df.iterrows():
        if contenu_ligne["Date"] == this_day: # Ligne à prendre 
            [num,date_day,time_in,time_out,code_transp] = list(contenu_ligne)
            # On inverse les positions time_in et time_out pour l'algo de tri
            day_resume.append(["IN",date_day,time_in,time_out,code_transp]) # On ajoute l'entrée
            day_resume.append(["OUT",date_day,time_out,time_in,code_transp]) # On ajoute la sortie
    return(day_resume)


def Enregister_graphiques(big_DICO,mean_stat,dates_dispo,dico_param,month_num,year_num,arrondir_stat,window):
    """ Enregistre tous les graphiques dans le dossier dont le nom est défini ci-dessous. """
    mkdir("Camions gypse " + list_months[dates_dispo[0][1]-1])
    len_ddispo = len(dates_dispo)
    the_step = 100//(len_ddispo+3) # 100 // Nb total de graphiques
    # Jours individuels
    for progress in range(0,len_ddispo):
        (d,m,y) = dates_dispo[progress]
        Create_single_day_graph(big_DICO,dico_param,mean_stat,d,month_num,year_num) # Création du graphe de la journée
        zero_m = "" ; zero_d = ""
        if m<10:
            zero_m = "0"
        if d<10:
            zero_d = "0"
        graph_name = "Camions gypse " + zero_d + str(d) + "_" + zero_m + str(m) + "_" + str(y)
        plt.savefig("Camions gypse " + list_months[m-1] + "./" + graph_name)
        plt.close()
        update_loading_2(window,(progress+1)*the_step)
    # Jours réunis
    Create_all_day_graph(big_DICO["dico_t_in"],big_DICO["dico_wttime"],dates_dispo,dico_param["barre_cible"],month_num,year_num)
    plt.savefig("Camions gypse " + list_months[month_num-1] + "./" + "Camions gypse - cumul graphiques " + list_months[month_num-1])
    plt.close()
    update_loading_2(window,(len_ddispo+1)*the_step)
    # Graphe du nb de camions/temps d'attente
    Create_waiting_trucks_graph(big_DICO["dico_stat_trucks"],big_DICO["dico_outnb_trucks"],big_DICO["dico_mean_month"],big_DICO["dico_zone_trucks"],dico_param,month_num,year_num,arrondir_stat)
    plt.savefig("Camions gypse " + list_months[month_num-1] + "./" + "Camions gypse - stat temps")
    plt.close()
    update_loading_2(window,(len_ddispo+2)*the_step)
    # Graphe de la courbe moyenne du mois
    Create_mean_curve(mean_stat[0],mean_stat[1],dico_param["barre_cible"],month_num,year_num)
    plt.savefig("Camions gypse " + list_months[month_num-1] + "./" + "Camions gypse - graphique moyen")
    plt.close()
    update_loading_2(window,(len_ddispo+3)*the_step)


def Export_datas(big_DICO,dico_param,dates_dispo,les_anomalies,month_num,year_num,arrondir_stat=False):
    """ Exporte les donnees analysees dans un fichier '.xls'. Taille standard d'une colonne = 2962 """
    workbook = xlwt.Workbook() # Création de l'objet excel.
    sheet = workbook.add_sheet("Bilan du mois") # Rajout d'une feuille.
    # Initialisation des noms des têtes de colonne : les têtes de colonnes prennent les 2 premières lignes
    sheet.write(0,0,"JOURS")
    sheet.write(0,2,"Nombre de camions")
    sheet.write(1,1,"PICCONI") ; sheet.write(1,2,"COCHU") ; sheet.write(1,3,"PICCONI+COCHU")
    sheet.col(3).width = 4000 # On élargit 'PICCONI+COCHU'
    sheet.write(0,5,"Temps moyen passe au fond")
    sheet.write(1,4,"PICCONI") ; sheet.write(1,5,"COCHU") ; sheet.write(1,6,"PICCONI+COCHU")
    sheet.col(6).width = 4000 # On élargit 'PICCONI+COCHU'
    sheet.write(0,7,"+ {0} camions au fond pendant".format(dico_param["barre_camion"]))
    sheet.col(7).width = 6500
    sheet.write(len(dates_dispo)+3,0,"Mois de {0}".format(list_months[month_num]))
    sheet.col(0).width = 3500

    ## On complète chaque jour
    for i in range(0,len(dates_dispo)):
        day_num = dates_dispo[i][0]
        sheet.write(i+2,0,"{0} {1} {2}".format(day_num,list_months[month_num-1],year_num)) # Case de la colonne de gauche donnant la date du jour
        les_wttime = [ big_DICO["dico_transp"]["PICCONI"][day_num][1] , big_DICO["dico_transp"]["COCHU"][day_num][1] ]
        sheet.write(i+2,1,len(les_wttime[0])) # nb trucks PICCONI
        sheet.write(i+2,2,len(les_wttime[1])) # nb trucks COCHU
        sheet.write(i+2,3,len(les_wttime[0])+len(les_wttime[1])) # nb trucks PICCONI+COCHU
        sheet.write(i+2,4,mean_list(les_wttime[0])) # mean time PICCONI
        sheet.write(i+2,5,mean_list(les_wttime[1])) # mean time COCHU
        sheet.write(i+2,6,mean_list(les_wttime[0]+les_wttime[1])) # mean time PICCONI+COCHU
        surplus = big_DICO["dico_outnb_trucks"][day_num]
        sheet.write(i+2,7,print_a_time(big_DICO["dico_outnb_trucks"][day_num],"min")) # Barre_camion         

    ## On complète les données du mois
    nb_trucks_month = [sum_list(big_DICO["dico_zone_trucks"]["PICCONI"]),sum_list(big_DICO["dico_zone_trucks"]["COCHU"])]
    sheet.write(len(dates_dispo)+3,1,nb_trucks_month[0])
    sheet.write(len(dates_dispo)+3,2,nb_trucks_month[1])
    sheet.write(len(dates_dispo)+3,3,nb_trucks_month[0]+nb_trucks_month[1])
    sheet.write(len(dates_dispo)+3,4,big_DICO["dico_mean_month"]["PICCONI"])
    sheet.write(len(dates_dispo)+3,5,big_DICO["dico_mean_month"]["COCHU"])

    # Calcul des temps moyens et nb_to_trucks des transporteur sur le mois
    stat_trucks = [0,0,0] # [tps_att<30min , 30min<=tps_att<=1h , 1h<tps_att] -> Convention du tableur Excel
    for ind in [0,1,2]: # On somme les totaux de chq constructeur zone par zone
        stat_trucks[ind] = big_DICO["dico_zone_trucks"]["PICCONI"][ind] + big_DICO["dico_zone_trucks"]["COCHU"][ind]
    nb_trucks_tot = sum_list(stat_trucks)
    moy_wttime = moy_pond( [ [big_DICO["dico_mean_month"]["PICCONI"],nb_trucks_month[0]],
                             [big_DICO["dico_mean_month"]["COCHU"],nb_trucks_month[1]] ] )
    rates = { "ALL":[] , "PICCONI":[] , "COCHU":[] }
    if arrondir_stat:
        rates["ALL"] = int_stat(stat_trucks) # La fonction fait tout le boulot de calcul et mise en forme des stats sur 'stat_trucks'
        rates["PICCONI"] = int_stat(big_DICO["dico_zone_trucks"]["PICCONI"])
        rates["COCHU"] = int_stat(big_DICO["dico_zone_trucks"]["COCHU"])
        moy_wttime = int(moy_wttime)
    else:
        rates["ALL"] = deux_dec_stat(stat_trucks)
        rates["PICCONI"] = deux_dec_stat(big_DICO["dico_zone_trucks"]["PICCONI"])
        rates["COCHU"] = deux_dec_stat(big_DICO["dico_zone_trucks"]["COCHU"])
        moy_wttime = float(int(100*moy_wttime))/100
    sheet.write(len(dates_dispo)+3,6,moy_wttime)
    sheet.write(len(dates_dispo)+3,7,print_a_time(sum_list(big_DICO["dico_outnb_trucks"].values()),""))

    # Affichage des zones de couleur
    sheet.write(len(dates_dispo)+5,1,"Zone verte") ; sheet.write(len(dates_dispo)+5,2,"Zone orange") ; sheet.write(len(dates_dispo)+5,3,"Zone rouge")
    sheet.write(len(dates_dispo)+6,0,"PICCONI")
    sheet.write(len(dates_dispo)+6,1,str(rates["PICCONI"][0])+"%") ; sheet.write(len(dates_dispo)+6,2,str(rates["PICCONI"][1])+"%") ; sheet.write(len(dates_dispo)+6,3,str(rates["PICCONI"][2])+"%")
    sheet.write(len(dates_dispo)+7,0,"COCHU")
    sheet.write(len(dates_dispo)+7,1,str(rates["COCHU"][0])+"%") ; sheet.write(len(dates_dispo)+7,2,str(rates["COCHU"][1])+"%") ; sheet.write(len(dates_dispo)+7,3,str(rates["COCHU"][2])+"%")
    sheet.write(len(dates_dispo)+8,0,"PICCONI+COCHU")
    sheet.write(len(dates_dispo)+8,1,str(rates["ALL"][0])+"%") ; sheet.write(len(dates_dispo)+8,2,str(rates["ALL"][1])+"%") ; sheet.write(len(dates_dispo)+8,3,str(rates["ALL"][2])+"%")
    
    # Affichage des anomalies
    if les_anomalies!=[]:
        sheet.write(1,9,"Camions en anomalie en {0}".format(list_months[month_num-1]))
        sheet.col(9).width = 13000
        ind = 2
        for [plaque_cam,(d,m,y),time_in,time_out,code_transp] in les_anomalies:
            txt_to_print = "{0} : {1} - le {3} {4} {5} a {6} - {2}min.".format(code_transp,plaque_cam,time_out-time_in,d,list_months[month_num-1],y,print_a_time(time_in,""))
            sheet.write(ind,9,txt_to_print)
            ind += 1
    
    workbook.save("Analyse_de_{0}.xls".format(list_months[month_num-1]))
                      

### FONCTIONS DE CREATION DES LISTES DE DONNEES POUR LES GRAPHIQUES ###

def Calculate_data_lists(df,dates_dispo,month_num,year_num,dico_param,window):
    """ Renvoie l'ensemble des listes nécessaires pour tracer tous les graphiques disponibles :
        les_t_in_out / les_time_in / les_waiting_time / les_nb_trucks /
        - dico_t_in_out = { day_num : liste_triée_time_in_out_de_ce_jour , ...} ### Les valeurs sont doublées pour dico_nb_trucks !!!
        - dico_t_in = { day_num : liste_triée_time_in_de_ce_jour , ...}
        - dico_wttime = { day_num : liste_des_waiting_time_de_ce_jour , ...}
        - dico_transp = { "PICCONI" : dico_PICCONI , "COCHU" : dico_COCHU }
          | dico_PICCONI = { day_num : [liste_triée_time_in_PICCONI_de_ce_jour,liste_wttime_PICCONI] , ...}
          | dico_COCHU = {...}
        - dico_nb_trucks = { day_num : liste adaptée du nb de camions calée sur les_waiting , ... } ### En relation avec dico_t_in_out
        - dico_outnb_trucks = { day_num : temps passé au dessus de la barre_camion ce jour , ... }
        - dico_ylim_ax1 = { day_num : liste de la graduation maxi à afficher sur l'axe de gauche pour un single_day_graph , ...} # the_ylim est calculé pour l'axe 1 à partir du max des wttime et du max des nb de camions
        - mean_stat = [time_in_mean,waiting_time_mean]
        - dico_stat_truck = { "PICCONI" : stat_trucks_PICCONI , "COCHU" : stat_trucks_COCHU }
          | stat_trucks_PICCONI : {0:[liste wttime entre 0 et dt_2] , dt_2 : liste wttime entre dt_2 et 2*dt_2 , ... , 120 : liste wttime >= 120 }
          | stat_trucks_COCHU : {0:[liste wttime entre 0 et dt_2] , dt_2 : liste wttime entre dt_2 et 2*dt_2 , ... , 120 : liste wttime >= 120 }
        - dico_mean_month = { "PICCONI" : month_mean_time_PICCONI , "COCHU" : month_mean_time_COCHU }
        - dico_zone_trucks = { "PICCONI" : [nb_trucks_VERT,nb_trucks_ORANGE,nb_trucks_RED] ,
                               "COCHU" : [nb_trucks_VERT,nb_trucks_ORANGE,nb_trucks_RED] }
        """
    
    ## INIT des dicos 'classiques'
    dico_t_in_out = {}
    dico_t_in = {}
    dico_wttime = {}
    dico_transp = { "PICCONI":{} , "COCHU":{} }
    dico_nb_trucks = {}
    dico_outnb_trucks = {}
    dico_ylim_ax1 = {}
    dico_zone_trucks = { "PICCONI":[0,0,0] , "COCHU":[0,0,0] }

    ## INIT du dico pour la courbe moyenne
    dico_mean = {} ; dt_1 = dico_param["dt_1"] ; k = 6*60 # 6h en minutes
    while k<=18*60: # On va jusqu'à 18h maxi
        dico_mean[k] = []
        k += dt_1

    ## INIT des dicos pour le graphe en barres
    dico_stat_trucks = { "PICCONI":{} , "COCHU":{} } ; dt_2 = dico_param["dt_2"] ; k = 0
    while k<=120: # On va jusqu'à 120min maxi
        dico_stat_trucks["PICCONI"][k] = [] ; dico_stat_trucks["COCHU"][k] = []
        k += dt_2

    ## Gestion affichage de la barre de chargement
    loading_step = 100//len(dates_dispo)

    ## Passage en revue de chaque jour un à un
    for progress in range(0,len(dates_dispo)): # Seul le jour est a récupérer
        day_num = dates_dispo[progress][0]
        ordered_day = sort_elts(historique_of_the_day(df,day_num,month_num,year_num),2)
        
        dico_t_in[day_num] = []
        dico_wttime[day_num] = []
        dico_t_in_out[day_num] = []
        dico_transp["PICCONI"][day_num] = [[],[]] ; dico_transp["COCHU"][day_num] = [[],[]]
        dico_nb_trucks[day_num] = [0]
        waiting_time_max = 0 ; nb_trucks_x10_max = 0
        dico_outnb_trucks[day_num] = [0,-1] # en [0] le temps cumulé et en [1] l'heure (en min) de montée du dernier pic (-1 signifie qu'on est PAS en situation critique)    
        
        for event in ordered_day:
            time = event[2] # (time = time_in) si event est "IN" et (time = time_out) si event est "OUT"
            hour = time//60
            minute_dec = float(time-60*hour)/60 # minute décimal (0min=0,30min=0.5,60min=1)
            
            if event[0] == "IN":
                
                ## Ajout des temps in et out et des temps d'attente (en minutes)
                dico_t_in[day_num].append(hour+minute_dec) # Abscisse
                dico_wttime[day_num].append(event[3]-time) # Ordonnée
                waiting_time_max = max(event[3]-time,waiting_time_max)
                dico_transp[event[4]][day_num][0].append(hour+minute_dec)
                dico_transp[event[4]][day_num][1].append(event[3]-time)
                
                ## Ajout des temps in et out ainsi que les nombres de camions [Trait vertical : (nv temps,ancienne valeur) ---> (nv temps,nvlle valeur)]
                dico_t_in_out[day_num].append(hour+minute_dec) # Abscisse
                dico_t_in_out[day_num].append(hour+minute_dec) # On double car il faut deux points pour faire une verticale
                dico_nb_trucks[day_num].append(dico_nb_trucks[day_num][-1]) # Ordonnéee -> Ancienne valeur
                dico_nb_trucks[day_num].append(dico_nb_trucks[day_num][-1]+10) # -> Nouvelle valeur
                nb_trucks_x10_max = max(dico_nb_trucks[day_num][-1],nb_trucks_x10_max)

                ## Ajout des temps in pour la courbe moyenne du mois -> Besoin de discrétiser le temps en tranches de largeur 'dt_1'
                time_in_arrondi = dt_1*(time//dt_1) # On arrondi l'heure d'entrée au + grand multiple de dt_1 inférieur
                if 6*60 <= time_in_arrondi <= 18*60: # <=> if time_in_arrondi in dico_means.keys()
                    dico_mean[time_in_arrondi].append(event[3]-time) # On rajoute le temps d'attente (= time_out - time_in)
                else:
                    print( "ERREUR : Depassement des horaires [6h->18h] avec {0}h{1} le {2}".format(time//60,time%60,day_num) )
                    dico_mean[time_in_arrondi] = [event[3]-time] # On rajoute quand même
                
                ## Actualtisation du cumul_time si on détecte une situtation critique (>= barre_camion)
                if dico_nb_trucks[day_num][-1] >= 10*dico_param["barre_camion"]: # Détection d'une situation critique
                    if dico_outnb_trucks[day_num][1] == (-1): # On passe bien en situation critique
                        dico_outnb_trucks[day_num] = [dico_outnb_trucks[day_num][0],time]

                ## Ajout du wttime pour le graphe des statistiques camion en barres
                tps_att = min(dt_2*((event[3]-time)//dt_2),120) # On arrondi l'heure d'entrée au + grand multiple de dt_2 inférieur et on limite à 120min
                dico_stat_trucks[event[4]][tps_att].append(event[3]-time) # On stocke le vrai temps pour pouvoir moyenner

                ## Classification du camion dans une zone de couleur
                if event[3]-time < dico_param["temps_vert_max"]: # tps_att=30 correspond à [30,34] donc en prenant les <30, on prend les <=25 et donc ceux jusqu'à 29min
                    dico_zone_trucks[event[4]][0] += 1
                elif event[3]-time < dico_param["temps_orange_max"]: # 60 correspond à [60,65]
                    dico_zone_trucks[event[4]][1] += 1
                else: # temps_orange_max <= tps_att:
                    dico_zone_trucks[event[4]][2] += 1
                    
            elif event[0] == "OUT":

                ## Affichage du nombre de camions
                dico_t_in_out[day_num].append(hour+minute_dec) # Abscisse
                dico_t_in_out[day_num].append(hour+minute_dec) # On double car il faut deux points pour faire une verticale
                dico_nb_trucks[day_num].append(dico_nb_trucks[day_num][-1]) # Ordonnéee -> Ancienne valeur
                dico_nb_trucks[day_num].append(dico_nb_trucks[day_num][-1]-10) # -> Nouvelle valeur

                ## Actualtisation du cumul_time si on détecte une fin de situtation critique (< barre_camion)
                if dico_nb_trucks[day_num][-1] < 10*dico_param["barre_camion"]: # Détection d'une fin de situation critique
                    if dico_outnb_trucks[day_num][1] != (-1): # On sort bien d'une situation critique
                        dico_outnb_trucks[day_num][0] = dico_outnb_trucks[day_num][0]+(event[2]-dico_outnb_trucks[day_num][1]) # On rajoute le delta relevé au cumul total de temps (delta=time_out-time_in)
                        dico_outnb_trucks[day_num][1] = -1

        ## Traitement pour l'axe y de ax1
        dico_nb_trucks[day_num].pop(0) # C'était la valeur par défaut pour initialiser et faire fonctionner le '[-1]' ds la boucle for
        waiting_time_max = 10*((waiting_time_max//10)+1) # On arrondit au multiple de 10 SUPERIEUR
        dico_ylim_ax1[day_num] = max(waiting_time_max,nb_trucks_x10_max+10) # C'est the_ylim !

        ## Traitement pour le temps cumulé au dessus de la 'barre_camion'
        dico_outnb_trucks[day_num] = dico_outnb_trucks[day_num][0] # On ne garde que le temps cumulé

        ## Actualisation de la barre de chargement
        update_loading_1(window,progress*loading_step) 

    ## SORTIE de la boucle FOR ! ##
        
    ## Traitement pour la courbe moyenne
    # On fait le ménage
    for key in dico_mean.keys():
        if dico_mean[key] == []:
            dico_mean.pop(key)
    # On trie les éléments avant de séparer les couples
    L = []
    for (a,b) in dico_mean.items(): # On ne les récupère pas forcément dans l'ordre (pour cela qu'on trie juste après)
        L.append([a,b])
    L = sort_elts(L,0)
    # On peut maintenant séparer les couples
    mean_stat = [[],[]] # mean_stat = [time_in_mean,waiting_time_mean]
    for [a,b] in L:
        hour = a//60
        minute_dec = float(a-60*hour)/60
        mean_stat[0].append(hour+minute_dec) ; mean_stat[1].append(mean_list(b))

    # Calcul des temps moyens et nb_to_trucks des transporteur sur le mois
    dico_mean_month = { "PICCONI" : [] , "COCHU" : [] }
    for code_transp in ["PICCONI","COCHU"]:
        for une_liste in dico_stat_trucks[code_transp].values(): # une_liste correspond aux wttime d'un intervalle [k,k+dt_2[
            dico_mean_month[code_transp] += une_liste
        dico_mean_month[code_transp] = mean_list(dico_mean_month[code_transp]) # On stocke mean_time_month_fot_this_transp

    update_loading_1(window,100)
    # On renvoie tous les dictionnaires construits
    big_DICO = {}
    big_DICO["dico_t_in"] = dico_t_in
    big_DICO["dico_t_in_out"] = dico_t_in_out
    big_DICO["dico_wttime"] = dico_wttime
    big_DICO["dico_transp"] = dico_transp
    big_DICO["dico_nb_trucks"] = dico_nb_trucks
    big_DICO["dico_outnb_trucks"] = dico_outnb_trucks
    big_DICO["dico_ylim_ax1"] = dico_ylim_ax1
    big_DICO["dico_stat_trucks"] = dico_stat_trucks
    big_DICO["dico_mean_month"] = dico_mean_month
    big_DICO["dico_zone_trucks"] = dico_zone_trucks
    return(big_DICO,mean_stat)


### FONCTIONS DE TRACE DES GRAPHIQUES ###

def Create_single_day_graph(big_DICO,dico_param,mean_stat,day_num,month_num,year_num):
    """ Affiche le graphique du jour passé en argument. """

    # On récupère toutes les listes de valeurs
    les_time_in = big_DICO["dico_t_in"][day_num]
    les_time_in_out = big_DICO["dico_t_in_out"][day_num]
    les_wttime = big_DICO["dico_wttime"][day_num]
    les_nb_trucks = big_DICO["dico_nb_trucks"][day_num]
    dico_wttime_transp = {}
    dico_wttime_transp["PICCONI"] = big_DICO["dico_transp"]["PICCONI"][day_num] # du type [liste_des_time_in , liste_des_waiting_time]
    dico_wttime_transp["COCHU"] = big_DICO["dico_transp"]["COCHU"][day_num] # du type [liste_des_time_in , liste_des_waiting_time]
    cumul_time = big_DICO["dico_outnb_trucks"][day_num] # Un entier donnant le temps en minutes
    the_ylim = big_DICO["dico_ylim_ax1"][day_num]

    # On adapte la largeur de la courbe moyenne à celle du graphique
    stat_moyennes = [list(mean_stat[0]),list(mean_stat[1])] # On duplique pour ne pas changer l'original
    while len(stat_moyennes[0])>=2 and (stat_moyennes[0][-2]>les_time_in_out[-1]):
        stat_moyennes[0].pop() # On retire le dernier élément
        stat_moyennes[1].pop()

    # Affichage du graphique
    fig,ax1 = plt.subplots(figsize = (20,10)) ; plt.grid(True)
    plt.title("Graphique du {0} {1} {2}".format(day_num,list_months[int(month_num)-1],year_num))
    ax1.set_xlabel("Heure d'entree")
    ax1.set_ylabel("Temps passe au fond (en min)")
    ax2 = ax1.twinx() # Double graduation sur l'axe des y
    ax2.set_ylabel("Nombre de camions au fond")

    ax1.fill_between(les_time_in_out,les_nb_trucks, color='orange',zorder=1) # Colorier sous la courbe orange
    ax1.plot([les_time_in_out[0],les_time_in_out[-1]],[dico_param["barre_cible"],dico_param["barre_cible"]],linewidth=2, linestyle='-', color='red',zorder=2) # barre_cible
    ax1.plot(les_time_in, les_wttime, linewidth=2, linestyle='-', color='black', label="Temps passe au fond",zorder=2) # Ligne continue
    ax1.scatter([],[], marker='s', color='orange',label="Nombre de camions au fond",zorder=2) # Pour la légende
    ax1.scatter([],[],marker='x',color='white',label="{0} camions ou + au fond pendant {1}".format(dico_param["barre_camion"],print_a_time(cumul_time)),zorder=2) # Durée de dépassement de la barre ce jour

    if dico_wttime_transp["PICCONI"][1]!=[]: # Sinon bug dans mean_list(len(...))
        ax1.scatter(dico_wttime_transp["PICCONI"][0],dico_wttime_transp["PICCONI"][1],marker='s',color='red',label="PICCONI [{0} camions - {1}min]".format(len(dico_wttime_transp["PICCONI"][1]),mean_list(dico_wttime_transp["PICCONI"][1])),zorder=3) # Point pour chaque camion PICOLI
    if dico_wttime_transp["COCHU"][1]!=[]:
        ax1.scatter(dico_wttime_transp["COCHU"][0],dico_wttime_transp["COCHU"][1],marker='s',color='green',label="COCHU [{0} camions - {1}min]".format(len(dico_wttime_transp["COCHU"][1]),mean_list(dico_wttime_transp["COCHU"][1])),zorder=3) # Point pour chaque camion COCHU
    ax1.scatter([],[], marker='o', color='white',label="PICCONI+COCHU [{0} camions - {1}min]".format(len(les_time_in),mean_list(les_wttime))) # Pour la légende [nb_to_trucks,day_mean_time]
    # ax1.plot(stat_moyennes[0],stat_moyennes[1], linewidth=1, linestyle='--', color='black', label="Temps moyen passe au fond en " + list_months[int(month_num)-1],zorder=3) # Ligne ------ 

    # Réglage des graduations
    ax1.set_ylim(bottom=0,top=the_ylim)
    ax1.set_yticks( [10*k for k in range(0,(the_ylim//10)+1)] )
    ax1.set_xticks( [k for k in range(6,int(les_time_in_out[-1])+2)] )
    ax2.set_ylim(bottom=0,top=the_ylim//10)
    ax2.set_yticks( [k for k in range(0,(the_ylim//10)+1)] )
    ax1.legend(loc = 'upper left')


def Create_all_day_graph(dico_t_in,dico_wttime,dates_dispo,barre_cible,month_num,year_num):
    """ Créer et affiche la superposition de tous les graphiques du mois (seulement des courbes). """
    fig,ax = plt.subplots(figsize = (20,10)) ; les_lines = [] ; les_labels = []
    plt.grid(True)
    for (day_num,_,_) in dates_dispo:
        a_line = ax.plot(dico_t_in[day_num], dico_wttime[day_num], linewidth=2, linestyle='-', color=alea_col())
        str_day = str(day_num) + " " + list_months[month_num-1] + " " + str(year_num)
        les_lines.append(a_line) ; les_labels.append(str_day)
    ax.plot([6,17],[barre_cible,barre_cible],linewidth=4, linestyle='-', color='red', label="Barre cible des {0} minutes".format(barre_cible))
    plt.title( "Cumul des graphiques de {0}".format(list_months[month_num-1]) )
    plt.xlabel("Heure d'entree")
    plt.ylabel("Temps passe au fond (en min)")
    plt.xticks( [6,7,8,9,10,11,12,13,14,15,16,17] )
    fig.legend(les_lines , labels=les_labels , loc="center right" , title="Jours") 


def Create_waiting_trucks_graph(dico_stat_trucks,dico_outnb_trucks,dico_mean_month,dico_zone_trucks,dico_param,month_num,year_num,arrondir_stat):
    """ Créer et affiche le graphique du nombre de camions ayant attendu entre t et t+dt pour t dans [0,2h-dt].
        Un temps d'attente supérieur à deux heures est ramené à deux heures pas défaut. ----> dt = 5 est optimal !
        On doit FORCEMENT avoir 2h=120min%dt == 0 ! """

    # Calculs des listes pour l'affichage des barres
    dt_2 = dico_param["dt_2"] # 5 min usuellement
    dt_2f = float(dt_2)
    level_0 = { "PICCONI" : [[],[]] , "COCHU" : [[],[]] } # tps_att <= 30min
    level_1 = { "PICCONI" : [[],[]] , "COCHU" : [[],[]] } # 30min < tps_att <= 1h
    level_2 = { "PICCONI" : [[],[]] , "COCHU" : [[],[]] } # 1h < tps_att
    # PICCONI sera la demi-barre de gauche (+1.25) et COCHU sera la demi-barre de droite (+3.75)
    for code_transp in ["PICCONI","COCHU"]:
        for (tps_att,les_wttime) in dico_stat_trucks[code_transp].items():
            x = len(les_wttime)
            if tps_att<dico_param["temps_vert_max"]: # tps_att=30 correspond à [30,34] donc en prenant les <30, on prend les <=25 et donc ceux jusqu'à 29min
                level_0[code_transp][0].append(tps_att+(dt_2f/2)) ; level_0[code_transp][1].append(x)
            elif tps_att<dico_param["temps_orange_max"]: # 60 correspond à [60,65]
                level_1[code_transp][0].append(tps_att+(dt_2f/2)) ; level_1[code_transp][1].append(x)
            else: # temps_orange_max <= tps_att:
                level_2[code_transp][0].append(tps_att+(dt_2f/2)) ; level_2[code_transp][1].append(x)
    
    # Calcul des temps moyens et nb_to_trucks des transporteur sur le mois
    stat_trucks = [0,0,0] # [tps_att<30min , 30min<=tps_att<=1h , 1h<tps_att] -> Convention du tableur Excel
    for ind in [0,1,2]: # On somme les totaux de chq constructeur zone par zone
        stat_trucks[ind] = dico_zone_trucks["PICCONI"][ind] + dico_zone_trucks["COCHU"][ind]
    nb_trucks_tot = sum_list(stat_trucks)
    moy_wttime = moy_pond( [ [dico_mean_month["PICCONI"],sum_list(dico_zone_trucks["PICCONI"])] ,
                             [dico_mean_month["COCHU"],sum_list(dico_zone_trucks["COCHU"])] ] )
    rates = { "ALL":[] , "PICCONI":[] , "COCHU":[] }
    if arrondir_stat:
        rates["ALL"] = int_stat(stat_trucks) # La fonction fait tout le boulot de calcul et mise en forme des stats sur 'stat_trucks'
        rates["PICCONI"] = int_stat(dico_zone_trucks["PICCONI"])
        rates["COCHU"] = int_stat(dico_zone_trucks["COCHU"])
        moy_wttime = int(moy_wttime)
    else:
        rates["ALL"] = deux_dec_stat(stat_trucks)
        rates["PICCONI"] = deux_dec_stat(dico_zone_trucks["PICCONI"])
        rates["COCHU"] = deux_dec_stat(dico_zone_trucks["COCHU"])
        moy_wttime = float(int(100*moy_wttime))/100    
    
    # On va mettre PICCONI au dessus de COCHU en réhaussant les valeurs de PICCONI avec celles de COCHU
    for indice in range(0,len(level_0["PICCONI"][0])):
        level_0["PICCONI"][1][indice] += level_0["COCHU"][1][indice] # On réhausse chaque barre pour chaque temps d'attente dans la catégorie 'VERTE'
    for indice in range(0,len(level_1["PICCONI"][0])):
        level_1["PICCONI"][1][indice] += level_1["COCHU"][1][indice] # On réhausse chaque barre pour chaque temps d'attente dans la catégorie 'VERTE'
    for indice in range(0,len(level_2["PICCONI"][0])):
        level_2["PICCONI"][1][indice] += level_2["COCHU"][1][indice] # On réhausse chaque barre pour chaque temps d'attente dans la catégorie 'VERTE'
    max_axe_y = max(get_max(level_0["PICCONI"][1]),get_max(level_1["PICCONI"][1]),get_max(level_2["PICCONI"][1]))
       
    plt.figure(figsize = (20, 10)) ; plt.grid(True)
    plt.bar(level_0["PICCONI"][0],level_0["PICCONI"][1], width = dt_2, color = dico_COLORS["green_2"])
    plt.bar(level_1["PICCONI"][0],level_1["PICCONI"][1], width = dt_2, color = dico_COLORS["orange_2"])
    plt.bar(level_2["PICCONI"][0],level_2["PICCONI"][1], width = dt_2, color = dico_COLORS["red_2"])
    plt.bar(level_0["COCHU"][0],level_0["COCHU"][1], width = dt_2, color = dico_COLORS["green_1"])
    plt.bar(level_1["COCHU"][0],level_1["COCHU"][1], width = dt_2, color = dico_COLORS["orange_1"])
    plt.bar(level_2["COCHU"][0],level_2["COCHU"][1], width = dt_2, color =  dico_COLORS["red_1"])

    t1 = print_a_time(dico_param['temps_vert_max'],"min") ; t2 = print_a_time(dico_param['temps_orange_max'],"min")
    plt.scatter([],[],marker='s',color='black',label="PICCONI :")
    plt.scatter([],[],color=dico_COLORS["green_2"], label="| Inferieur a {0} : {1}%".format(t1,rates["PICCONI"][0]))
    plt.scatter([],[],color=dico_COLORS["orange_2"], label="| Entre {0} et {1} : {2}%".format(t1,t2,rates["PICCONI"][1]))
    plt.scatter([],[],color=dico_COLORS["red_2"], label="| Superieur a {0} : {1}%".format(t2,rates["PICCONI"][2]))
    plt.scatter([],[],color='white',label=" ") # "Saut de ligne"
    plt.scatter([],[],marker='s',color='black',label="COCHU :")
    plt.scatter([],[],color=dico_COLORS["green_1"], label="| Inferieur a {0} : {1}%".format(t1,rates["COCHU"][0]))
    plt.scatter([],[],color=dico_COLORS["orange_1"], label="| Entre {0} et {1} : {2}%".format(t1,t2,rates["COCHU"][1]))
    plt.scatter([],[],color=dico_COLORS["red_1"], label="| Superieur a {0} : {1}%".format(t2,rates["COCHU"][2]))
    plt.scatter([],[],color='white',label=" ") # "Saut de ligne"
    plt.scatter([],[],marker='s',color='black',label="PICCONI + COCHU :")
    plt.scatter([],[],color='white', label="| Inferieur a {0} : {1}%".format(t1,rates["ALL"][0]))
    plt.scatter([],[],color='white', label="| Entre {0} et {1} : {2}%".format(t1,t2,rates["ALL"][1]))
    plt.scatter([],[],color='white', label="| Superieur a {0} : {1}%".format(t2,rates["ALL"][2]))
    plt.scatter([],[],color='white',label=" ") # "Saut de ligne"
    plt.scatter([],[],marker='s',color='black',label = "PICCONI + COCHU : {0} camions - {1}min".format(nb_trucks_tot,moy_wttime)) # PICCONI+COCHU mean/count
    plt.scatter([],[],marker='s',color='white',label = "| PICCONI : {0} camions - {1}min".format(sum_list(dico_zone_trucks["PICCONI"]),dico_mean_month["PICCONI"])) # PICCONI mean/count
    plt.scatter([],[],marker='s',color='white',label = "| COCHU : {0} camions - {1}min".format(sum_list(dico_zone_trucks["COCHU"]),dico_mean_month["COCHU"])) # COCHU mean/count
    plt.scatter([],[],color='white',label=" ") # "Saut de ligne"
    plt.scatter([],[],marker='*',color='white',label = "+ de {0} camions au fond pendant {1} en {2}".format(dico_param["barre_camion"],print_a_time(sum_list(dico_outnb_trucks.values())),list_months[month_num-1])) # total time outnumber
    plt.scatter([],[],marker='*',color='white',label = "+ de {0} camions au fond en moyenne {1}/jour".format(dico_param["barre_camion"],print_a_time(mean_list(dico_outnb_trucks.values())))) # mean time outnumber
    
    plt.title("Statistiques du mois de {0} {1}".format(list_months[int(month_num)-1],year_num))
    plt.xlabel("Temps passe au fond")
    plt.ylabel("Nombre de camions")
    plt.xticks( [k*dt_2 for k in range(0,(120//dt_2)+1)] )
    plt.yticks( [20*k for k in range(0,(max_axe_y//20)+2)] )
    plt.legend()                      

    
def Create_mean_curve(time_in_mean,waiting_time_mean,barre_cible,month_num,year_num):
    max_wt_time_mean = 0
    for x in waiting_time_mean:
        max_wt_time_mean = max(x,max_wt_time_mean)
    max_wt_time_mean = 10*(max_wt_time_mean//10)
    
    plt.figure(figsize = (20, 10)) ; plt.grid(True)
    plt.plot(time_in_mean,waiting_time_mean,linewidth=2, linestyle='--', color='black', label="Temps moyen passe au fond en " + list_months[month_num-1])
    plt.plot([time_in_mean[0],time_in_mean[-1]],[barre_cible,barre_cible],linewidth=1, linestyle='-', color='red',label="Barre des {0} minutes".format(barre_cible)) # barre_cible
    plt.title("Graphique moyen de " + list_months[month_num-1])
    plt.xlabel("Heure d'entree")
    plt.ylabel("Temps passe au fond (en min)")
    plt.xticks( [6,7,8,9,10,11,12,13,14,15,16,17] )
    plt.yticks( [10*k for k in range(0,(max_wt_time_mean//10)+2)] )
    plt.legend()

