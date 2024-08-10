# -*- coding: utf-8 -*-
"""
Script pour transformer le jeu de données listant tous les mots possibles
depuis le fichier .txt en un jeu de données utilisable par l'algorithme du
jeu du pendus.
"""

import numpy as np

# Extrait les mots contenus dans le fichier cible
file = open('../data/list_words.txt', 'r')
list_w = file.readlines()
file.close()

# Nombre total de mots
num_w = len(list_w)

# Base de données
database = {}
# Liste des caractères possible
database['caracteres'] = np.array(['-', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
								   'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
								   'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
								   'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e',
								   'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
								   'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
								   'v', 'w', 'x', 'y', 'z', 'à', 'â', 'ä',
								   'ç', 'è', 'é', 'ê', 'ë', 'î', 'ï', 'ô',
								   'ö', 'ù', 'û', 'ü'])

# Liste des mots
database['mots'] = []

# Longueur des mots
database['longueur'] = np.zeros(num_w, dtype='int8')

# Représentation en valeur numériques, le 100 est une surestimation large du
# nombre maximum de caractères (i.e. du mot le plus long)
database['map'] = np.zeros((num_w, 100), dtype='int8')

# Nombre de chaque caractères par mot
database['rec_map'] = np.zeros((num_w, len(database['caracteres'])), dtype='int8')

for i, mot in enumerate(list_w):
	mot_compo = np.array(list(mot), dtype=object)
	if mot_compo[-1] == '\n':
		mot_compo = mot_compo[:-1]

	# Longueur du mot
	database['longueur'][i] = len(mot_compo)

	# Le mot en lui même
	database['mots'].append(np.sum(mot_compo))

	# représentation du mot en valeurs numérique
	mask = mot_compo[:, np.newaxis] == database['caracteres']
	argwhere = np.argwhere(mask)
	database['map'][i, argwhere[:, 0]] = argwhere[:, 1]+1

	# nombre de chaque caractères par mot
	database['rec_map'][i] = np.sum(mask, axis=0).astype('int8')

# dtype=object est pour consommer moins de mémoire
database['mots'] = np.array(database['mots'], dtype=object)

# Pour enlever les colonnes innutilisées en fonction du mot le plus long
max_len = np.max(database['longueur'])
database['map'] = np.array(database['map'])[:, :max_len]

# Sauvegarde la base de donnée
np.save('../data/database.npy', np.array([database], dtype=object))
