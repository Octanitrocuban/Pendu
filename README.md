# Pendu
Jeu du pendu avec une interface graphique utilisant pygame.


Le dossier data contient un fichier (list_words.txt) qui est une liste de mots français et un dossier compressé qui contient une version transformé du premier fichier. La version transformée est celle qui sera utilisée par le programme. Il est nécessaire de décomprésser le dossier et de mettre le fichier dans le dossier data.

Le dossier src contient quatre fichiers python : 
    - to_database.py: transforme le fichier list_words.txt en un fichier utilisable par le programe en .npy.
    - main.py : scripte à éxécuter pour jouer au pendu.
    - actions.py : scripte contenant les fontcions qui vont modifier les variables du jeu (réflexion de l'ia, clique du joueur ...).
    - graphical.py : scripte contenant les fonctions servant à afficher l'interface graphique.

Le fichier ./data/list_words.txt est une version modifier de la liste : https://www.pallier.org/extra/liste.de.mots.francais.frgut.txt, pour la passer en utf-8.

### L'IA pour trouver un mot du joueur humain

Cette ia fonctionne à l'aide de la base de données. Elle vas utiliser les informations obtenus pour réduire un pool de mot jusqu'à ce qu'il n'en reste plus qu'un. Le choix de la lettre proposée est basée sur la fréquence des lettres présentes dans les mots du pool.

Sur l'ensemble de la base des mots de la base de donnée (336 537 [15/02/2025]), 66 ont été trouvé du premier coup (sans avoir à proposer de lettre) et 2 396 n'ont pas été trouvé.
