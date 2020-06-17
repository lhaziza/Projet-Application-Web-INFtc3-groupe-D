# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 08:27:56 2020

@author: porte
"""

import wptools


def get_info(country):
    page = wptools.page(country, silent=True)
    page.get_parse(False)
    return page.data['infobox']
#On utilise cette fonction pour récupérer le nom du pays dans la base de donnée

def get_name(wp_info):
    
    # cas général
    if 'conventional_long_name' in wp_info:
        name = wp_info['conventional_long_name']
        return name
    else:   
    # Aveu d'échec, on ne doit jamais se retrouver ici
        print('Could not fetch country name {}'.format(wp_info))
        return None
#On utilise cette fonction pour récupérer le nom conventionnel du pays qui va être utilisé comme information à afficher

def get_capital(wp_info):
    
    # cas général
    if 'capital' in wp_info:
        
        # parfois l'information récupérée comporte plusieurs lignes
        # on remplace les retours à la ligne par un espace
        capital = wp_info['capital'].replace('\n',' ')
        print(capital[17::],capital)
        if len(capital) >= 25:
            #Ici on traite les cas similaire à celui des Etats Unis
            result=''
            i=17
            while capital[i] != ']':
                result += capital[i]
                i += 1
            capital = str(result)
        else:
            #On retire les crochets
            capital = capital[2:len(capital)-2]

        return capital
    else :    
        # Aveu d'échec, on ne doit jamais se retrouver ici
        print(' Could not fetch country capital {}'.format(wp_info))
        return 'inconnu'
    
    
def get_more(wp_info):
    sortie = []
    # cas général
    if 'image_flag' in wp_info:
        
        # parfois l'information récupérée comporte plusieurs lignes
        # on remplace les retours à la ligne par un espace
        flag = wp_info['image_flag'].replace('\n',' ')

        sortie.append(flag)
    else :    
        # Aveu d'échec, on ne doit jamais se retrouver ici
        print(' Could not fetch country flag {}'.format(wp_info))
        sortie.append('inconnu')
    
    if 'leader_name1' in wp_info:
        
        # parfois l'information récupérée comporte plusieurs lignes
        # on remplace les retours à la ligne par un espace
        leader_name1 = wp_info['leader_name1'].replace('\n',' ')
        if leader_name1[10:21] == 'Donald Trump':
            sortie.append('Donald Trump')
        else:
            sortie.append(leader_name1)
            
    else :    
        # Aveu d'échec, on ne doit jamais se retrouver ici
        print(' Could not fetch country gov {}'.format(wp_info))
        sortie.append('inconnu')
        
    if 'area_km2' in wp_info:
        
        # parfois l'information récupérée comporte plusieurs lignes
        # on remplace les retours à la ligne par un espace
        area_km2 = wp_info['area_km2'].replace('\n',' ')

        sortie.append(area_km2)
    else : 
#On distingue le cas ou l'expression est donnée en km² ou en miles² pour que le resultat soit
#toujours en km². 
        if 'area_sq_mi' in wp_info:
            area_km2 = 1.6*int(wp_info['area_sq_mi'].replace(',',''))
            sortie.append(area_km2)
        else:
            # Aveu d'échec, on ne doit jamais se retrouver ici
            print(' Could not fetch country area_km2 {}'.format(wp_info))
            sortie.append('inconnu')
        
    if 'population_density_km2' in wp_info:
        
        # parfois l'information récupérée comporte plusieurs lignes
        # on remplace les retours à la ligne par un espace
        population = wp_info['population_density_km2'].replace('\n',' ')

        sortie.append(population)
    else : 
#On distingue le cas ou l'expression est donnée en km² ou en miles² pour que le resultat soit
#toujours en km². 
        if 'population_density_sq_mi' in wp_info:
            population = 1.6*int(wp_info['population_density_sq_mi'].replace(',',''))
            sortie.append(population)
        else :    
            # Aveu d'échec, on ne doit jamais se retrouver ici
            print(' Could not fetch country population {}'.format(wp_info))
            sortie.append('inconnu')
        
    
    print(sortie[0],sortie[1],sortie[2],sortie[3])
    return sortie[0],sortie[1],sortie[2],sortie[3]
#Dans ce code, on réalise la même procédure pour plusieurs informations obtenues afin de les renvoyer
#sous le bon format et de les réexploiter plus tard




def cv_coords(str_coords):
    # on découpe au niveau des "|" 
    c = str_coords.split('|')

    # on extrait la latitude en tenant compte des divers formats
    lat = float(c.pop(0))
    if (c[0] == 'N'):
        c.pop(0)
    elif ( c[0] == 'S' ):
        lat = -lat
        c.pop(0)
    elif ( len(c) > 1 and c[1] == 'N' ):
        lat += float(c.pop(0))/60
        c.pop(0)
    elif ( len(c) > 1 and c[1] == 'S' ):
        lat += float(c.pop(0))/60
        lat = -lat
        c.pop(0)
    elif ( len(c) > 2 and c[2] == 'N' ):
        lat += float(c.pop(0))/60
        lat += float(c.pop(0))/3600
        c.pop(0)
    elif ( len(c) > 2 and c[2] == 'S' ):
        lat += float(c.pop(0))/60
        lat += float(c.pop(0))/3600
        lat = -lat
        c.pop(0)

    # on fait de même avec la longitude
    lon = float(c.pop(0))
    if (c[0] == 'W'):
        lon = -lon
        c.pop(0)
    elif ( c[0] == 'E' ):
        c.pop(0)
    elif ( len(c) > 1 and c[1] == 'W' ):
        lon += float(c.pop(0))/60
        lon = -lon
        c.pop(0)
    elif ( len(c) > 1 and c[1] == 'E' ):
        lon += float(c.pop(0))/60
        c.pop(0)
    elif ( len(c) > 2 and c[2] == 'W' ):
        lon += float(c.pop(0))/60
        lon += float(c.pop(0))/3600
        lon = -lon
        c.pop(0)
    elif ( len(c) > 2 and c[2] == 'E' ):
        lon += float(c.pop(0))/60
        lon += float(c.pop(0))/3600
        c.pop(0)
    
    # on renvoie un dictionnaire avec les deux valeurs
    return {'lat':lat, 'lon':lon }

#
# Récupération des coordonnées de la capitale depuis l'infobox d'un pays
#
def get_coords(wp_info):

    # S'il existe des coordonnées dans l'infobox du pays
    # (cas le plus courant)
    if 'coordinates' in wp_info:

        # (?i) - ignorecase - matche en majuscules ou en minuscules
        # ça commence par "{{coord" et se poursuit avec zéro ou plusieurs
        #   espaces suivis par une barre "|"
        # après ce motif, on mémorise la chaîne la plus longue possible
        #   ne contenant pas de },
        # jusqu'à la première occurence de "}}"
        m = re.match('(?i).*{{coord\s*\|([^}]*)}}', wp_info['coordinates'])

        # l'expression régulière ne colle pas, on affiche la chaîne analysée pour nous aider
        # mais c'est un aveu d'échec, on ne doit jamais se retrouver ici
        if m == None :
            print(' Could not parse coordinates info {}'.format(wp_info['coordinates']))
            return None


        str_coords = m.group(1)

        # on convertit en numérique et on renvoie
        if str_coords[0:1] in '0123456789':
            print(cv_coords(str_coords))
            return cv_coords(str_coords)
    else:
        capital = wp_info['capital'].replace('\n',' ')
        r = 0
        for i in range(len(capital)-4):
            if r==0 and capital[i] == 'c' and capital[i+1] == 'o'and capital[i+2] == 'o' and capital[i+3] == 'r' and capital[i+4] == 'd':
                r=1
                rang=i
#Ici on a donc un code qui detecte la séquence 'coord' et qui permet de renvoyer les valeur lon et lat
#De cette manière on gère toutes les exceptions qui ont la même forme que les Etats Unis 
    

        latitude = int(capital[rang+6:rang+8])+int(capital[rang+9:rang+11])/60
        if capital[rang+12] == "S":
            latitude *= -1
        longitude = int(capital[rang+14:rang+16])+int(capital[rang+17:rang+19])/60
        if capital[rang+20] == "W":
            longitude *= -1
#On gère egalementl'orientation de la coordonnée (NSEW)
        return {'lat':latitude,'lon':longitude}
        
        
        
        
        


#
# import du module d'accès à la base de données
#
import sqlite3

#
# Ouverture d'une connexion avec la base de données
#
conn = sqlite3.connect('pays.sqlite')


#Code que l'on utilise dans SQLite :
"""
CREATE TABLE `countries` (              -- la table est nommé "countries"
	`wp`	TEXT NOT NULL UNIQUE,       -- nom de la page wikipédia, non nul, unique
	`name`	TEXT,                       -- nom complet du pays
	`capital`	TEXT,                   -- nom de la capitale
	`latitude`	REAL,                   -- latitude, champ numérique à valeur décimale
	`longitude`	REAL,                   -- longitude, champ numérique à valeur décimale
	`flag`	TEXT,                   -- longitude, champ numérique à valeur décimale
	`gov`	TEXT,                   -- longitude, champ numérique à valeur décimale
	`currency`	TEXT,                   -- longitude, champ numérique à valeur décimale
	`population`	REAL,               -- population, champ numérique à valeur décimale
	PRIMARY KEY(`wp`)                   -- wp est la clé primaire
);
"""

def save_country(conn,country,info):

    # préparation de la commande SQL
    c = conn.cursor()
    sql = 'INSERT OR REPLACE INTO countries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'

    # les infos à enregistrer
    name = get_name(info)
    capital = get_capital(info)
    coords = get_coords(info)
    flag,leader_name1,area_km2,population_density_km2 = get_more(info)
    #On récupère toutes les informations nécessaires grâce aux fonctions préalablement crées
    print(capital, coords['lat'],coords['lon'],flag,leader_name1,area_km2,population_density_km2)

    # soumission de la commande (noter que le second argument est un tuple)
    c.execute(sql,(country, name, capital, coords['lat'],coords['lon'],flag,leader_name1,area_km2,population_density_km2))
    conn.commit()
    print('done')








from zipfile import ZipFile
import json

with ZipFile('north_america.zip','r') as z:
    #On ouvre tous les fichiers .json du fichier fourni pour ne pas avoir à passer par wikipédia 
    
    print(z.namelist())
    print(len(z.namelist()))
    for pays in z.namelist():
        #On ouvre ensuite tous ces fichiers un par un pour utiliser la fonction save_country
        #
        

        info = json.loads(z.read(pays))
        print(pays[:-5:])
        save_country(conn,pays[:-5:],info)
        print('check')