# Notice d'utilisation de l'application Web # 
__________________________________________________
## Installation ## 
L’installation de cette application se fait en plusieurs étapes.  
Dans un premier temps, il s’agit de récupérer l’intégralité du répertoire github. 
Dans un second temps, il faut lancer le serveur en exécutant le fichier serveur.py. Attention à bien l’exécuter dans une nouvelle console afin que le port utilisé (8080) soit bien libre. 
Une fois le serveur lancé, on peut ouvrir dans la fenêtre de navigateur l’application web correspondant au client (fichier HTML) nommé client_carte. Le lien suivant peut être utilisé : 

http://localhost:8080/client_carte.html

Il faudra toujours s’assurer que le fichier client est bien stocké avec : la feuille CSS style, les documents leaflet, le dossier flags (contenant les images de drapeau) et le dossier images (contenant les images de marqueurs). De plus, il faudra que le serveur (fichier serveur.py) et la base de données (pays.sqlite) restent dans le même dossier. 



__________________________________________________
## Utilisation ## 

Une fois l'application installée, une page web s'ouvre. On trouvera la notice d'installation en section 5 de la documentation technique.

En haut de la page web figure le titre de l'application, dans un bandeau blanc.
En cliquant dessus, l'utilisateur accède à la page wikipédia du continent traité ici, l'Amérique du Nord.

A gauche de l'écran figure une carte du monde, avec des repères géographiques.
Ces repères sont positionnés sur les capitales des pays d'Amérique du Nord.
Les petits boutons "+" / "-" en haut à gauche de la carte permettent à l'utilisateur de zoomer/ dézoomer sur la carte.
De plus, en positionnant sa souris sur la carte, l'utilisateur voit apparaître une petite main.
Elle permet, en cliquant et en maintenant appuyé de se déplacer sur la carte, en déplaçant la souris.

En cliquant sur un des repères, l'utilisateur peut visualiser à droite de la carte la description du pays sélectionné.
Il y retrouve le nom du pays, ainsi que sa capitale et ses coordonnées géographiques.
D'autres informations relatives au pays selectionné s'affichent : la densité de population, la surface et le nom du leader.
Enfin, en dessous de ces informations s'affiche le drapeau du pays.

En bas de la page, sont écrits les noms des personnes impliquées dans la création de l'application ainsi que l'année de création.

_________________________________________________
## Objectifs de l'application ##

Cette application vise à renseigner les informations principales des pays d'Amérique du Nord. 
C'est une interface ludique qui cherche à attiser la curiosité et développer la culture de son utilisateur.


