# TD3-lieux-insolites.py

# Application exemple : affichage de mes lieux préférés à la Croix-Rousse 2018-10-24

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote
import sqlite3
import json

# définition du handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):

  # sous-répertoire racine des documents statiques
  static_dir = '/client_projet'

  # version du serveur
  server_version = 'TD3_mieux-insolites.py/0.1'

  # on surcharge la méthode qui traite les requêtes GET
  def do_GET(self): #"surchargé pour renvoyer les infos"
    self.init_params()

    # requete location - retourne la liste de lieux et leurs coordonnées géogrpahiques
    if self.path_info[0] == "location":
      pays = self.db_get_countries()
      data = []#on ne va prendre ici que les infos utiles à la carte
      for p in pays:
          coord = {'wp' : p['wp'], 'lat' : p['latitude'], 'lon' : p['longitude'], 'name' : p['name']}
          data.append(coord)
        # data=[{'id':1,'lat':10,'lon':4.82667,'name':"Nigeria"},
        #     {'id':2,'lat':45.77128,'lon':4.83251,'name':"Rue Caponi"},
        #     {'id':3,'lat':45.78061,'lon':4.83196,'name':"Jardin Rosa-Mir"}]
      self.send_json(data)

    # requete description - retourne la description du lieu dont on passe l'id en paramètre dans l'URL
    elif self.path_info[0] == "description":
      print("on fait une description")
      data = self.db_get_countries()
        # data=[{'id':1,'desc':"Je suis un africain", 'lat':10,'lon':10},
        #     {'id':2,'desc':"C'est le lieux 2", 'lat':20,'lon':20},
        #     {'id':3,'desc':"Lieu 3", 'lat':30,'lon':30}]
      for c in data:
        print ("on parcours la liste de données")
        print(c['name'])
        if c['wp'] == (self.path_info[1]):
            donnees = {}
            liste_cle = []
            for k in c.keys():
                print(k)
                liste_cle.append(k)
                print (c[k])
                donnees[k] = c[k]
            print(donnees)
            self.send_json(donnees)
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


  # méthode pour traiter les requêtes POST - non utilisée dans l'exemple
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

  
  # Récupération de la liste des pays depuis la base
  def db_get_countries(self):
    c = conn.cursor()
    sql = 'SELECT wp, name, capital, latitude, longitude from countries'
    c.execute(sql)
    print("récupération des infos")
    return c.fetchall()

  # def db_get_country(self,country):
  #   # préparation de la requête SQL
  #   c = conn.cursor()
  #   sql = 'SELECT * from countries WHERE wp=?'
  #   # récupération de l'information (ou pas)
  #   c.execute(sql,(country,))
  #   return c.fetchone()


conn = sqlite3.connect('pays_pmos.sqlite')

# Pour accéder au résultat des requêtes sous forme d'un dictionnaire
conn.row_factory = sqlite3.Row

# instanciation et lancement du serveur
httpd = socketserver.TCPServer(("", 8080), RequestHandler)
httpd.serve_forever()
