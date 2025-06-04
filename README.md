# Pendu
Jeu du pendu avec une interface graphique utilisant pygame.


Le dossier data contient un fichier (list_words.txt) qui est une liste de mots français et un dossier compressé qui contient une version transformé du premier fichier. La version transformée est celle qui sera utilisée par le programme. Il est nécessaire de décomprésser le dossier et de mettre le fichier dans le dossier data.

Le dossier src contient quatre fichiers python : 
    - to_database.py: transforme le fichier list_words.txt en un fichier utilisable par le programe en .npy.
    - main.py : scripte à éxécuter pour jouer au pendu.
    - actions.py : scripte contenant les fontcions qui vont modifier les variables du jeu (réflexion de l'ia, clique du joueur ...).
    - graphical.py : scripte contenant les fonctions servant à afficher l'interface graphique.

Le fichier ./data/list_words.txt est une version modifier de la liste : https://www.pallier.org/extra/liste.de.mots.francais.frgut.txt, pour la passer en utf-8.

## Les méthodes des robots pour trouver le mot du joueur humain :

### frequentiel :
Ce robot utilise une attaque par fréquence qui est calculée de manière dynamique. Le robot utilise la liste de tous les mots possibles qu'il vas filtrer pour ne garder que ceux répondant aux critères fournis. Ce filtrage est d'abord réaliser lors de l'initialisation du mot avec la longueur de celui-ci et la présence et la position ou l'abscences de tirets. Le filtrage est ensuite appliqué après la réponse du joueur humain à chaque lettre proposées par le robot. Le choix de la lettre proposée est basée sur la fréquence des lettres présentes dans les mots du pool. Ce fonctionnement permet au robot de toujours proposer la lettre qui a le plus de chance d'être présente, ce qui limite le risque de perdre des points de vies. En conséquences, bien que certaines lettre permettrai de plus réduire le nombre de mot possible, le robot choisira celle qui minimise le risque de perte de vie.

Bien que ce comportement permet au robot de minimiser le risque de perdre, cela peut entraîner l'apparition d'une situation particulière où seul deux mots sont possibles. Le robot pourrait dans ce cas prédire plusieurs lettres sans que celles-ci ne lui permette de les différencier. Ainsi, quand le pool de mot n'en contient plus que deux, le robot prédira une lettre lui permettant de faire directement la différence entre eux.

Le comportement de ce robot fait que celui-ci répetera toujours la même suite de propositions tant que les conditions seront identiques.

Sur l'ensemble de la base des mots de la base de donnée (336 852 [04/06/2025]),   ont été trouvé du premier coup (sans avoir à proposer de lettre) et   n'ont pas été trouvé.

### probabiliste (à venir) :

### entropue (à venir) :


