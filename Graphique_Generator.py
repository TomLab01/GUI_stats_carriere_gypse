# -*- coding: utf-8 -*-

try: #python3
    import tkinter as tk
    from tkinter import ttk
except ImportError: #python2
    import Tkinter as tk
    import ttk
from PIL import Image,ImageTk

from FILES.Code_central import *
from FILES.Code_outils import *

def center_window(w,dimensions):
    """ Centre la fenêtre 'w' au milieu de l'écran. ['dimensions' = "largeurxhauteur"] """
    [l,h] = dimensions.split("x")
    largeur = int(l) ; hauteur = int(h)
    L_ecran = w.winfo_screenwidth() ; H_ecran = w.winfo_screenheight()
    w.geometry( dimensions+"+"+str((L_ecran-largeur)//2)+"+"+str((H_ecran-hauteur)//2) )
    

### Definition de la FENETRE ACCEUIL Tkinter ###

class Window_1():
    """ Fenetre d'acceuil """
    def __init__(self): ### Se lance à la création de la fenêtre !
        self.root = tk.Tk()
        self.dim = "700x700" # "largeurxhauteur"
        center_window(self.root,self.dim) # self.root.geometry(self.dim)
        self.bg_color = 'light goldenrod'
        self.root.configure(bg=self.bg_color)
        self.font = ("arial",15)
        self.parametres = {} # Tous les champs sont vides au début
        self.dataframe = None
        self.valid_files = get_files_on_type([".xls",".xlsx"])
        self.root.title("Graphique Generator")
        self.infos_open = False
        self.go_on = False

        ## Icone + Titre + Images de décoration
        # icon = tk.PhotoImage(file=getcwd()+"/truck_icon.gif")
        # self.root.iconbitmap(icon)
        img1 = Image.open("FILES./img_deco_1.png") ; self.img1_tk = ImageTk.PhotoImage(img1) # self. pour pas que l'img disparaisse !
        img2 = Image.open("FILES./logo_etex_fond.png") ; self.img2_tk = ImageTk.PhotoImage(img2)
        title_zone = tk.Canvas(self.root, width = 650, height = max(img1.size[1],img2.size[1]), bg=self.bg_color, highlightthickness=0) 
        title_zone.create_image(20+img1.size[0]/2,img1.size[1]/2, image=self.img1_tk) # anchor = tk.NW
        title_zone.create_text(325,img1.size[1]/2,text="CHARGEMENT", font=('impact',40))
        title_zone.create_image(650-20-img2.size[0]/2,img2.size[1]/2, image=self.img2_tk) # anchor = tk.NW
        title_zone.grid(row=0,column=0,pady=20, columnspan=3) 
        
        ## Saisie du nom du fichier
        # 1 - label gauche
        tk.Label(self.root,text="Nom du fichier :",bg=self.bg_color, font=self.font).grid(row=1,column=0,sticky='se')
        # 2 - zone de saisie et de choix
        self.file_name = ttk.Combobox(self.root,values=self.valid_files,font=(self.font[0],self.font[1]-2))
        self.file_name.grid(row=1,column=1,sticky='s')
        # 3 - clear button
        tk.Button(self.root,text="Clear",command=self.clear_file_name, font=self.font).grid(row=1,column=2,sticky='s')

        ## Saisie du 'temps_mini'
        # 1 - label gauche
        tk.Label(self.root,text="Durée minimale crédible :",bg=self.bg_color, font=self.font).grid(row=3,column=0,sticky='e')
        # 2 - zone de saisie
        self.temps_mini = tk.StringVar()
        tk.Entry(self.root,textvariable=self.temps_mini, width=5, font=self.font).grid(row=3,column=1)

        ## Saisie du 'temps_ok'
        # 1 - label gauche
        tk.Label(self.root,text="Durée minimale acceptable :",bg=self.bg_color, font=self.font).grid(row=4,column=0,sticky='e')
        # 2 - zone de saisie
        self.temps_ok = tk.StringVar()
        tk.Entry(self.root,textvariable=self.temps_ok, width=5, font=self.font).grid(row=4,column=1)

        ## Saisie du 'temps_vert_max'
        # 1 - label gauche
        tk.Label(self.root,text="Durée limite optimale :",bg=self.bg_color, font=self.font).grid(row=5,column=0,sticky='e')
        # 2 - zone de saisie
        self.temps_vert_max = tk.StringVar()
        tk.Entry(self.root,textvariable=self.temps_vert_max, width=5, font=self.font).grid(row=5,column=1)

        ## Saisie du 'temps_orange_max'
        # 1 - label gauche
        tk.Label(self.root,text="Durée limite acceptable :",bg=self.bg_color, font=self.font).grid(row=6,column=0,sticky='e')
        # 2 - zone de saisie
        self.temps_orange_max = tk.StringVar()
        tk.Entry(self.root,textvariable=self.temps_orange_max, width=5, font=self.font).grid(row=6,column=1)

        ## Bouton INFO
        tk.Button(self.root,text="Détails",bg='dark orange',font=self.font, command=self.show_infos).grid(row=6,column=2)

        ## Saisie de 'barre_cible'
        # 1 - label gauche
        tk.Label(self.root,text="Durée standard :",bg=self.bg_color, font=self.font).grid(row=7,column=0,sticky='e')
        # 2 - zone de saisie
        self.barre_cible = tk.StringVar()
        tk.Entry(self.root,textvariable=self.barre_cible, width=5, font=self.font).grid(row=7,column=1)

        ## Saisie de 'barre_camion'
        # 1 - label gauche
        tk.Label(self.root,text="Barre camions simultanés :",bg=self.bg_color, font=self.font).grid(row=8,column=0,sticky='e')
        # 2 - zone de saisie
        self.barre_camion = tk.StringVar()
        tk.Entry(self.root,textvariable=self.barre_camion, width=5, font=self.font).grid(row=8,column=1)

        ## Saisie du 'dt_1'
        # 1 - label gauche
        tk.Label(self.root,text="Pas de discrétisation 1 :",bg=self.bg_color, font=self.font).grid(row=9,column=0,sticky='e')
        # 2 - zone de saisie
        self.dt_1 = tk.StringVar()
        tk.Entry(self.root,textvariable=self.dt_1, width=5, font=self.font).grid(row=9,column=1)

        ## Saisie du 'dt_2'
        # 1 - label gauche
        tk.Label(self.root,text="Pas de discrétisation 2 :",bg=self.bg_color, font=self.font).grid(row=10,column=0,sticky='e')
        # 2 - zone de saisie
        self.dt_2 = tk.StringVar()
        tk.Entry(self.root,textvariable=self.dt_2, width=5, font=self.font).grid(row=10,column=1)

        # Bouton : Enregistrement des nvx param par défaut
        tk.Button(self.root,text="Save parameters",bg='indian red',command=self.save_param, font=self.font).grid(row=11,column=0,pady=15)

        # Bouton : Chargement des param par défaut
        tk.Button(self.root,text="Load parameters",bg='salmon',command=self.load_param, font=self.font).grid(row=11,column=1)
        # load_button.grid(row=11,column=1)

        # Bouton : Validation
        tk.Button(self.root,text="Valider",bg='gold',command=self.valid, font=self.font).grid(row=11,column=2)

        # Canva pour le chargement
        self.cnv = tk.Canvas(self.root, width=240, height=80, bg='gainsboro',highlightthickness=4,highlightbackground ='black')
        self.cnv.create_text(120,22,text="",font=('arial',12)) # Le texte est centré autour du point (120,20)
        self.cnv.grid(row=12,column=0,columnspan=3)

        # Liste qui référence toutes les StringVar controlant les paramètres 
        self.list_param_name = ["temps_mini","temps_ok","temps_vert_max","temps_orange_max","dt_1","dt_2","barre_camion","barre_cible"]
        self.list_param_StrVar = [self.temps_mini,self.temps_ok,self.temps_vert_max,self.temps_orange_max,self.dt_1,self.dt_2,self.barre_camion,self.barre_cible]
        # --> Important d'avoir les listes dans le même ordre !!!

        # On charge directement les paramètres par défaut
        self.load_param()
        
        # On ajuste la grille à la fenêtre
        self.expand_grid(2,13) # <-- Paramètres à changer ici
        
        self.root.mainloop()

    def expand_grid(self,nb_col,nb_row):
        # On étend les colonnes
        for k in range(0,nb_col+1):
            self.root.columnconfigure(k, weight=1)
        # On étend les lignes
        for k in range(0,nb_row+1):
            self.root.rowconfigure(k, weight=1)
    
    def load_param(self):
        """ Charge dans les StringVar les paramètres du fichier 'parametres.txt'. """
        d = get_parameters()
        self.temps_mini.set(str(d["temps_mini"]))
        self.temps_ok.set(str(20))
        self.temps_vert_max.set(str(d["temps_vert_max"]))
        self.temps_orange_max.set(str(d["temps_orange_max"]))
        self.dt_1.set(str(d["dt_1"]))
        self.dt_2.set(str(d["dt_2"]))
        self.barre_camion.set(str(d["barre_camion"]))
        self.barre_cible.set(str(d["barre_cible"]))

    def save_param(self):
        """ Enregistre les paramètres des StringVar dans le fichier 'parametres.txt'. """
        valid_param = True
        for a_StrVar in self.list_param_StrVar:
            if not(is_int(a_StrVar.get())):
                valid_param = False
        if valid_param:
            dprov = {}
            for ind in range(0,len(self.list_param_name)):
                dprov[self.list_param_name[ind]] = self.list_param_StrVar[ind].get()
            with open('FILES./parametres.txt','wb') as file_param:
                outil = pickle.Pickler(file_param)
                outil.dump(dprov)

    def clear_file_name(self):
        self.file_name.set("")
        self.cnv.itemconfigure(1, text="")
        self.cnv.create_rectangle(20,40,220,70,outline='gainsboro',fill='gainsboro')
        

    def show_infos(self):
        """ Ouvre une fenêtre d'information sur la définition de certaines variables. """
        if not(self.infos_open): # Pour n'ouvrir qu'une seule fenêtre
            window_infos = tk.Toplevel()
            # window_infos.resizable(False,False)
            txt_list = []
            txt_list.append("[1] = Durée minimale crédible : un camion passant strictement moins de [1]min au fond est considéré comme une erreur et est supprimé des données.")
            txt_list.append("[2] = Durée minimale acceptable : un camion passant plus de [1]min mais strictement moins de [2]min au fond est considéré comme un fraudeur.")
            txt_list.append("[3] = Durée limite optimale : un camion passant plus de [2]min mais strictement moins de [3]min au fond sera représenté dans une barre verte.")
            txt_list.append("[4] = Durée limite acceptable : un camion passant plus de [3]min mais strictement moins de [4]min au fond sera représenté dans une barre orange.")
            txt_list.append("[5] = Durée standard : temps qu'un camion est supposé passer au fond.")
            txt_list.append("[6] = Barre camions simultanés : permet de compter le temps passé avec plus de [6] camions au fond en simultané sur une journée et sur le mois.")
            txt_list.append("[7] = Pas de discrétisation 1 : pas de discrétisation de l'heure de la journée (en min) pour le calcul du temps moyen passé au fond sur le mois")
            txt_list.append("[8] = Pas de discrétisation 2 : pas de discrétisation du temps passé au fond par un camion pour le diagramme en barres.")
            tk.Label(window_infos,text="Détails des paramètres",font=("arial",22)).grid(row=0,column=0)
            for k in range(0,len(txt_list)):
                tk.Label(window_infos,text=txt_list[k],font=("arial",12)).grid(row=k+2,column=0,padx=10,pady=10,sticky='w')
            # On repère qu'une fenêtre est déjà ouverte et on repasse en 'False' seulement lorsqu'elle est refermée
            self.infos_open = True
            def close_infos():
                self.infos_open = False ; window_infos.destroy()
            window_infos.protocol("WM_DELETE_WINDOW", close_infos)

    def valid(self):
        """ On vérifie toutes les entrées pour savoir si on peut valider. """
        validation = True
        if not(self.file_name.get() in self.valid_files): # Check 'file_name'
            validation = False ; self.file_name.set("")
        for a_StrVar in self.list_param_StrVar: # Check parameters
            if not(is_int(a_StrVar.get())):
                validation = False ; a_StrVar.set("")
        if validation: # On vérifie les relations entre les paramètres
            if int(self.temps_vert_max.get())%int(self.dt_2.get())!=0:
                validation = False ; self.temps_vert_max.set("")
            if int(self.temps_orange_max.get())%int(self.dt_2.get())!=0:
                validation = False ; self.temps_orange_max.set("")
            
        if validation: # On tente de charger et on quitte si tout est bien valide
            try:
                ## On récupère et on normalise les informations
                dataframe = get_dataframe(self.file_name.get()) ; print(1)
                dataframe["Date"] = dataframe["Date"].apply(dateday_to_int)  ; print(2) # On applique la fonction à tous les elts de la colonne "Date"
                dataframe["Date du poids d'entree"] = dataframe["Date du poids d'entree"].apply(date_inout_to_int) ; print(3)
                dataframe["Date du poids de sortie"] = dataframe["Date du poids de sortie"].apply(date_inout_to_int) ; print(4)
                dataframe["Code transporteur"] = dataframe["Code transporteur"].apply(PICONI_to_PICCONI) # Erreur PICONI->PICCONI
                self.dataframe = dataframe
                for ind in range(0,len(self.list_param_name)): # On charge les paramètres dans le dictionnaire
                    self.parametres[self.list_param_name[ind]] = int(self.list_param_StrVar[ind].get())
                self.cnv.itemconfigure(1, text="CHARGEMENT : 0%")
                self.cnv.delete("loading_grey_rect")
                self.cnv.create_rectangle(20,40,220,70, fill='whitesmoke', tag="loading_grey_rect")
                self.root.update()
                self.go_on = True
                self.root.quit()
            
            except: # ERREUR de chargement des données -> sûrement dans la forme des données
                self.cnv.itemconfigure(1, text="ECHEC DU CHARGEMENT")
                self.cnv.delete("loading_grey_rect")
                self.cnv.create_rectangle(20,40,220,70, fill="red", tag="loading_grey_rect")
                self.root.update()


### Definition FENETRE MENU Tkinter ###

class Window_2():
    """ Fenetre Menu """
    def __init__(self,big_DICO,mean_stat,dico_param,dates_dispo,les_anomalies,lignes_df_suppr): ### Se lance à la création de la fenêtre !
        self.root = tk.Tk()
        self.dim = "750x600" # "largeurxhauteur"
        center_window(self.root,self.dim)
        self.bg_color = 'light goldenrod'
        self.root.configure(bg=self.bg_color)
        self.font = ("arial",15)
        self.anomalies_open = False ; self.del_lines = False
        self.root.title("Graphique Generator")
        self.valid_days = [str(d) + " " + str(list_months[m-1]) for (d,m,y) in dates_dispo]

        # Définition des ttes les données en attribut pour pouvoir les utiliser dans les méthodes de la classe 'Window_2'
        self.big_DICO = big_DICO
        self.mean_stat = mean_stat
        self.dico_param = dico_param
        self.dates_dispo = dates_dispo
        self.les_anomalies = les_anomalies
        self.lignes_df_suppr = lignes_df_suppr
        self.month_num = dates_dispo[0][1] ; self.year_num = dates_dispo[0][2]
        
        ## Titre label
        tk.Label(self.root,text="GraphiqueGenerator",bg=self.bg_color, font=('impact',36)).grid(row=0,column=0,columnspan=3,pady=16)

        ## Graphique d'une seule journée
        # 1 - label gauche
        tk.Label(self.root,text="Graphique d'une journée :",bg=self.bg_color, font=self.font).grid(row=1,column=0,sticky='e')
        # 2 - zone de saisie et de choix
        self.day_choice = tk.StringVar() ; self.day_choice.set(self.valid_days[0])
        self.day_choice_menu = tk.OptionMenu(self.root,self.day_choice,*self.valid_days)
        self.day_choice_menu.config(width=10,font=self.font,bg='gold',highlightthickness=0,activebackground='gold')
        self.day_choice_menu.grid(row=1,column=1)
        # 3 - view button
        tk.Button(self.root,text="Voir",bg="white",command=self.show_single_day_graph, font=self.font).grid(row=1,column=2)
        
        ## Bouton : Graphe camions
        tk.Label(self.root,text="Statistiques durées de "+list_months[self.month_num-1]+" :",bg=self.bg_color,font=self.font).grid(row=2,column=0,columnspan=2)
        tk.Button(self.root,text="Voir",bg='white',command=self.show_trucks_graph, font=self.font).grid(row=2,column=1,columnspan=2)
        self.arr_stat_1 = False
        self.checkbutton_1 = tk.IntVar()
        tk.Checkbutton(self.root,text="Arrondir %",variable=self.checkbutton_1,bg=self.bg_color, font=(self.font[0],self.font[1]-2)).grid(row=2,column=2)

        ## Bouton : Graphe de tous les jours
        tk.Label(self.root,text="Courbes journalières cumulées :",bg=self.bg_color,font=self.font).grid(row=3,column=0,columnspan=2)
        tk.Button(self.root,text="Voir",bg='white',command=self.show_all_day_graph, font=self.font).grid(row=3,column=1,columnspan=2)

        ## Bouton : Graphe moyen du mois
        tk.Label(self.root,text="Courbe moyenne du mois :",bg=self.bg_color,font=self.font).grid(row=4,column=0,columnspan=2)
        tk.Button(self.root,text="Voir",bg='white',command=self.show_mean_graph, font=self.font).grid(row=4,column=1,columnspan=2)

        ## Bouton : Liste des anomalies
        tk.Label(self.root,text="Camions en anomalie :",bg=self.bg_color,font=self.font).grid(row=5,column=0,columnspan=2)
        tk.Button(self.root,text="Voir",bg='white',command=self.show_anomalies, font=self.font).grid(row=5,column=1,columnspan=2)

        ## Bouton : Exporter les données
        tk.Button(self.root,text="Exporter les données",bg='orange',command=self.export, font=self.font).grid(row=7,column=0,columnspan=3,sticky='s')
        self.txt_export = tk.StringVar() # ; self.txt_export.set("")
        tk.Label(self.root,textvariable=self.txt_export,bg=self.bg_color,fg='black',font=(self.font[0],self.font[1]-2)).grid(row=8,column=0,columnspan=3,sticky='n')

        ## Bouton : Enregistrement de tous les graphes
        tk.Button(self.root,text="Enregistrer tous les graphiques",bg='orange',command=self.save_all_graph, font=self.font).grid(row=9,column=0,columnspan=3,sticky='s')
        self.arr_stat_2 = False
        self.checkbutton_2 = tk.IntVar()
        tk.Checkbutton(self.root,text="Arrondir %",variable=self.checkbutton_2,bg=self.bg_color, font=(self.font[0],self.font[1]-2)).grid(row=10,column=0,columnspan=3,sticky='n')

        # Canva pour le chargement
        self.cnv = tk.Canvas(self.root, width=400, height=80, bg='gainsboro',highlightthickness=4,highlightbackground='black')
        self.cnv.create_text(200,22,text="",font=('arial',12)) # Le texte est centré autour du point (200,20)
        self.cnv.grid(row=11,column=0,columnspan=3,pady=15)

        if self.lignes_df_suppr != []: # Bouton pour voir les lignes supprimées
            tk.Button(self.root,text="Infos",bg='salmon',font=self.font,command=self.show_lignes_suppr).grid(row=11,column=2,sticky='e',padx=20)

        # On ajuste la grille à la fenêtre
        self.expand_grid(2,12) # <-- Paramètres à changer ici

        self.root.mainloop()

    def expand_grid(self,nb_col,nb_row):
        # On étend les colonnes
        for k in range(0,nb_col+1):
            self.root.columnconfigure(k, weight=1)
        # On étend les lignes
        for k in range(0,nb_row+1):
            self.root.rowconfigure(k, weight=1)
    
    def show_single_day_graph(self):
        Create_single_day_graph(self.big_DICO,self.dico_param,self.mean_stat,int(self.day_choice.get().split(" ")[0]),self.month_num,self.year_num)
        plt.show()

    def show_trucks_graph(self):
        """ Affiche les statistiques camion du mois. """
        arrondir_stat = True
        Create_waiting_trucks_graph(self.big_DICO["dico_stat_trucks"] ,
                                    self.big_DICO["dico_outnb_trucks"] ,
                                    self.big_DICO["dico_mean_month"] ,
                                    self.big_DICO["dico_zone_trucks"] ,
                                    self.dico_param, self.month_num, self.year_num, self.checkbutton_1.get())
        plt.show()

    def show_all_day_graph(self):
        """ Affiche le graphique des toutes les courbes du mois. """
        arrondir_stat = True
        Create_all_day_graph(self.big_DICO["dico_t_in"], self.big_DICO["dico_wttime"] ,
                             self.dates_dispo, self.dico_param["barre_cible"], self.month_num, self.year_num)
        plt.show()

    def show_mean_graph(self):
        """ Affiche le graphique de la courbe moyenne du mois. """
        arrondir_stat = True
        Create_mean_curve(self.mean_stat[0], self.mean_stat[1], self.dico_param["barre_cible"], self.month_num, self.year_num)
        plt.show()

    def export(self):
        """ Exporte toutes les données calculées (moyennes/comptages) dans un fichier excel. """
        Export_datas(self.big_DICO,self.dico_param,self.dates_dispo,self.les_anomalies,self.month_num,self.year_num)
        self.txt_export.set("Exportation réussie !")
        self.root.update()
        sleep(1.5)
        self.txt_export.set("")
    
    def save_all_graph(self):
        """ Enregistre tous les graphiques du mois. """
        if not(already_exists("Camions gypse " + list_months[self.month_num-1])):
            self.cnv.itemconfigure(1, text="Enregistrement en cours : 0%")
            self.cnv.delete("loading_grey_rect")
            self.cnv.create_rectangle(100,40,300,70, fill='whitesmoke', tag="loading_grey_rect") # rectangle de dim 200*30
            self.root.update()
            plt.switch_backend('Agg') # Pour ne pas que tkinter se ferme juste après
            Enregister_graphiques(self.big_DICO, self.mean_stat, self.dates_dispo,self.dico_param ,
                                  self.month_num, self.year_num, self.checkbutton_2.get(), self)
            plt.switch_backend('TkAgg') # Pour pouvoir voir les graphiques avoir 'Voir'
            self.cnv.itemconfigure(1, text="Enregistrement terminé !")
            self.cnv.delete("loading_green_rect")
            self.cnv.create_rectangle(100,40,300,70, fill="green", tag="loading_green_rect")
            self.root.update()
        else:
            self.cnv.itemconfigure(1, text="Dossier 'Camions gypse {0}' déjà existant".format(list_months[self.month_num-1]))
            self.root.update()
            

    def show_anomalies(self):
        """ Ouvre une fenêtre d'information sur la définition de certaines variables. """
        if not(self.anomalies_open) and not(self.les_anomalies==[]): # Pour n'ouvrir qu'une seule fenêtre
            window_anomalies = tk.Toplevel()
            window_anomalies.configure(bg='salmon')
            the_month = list_months[self.month_num-1]
            tk.Label(window_anomalies,text="Camions en anomalie en "+the_month,bg='salmon',font=("arial",24)).grid(row=0,column=0,pady=10)
            ind = 2
            for [plaque_cam,(d,m,y),time_in,time_out,code_transp] in self.les_anomalies:
                txt_to_print = "{0} : {1} - le {3} {4} {5} à {6} - {2}min.".format(code_transp,plaque_cam,time_out-time_in,d,the_month,y,print_a_time(time_in,""))
                tk.Label(window_anomalies,text=txt_to_print,bg='salmon',font=self.font).grid(row=ind,column=0,sticky='w',padx=10)
                ind += 1
            # On repère qu'une fenêtre est déjà ouverte et on repasse en 'False' seulement lorsqu'elle est refermée
            self.anomalies_open = True
            def close_anomalies():
                self.anomalies_open = False ; window_anomalies.destroy()
            window_anomalies.protocol("WM_DELETE_WINDOW", close_anomalies)

    def show_lignes_suppr(self):
        """ Affiche dans une autre fenêtre les lignes supprimées au cours de l'analyse. """
        # Fenetre_del_lines = Window_3(self.lignes_df_suppr)
        if not(self.del_lines): # Pour n'ouvrir qu'une seule fenêtre
            w_lignes_suppr = tk.Toplevel()
            bg_color = 'salmon' ; w_lignes_suppr.configure(bg=bg_color)
            tk.Label(w_lignes_suppr,text="Données supprimées lors de l'analyse",bg=bg_color,font=("arial",24)).grid(row=0,column=0,pady=10)
            ind = 1
            for (num_ligne,error_type) in self.lignes_df_suppr:
                txt_to_print = "Ligne {0} : {1}".format(num_ligne+2,error_type)
                tk.Label(w_lignes_suppr,text=txt_to_print,bg=bg_color,font=('arial',16)).grid(row=ind,column=0,sticky='w',padx=10)
                ind += 1
            # On repère qu'une fenêtre est déjà ouverte et on repasse en 'False' seulement lorsqu'elle est refermée
            self.del_lines = True
            def close_window():
                self.del_lines = False ; w_lignes_suppr.destroy()
            w_lignes_suppr.protocol("WM_DELETE_WINDOW", close_window)


### Definition de la FENETRE D AFFICHAGE DES SUPPRESSIONS Tkinter ###        

class Window_3():
    """ Fenetre affichant les lignes supprimées. """
    def __init__(self,les_lignes):
        self.root = tk.Tk()
        self.bg_color = 'salmon'
        self.root.configure(bg=self.bg_color)
        
        tk.Label(self.root,text="Données supprimées lors de l'analyse",bg=self.bg_color,font=("arial",24)).grid(row=0,column=0,pady=10)
        ind = 1
        for (num_ligne,error_type) in les_lignes:
            txt_to_print = "Ligne {0} : {1}".format(num_ligne+2,error_type)
            tk.Label(self.root,text=txt_to_print,bg=self.bg_color,font=('arial',16)).grid(row=ind,column=0,sticky='w',padx=10)
            ind += 1

        def close_window():
            self.root.destroy()
        tk.Button(self.root,text="Continuer",bg='gold',font=('arial',16),command=close_window).grid(row=ind,column=0,pady=10)
        self.root.protocol("WM_DELETE_WINDOW", close_window)
        self.root.update_idletasks() # Pour pouvoir après obtenir les dimensions de la fenêtre
        center_window(self.root,str(self.root.winfo_width())+"x"+str(self.root.winfo_height()))
        self.root.mainloop()


### ========== PROGRAMME PRINCIPAL ========== ###

def Graph_Generator(default_name = "GYPSE 06.xlsx"):
    """ Les données récupérées de la dataframe sont de la forme suivante :
        [25255, Timestamp('2020-06-02 00:00:00'), u'02/06/2020 06:25', u'02/06/2020 06:57', u'PICONI']
        -> "Date" est un 'Timestamp' qu'il suffit de transormer en chaine de caractère
        -> "Date du poids d'entree" et "Date du poids de sortie" sont déjà des chaines de caractère
        -> "Code transporteur" est une chaine de caractères.
        On transforme les "Date" en des triplets d'int (d,m,y) et "Date du poids d'entree/sortie" en un int donnant l'heure en minutes. """

    Fenetre_Accueil = Window_1()
    if Fenetre_Accueil.go_on:

        dataframe = Fenetre_Accueil.dataframe # Récupération de la dataframe
        dico_param = Fenetre_Accueil.parametres # Récupération des paramètres
                
        ## 1 - Formation de 'dates_dispo', 'month_num' et 'year_num'
        dates_dispo_brut = list(dataframe["Date"].unique()) ; dates_dispo_x = []
        month_num = most_present_value(dates_dispo_brut,1) # Attention au décalage avec list_months qui compte Janvier comme le mois 0 !!!
        year_num = most_present_value(dates_dispo_brut,2)
        dates_dispo = []
        for (d,m,y) in dates_dispo_brut:
            if (m==month_num) and (y==year_num):
                dates_dispo.append( (d,m,y) )
        del(dates_dispo_brut)
        # dates_dispo contient tous les jours présents dans le fichier (et sans répétition) et appartenant à month_num et year_num !
        
        ## 2 - On liste les données qui ne correspondent pas !
        lignes_df_suppr = []
        for (num_ligne,contenu_ligne) in dataframe.iterrows():
            m = contenu_ligne["Date"][1]
            if m != month_num:
                lignes_df_suppr.append((num_ligne,"Erreur de mois")) # On stocke pour l'instant
            elif y != year_num:
                lignes_df_suppr.append((num_ligne,"Erreur d'annee"))
            elif ((contenu_ligne["Date du poids de sortie"]-contenu_ligne["Date du poids d'entree"])<dico_param["temps_mini"]): # Anomalie lorsque <=10min au fond !
                lignes_df_suppr.append((num_ligne,"Erreur de temps passe au fond"))
        if lignes_df_suppr!=[] : # Il y a bien des lignes à supprimer ! La suppression n'est pas faîte sur place pour ne pas toucher aux indices !
            lignes_df_suppr = reverse_list(lignes_df_suppr)
            for (num_ligne,error_type) in lignes_df_suppr:
                dataframe.drop(dataframe.index[[num_ligne]], inplace=True)
        
        ## 3 - On récupère toutes les données
        big_DICO , mean_stat = Calculate_data_lists(dataframe,dates_dispo,month_num,year_num,dico_param,Fenetre_Accueil)

        ## 4 - On récupère les anomalies dans une liste d'éléments de la forme : [plaque_cam,(d,m,y),time_in,time_out,code_transp]
        les_anomalies = []
        for (_,contenu_ligne) in dataframe.iterrows():
            [plaque_cam,(d,m,y),time_in,time_out,code_transp] = list(contenu_ligne)
            if time_out-time_in < dico_param["temps_ok"]:
                les_anomalies.append([plaque_cam,(d,m,y),time_in,time_out,code_transp])        
        
        ## 5 - Lancement du MENU
        Fenetre_Accueil.root.destroy() # On ferme la fenêtre Tkinter
        if lignes_df_suppr != []: # On affiche les lignes supprimées
            Window_3(lignes_df_suppr)
        Window_2(big_DICO,mean_stat,dico_param,dates_dispo,les_anomalies,lignes_df_suppr)
        print("FIN")


### ========== LANCEMENT ! ========== ###
if __name__ == "__main__":
    Graph_Generator()



