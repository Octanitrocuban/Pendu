# Pendu
Jeu du pendu avec une interface graphique utilisant pygame.


Le dossier data contient un fichier (list_words.txt) qui est une liste de mots français et un dossier compressé qui contient une version transformé du premier fichier. La version transformée est celle qui sera utilisée par le programme. Il est nécessaire de décomprésser le dossier et de mettre le fichier dans le dossier data.

Le dossier src contient quatre fichiers python : 

    - to_database.py: transforme le fichier list_words.txt en un fichier utilisable par le programe en .npy.
    
    - main.py : scripte à éxécuter pour jouer au pendu.

    - actions.py : scripte contenant les fontcions qui vont modifier les variables du jeu (réflexion de l'ia, clique du joueur ...).

    - graphical.py : scripte contenant les fonctions servant à afficher l'interface graphique.

Le fichier ./data/list_words.txt est une version modifier de la liste : https://www.pallier.org/extra/liste.de.mots.francais.frgut.txt, pour la passer en utf-8.
