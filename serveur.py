# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 08:10:19 2020

@author: Marin
"""
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote
import sqlite3
import json

# définition du handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):

  # sous-répertoire racine des documents statiques
  static_dir = ''

  # on surcharge la méthode qui traite les requêtes GET
  # deux possiblité de get: soit location ou description
  def do_GET(self): #"surchargé pour renvoyer les infos"
    self.init_params()

    # requete location - retourne la liste de lieux et leurs coordonnées géographiques
    if self.path_info[0] == "location":
      pays = self.db_get_countries()
      data = []#on ne va prendre ici que les infos utiles à la carte
      for p in pays:
          coord = {'wp' : p['wp'], 'lat' : p['latitude'], 'lon' : p['longitude'], 'name' : p['name']}#identifiant, latitude, longitude, nom 
          data.append(coord)
      self.send_json(data)

    # requete description - retourne la description du lieu dont on passe l'id en paramètre dans l'URL
    elif self.path_info[0] == "description":
      print("on fait une description")
      data = self.db_get_countries()# on récupère la base de donnée avec les requètes sous forme de dictionnaire
      for c in data:
        print ("on parcours la liste de données")# on parcourt la liste pour chercher le pays qu'on veut décrire 
        print(c['name'])
        if c['wp'] == (self.path_info[1]):# si on trouve le bon identifiant
            donnees = {}
            liste_cle = []
            for k in c.keys():# on parcourt les différentes clé du dictionnaire afin de récupérer ce qu'il y a dedans
                print(k)# wp name capital latitude longitude flag leader_name1 area_km2 population density_km2
                liste_cle.append(k)
                print (c[k])
                donnees[k] = c[k]# on ajoute à donnée les informations contenues dans les clés du dictionnaire 
            print(donnees)
            self.send_json(donnees)# on envoie les informations au format Json
            break

    # requête générique
    elif self.path_info[0] == "service":
      self.send_html('<p>Path info : <code>{}</p><p>Chaîne de requête : <code>{}</code></p>' \
          .format('/'.join(self.path_info),self.query_string));

    else:
      self.send_static()


  # méthode pour traiter les requêtes HEAD
  def do_HEAD(self):
      self.send_static()


  # méthode pour traiter les requêtes POST -
  def do_POST(self):
    self.init_params()

    # requête générique
    if self.path_info[0] == "service":
      self.send_html(('<p>Path info : <code>{}</code></p><p>Chaîne de requête : <code>{}</code></p>' \
          + '<p>Corps :</p><pre>{}</pre>').format('/'.join(self.path_info),self.query_string,self.body));

    else:
      self.send_error(405)


  # on envoie le document statique demandé
  def send_static(self):

    # on modifie le chemin d'accès en insérant le répertoire préfixe
    self.path = self.static_dir + self.path

    # on appelle la méthode parent (do_GET ou do_HEAD)
    # à partir du verbe HTTP (GET ou HEAD)
    if (self.command=='HEAD'):
        http.server.SimpleHTTPRequestHandler.do_HEAD(self)
    else:
        http.server.SimpleHTTPRequestHandler.do_GET(self)


  # on envoie un document html dynamique
  def send_html(self,content):
     headers = [('Content-Type','text/html;charset=utf-8')]
     html = '<!DOCTYPE html><title>{}</title><meta charset="utf-8">{}' \
         .format(self.path_info[0],content)
     self.send(html,headers)

  # on envoie un contenu encodé en json
  def send_json(self,data,headers=[]):
    body = bytes(json.dumps(data),'utf-8') # encodage en json et UTF-8
    self.send_response(200)
    self.send_header('Content-Type','application/json')
    self.send_header('Content-Length',int(len(body)))
    [self.send_header(*t) for t in headers]
    self.end_headers()
    self.wfile.write(body) 

  # on envoie la réponse
  def send(self,body,headers=[]):
     encoded = bytes(body, 'UTF-8')

     self.send_response(200)

     [self.send_header(*t) for t in headers]
     self.send_header('Content-Length',int(len(encoded)))
     self.end_headers()

     self.wfile.write(encoded)


  # on analyse la requête pour initialiser nos paramètres
  def init_params(self):
    # analyse de l'adresse
    info = urlparse(self.path)
    self.path_info = [unquote(v) for v in info.path.split('/')[1:]]
    self.query_string = info.query
    self.params = parse_qs(info.query)

    # récupération du corps
    length = self.headers.get('Content-Length')
    ctype = self.headers.get('Content-Type')
    if length:
      self.body = str(self.rfile.read(int(length)),'utf-8')
      if ctype == 'application/x-www-form-urlencoded' : 
        self.params = parse_qs(self.body)
    else:
      self.body = ''
   
    # traces
    print('info_path =',self.path_info)
    print('body =',length,ctype,self.body)
    print('params =', self.params)

  
  # Récupération de la liste des pays depuis la base de donnée sql
  def db_get_countries(self):
    c = conn.cursor()
    sql = 'SELECT wp, name, capital, latitude,longitude,flag,leader_name1,area_km2,population_density_km2 from countries'
    c.execute(sql)
    print("récupération des infos")
    return c.fetchall()

# connexion à la base de donnée 
conn = sqlite3.connect('pays.sqlite')

# Permet de renvoyer les requete sous forme de dictionnaire plutot que sous forme de liste 
conn.row_factory = sqlite3.Row

# instanciation et lancement du serveur
httpd = socketserver.TCPServer(("", 8080), RequestHandler)
httpd.serve_forever()
