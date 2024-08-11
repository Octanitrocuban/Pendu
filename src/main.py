"""
Interface graphique et logique pour le jeu du pendu.
"""

import numpy as np
import pygame

pygame.init()

FPS = 60
WIDTH, HEIGHT = 800, 700
BG_COLOUR = (int(0.96*255), int(0.96*255), int(0.86*255))
BUTTON_COLOR = (180, 180, 180)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

TEXT_FONT = pygame.font.SysFont('Arial', 30)
RESULT_FONT = pygame.font.SysFont('Arial', 40, bold=True)
TITLE_FONT = pygame.font.SysFont('Arial', 50)

# Flèche pour revenir en arrière (positions)
ARROW = np.array([[0, 0], [0.75, 0.5], [0.75, 0.25], [1.5, 0.25],
				  [1.5, -0.25], [0.75, -0.25], [0.75, -0.5]])

ARROW = ARROW*np.array([70, 50])+np.array([50, 40])

# Tête de la flèche pour une optimization de calcul
HEAD = ARROW[[0, 1, 6]]

# Approximation de pi
PI2 = round(np.pi*2, 6)

# Croix (positions des coins)
CROSS = np.array([[-0.75,  0.25], [-0.25,  0.25], [-0.25,  0.75],
				  [ 0.25,  0.75], [ 0.25,  0.25], [ 0.75,  0.25],
				  [ 0.75, -0.25], [ 0.25, -0.25], [ 0.25, -0.75],
				  [-0.25, -0.75], [-0.25, -0.25], [-0.75, -0.25]])

# Croix servant à augmenter la limite supperieur du nombre de caractère ou le
# nombre de caractère
CROSS_UP = CROSS*20 + np.array([WIDTH/4+25-25, 200])
# Croix servant à augmenter la limite inferieur du nombre de caractère
CROSS_DW = CROSS*20 + np.array([WIDTH/4+25-25, 325])

# Base de données
DATA = np.load('../data/database.npy', allow_pickle=True)[0]

# Lettre "minimales" pour les propositions
LETTERS = np.array(list('azertyuiopqsdfghjklmwxcvbn'))
# Position des lettres du pseudo clavier
POSITIONS = np.array([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0],
					  [7, 0], [8, 0], [9, 0], [10, 0], [11, 0], [12, 0],
					  [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1],
					  [7, 1], [8, 1], [9, 1], [10, 1], [11, 1], [12, 1]])

POSITIONS = POSITIONS*60+np.array([WIDTH/2-385, 450])

pygame.display.set_caption('Pendu')

class Game:
	a_like = ['à', 'â', 'ä']
	c_like = ['ç']
	e_like = ['è', 'é', 'ê', 'ë']
	i_like = ['î', 'ï']
	o_like = ['ô', 'ö']
	u_like = ['ù', 'û', 'ü']
	# Quelles caractères sont reliés à chaque lettre "minimale"
	link_dico = {
		'a':['A', 'a', 'à', 'â', 'ä'], 'b':['B', 'b'], 'c':['C', 'c', 'ç'],
		'd':['D', 'd'], 'e':['E', 'e', 'è', 'é', 'ê', 'ë'], 'f':['F', 'f'],
		'g':['G', 'g'], 'h':['H', 'h'], 'i':['I', 'i', 'î', 'ï'],
		'j':['J', 'j'], 'k':['K', 'k'], 'l':['L', 'l'], 'm':['M', 'm'],
		'n':['N', 'n'], 'o':['O', 'o', 'ô', 'ö'], 'p':['P', 'p'],
		'q':['Q', 'q'], 'r':['R', 'r'], 's':['S', 's'], 't':['T', 't'],
		'u':['U', 'u', 'ù', 'û', 'ü'], 'v':['V', 'v'], 'w':['W', 'w'],
		'x':['X', 'x'], 'y':['Y', 'y'], 'z':['Z', 'z']}

	def __init__(self):
		# accueil / general
		self.initialized = False
		self.guess = False
		self.make_guess = False
		self.mouse_on_guess = False
		self.mouse_on_m_guess = False
		self.length = 5
		self.tirets = None
		self.mouse_on_return = False
		self.mouse_on_cr_up = False
		self.mouse_on_mi_up = False
		self.mouse_pos = (None, None)

		# guess init
		self.result_g = None
		self.start_g = False
		self.mouse_on_cr_dw = False
		self.mouse_on_mi_dw = False
		self.length_limits = [1, 25]
		self.m_on_start_g = False
		self.show_must_choice_tiret = False
		self.m_on_tiret_t = False
		self.m_on_tiret_f = False

		# make guess init
		self.result_mg = None
		self.m_on_tiret_mg = False
		self.num_tirets = 0
		self.start_m = False
		self.can_start_m = False
		self.m_on_start_m = False
		self.cells_dx = None
		self.profil = np.zeros(5, dtype='int8')
		self.show_no_word = False

		# guess play part
		self.choiced = None
		self.recenter = 0
		self.choice_letter = None
		self.tested_letters = []
		self.representation = None
		self.clavier = np.zeros(26, dtype='int8')
		self.health = 7
		self.show_alredy_tryed = False
		self.m_on_letters = np.zeros(26, dtype=bool)

		# make guess play part
		self.mots = None
		self.mapp = None
		self.rec_mapp = None
		self.propose = None
		self.is_letter = None
		self.m_on_oui_mkg = False
		self.m_on_non_mkg = False
		self.m_on_conf_mkg = False
		self.show_is_there = False
		self.possibles = None
		self.center_propos = None
		self.m_on_propose = None
		self.selected = None
		self.etat = None
		self.must_do_some = False
		self.no_possible = False
		self.one_possible = False

	def get_mouse_pos(self):
		"""
		Fonction pour enregistrer à chaque frame la position de la souris.
		"""
		self.mouse_pos = pygame.mouse.get_pos()

	def draw_word(self):
		"""
		Fonction pour tirer aléatoirement un mot répondant aux
		caractéristiques données par l'utilisateur.
		"""
		mots = np.copy(DATA['mots'])
		tire = np.copy(DATA['rec_map'][:, 0])
		mask = (DATA['longueur'] >= self.length_limits[0])&(
				DATA['longueur'] <= self.length_limits[1])

		mots = mots[mask]
		tire = tire[mask]
		if self.tirets == False:
			mots = mots[tire == 0]
	
		self.choiced = mots[np.random.randint(0, len(mots))]

	def is_possible_start_mg(self):
		"""
		Fonction pour voir si il y a au moins un mots répondant aux
		caractéristiques données par l'utilisateur.
		"""
		mapp = np.copy(DATA['map'])[:, :self.length]
		rec_mapp = np.copy(DATA['rec_map'])
		caracteres = np.copy(DATA['caracteres'])
		mask = DATA['longueur'] == self.length
		mapp = mapp[mask]
		rec_mapp = rec_mapp[mask]
		if self.num_tirets > 0:
			mask = rec_mapp[:, 0] == self.num_tirets
			mapp = mapp[mask]
			rec_mapp = rec_mapp[mask]
			known = len(self.profil[self.profil != 0])
			perf = mapp == self.profil
			occur = np.sum(perf, axis=1)
			mask = occur == known
			mapp = mapp[mask]
			rec_mapp = rec_mapp[mask]

		else:
			mask = rec_mapp[:, 0] == 0
			mapp = mapp[mask]
			rec_mapp = rec_mapp[mask]

		self.mapp = np.copy(mapp)
		self.rec_mapp = np.copy(rec_mapp)
		self.can_start_m = len(rec_mapp) > 0

	def whats_best(self):
		"""
		Fonction pour chercher le meilleur caractère à utiliser pour trouver
		le mot choisit par l'humain. L'approche est baser sur la fréquence d'
		apparition de chaque lettre "minimale".
		"""
		sub_map = np.copy(self.mapp)
		if len(sub_map) == 0:
			self.no_possible = True # No possible word from the data
			self.health = 0
			self.result_mg = 'p'

		elif len(sub_map) == 1:
			self.one_possible = True
			mot = np.sum(DATA['caracteres'][sub_map[0]-1].astype(object))
			self.propose = mot

		elif sub_map.shape[0] > 2:
			m_equal = DATA['caracteres'] == np.array(list(self.choiced))[:, np.newaxis]
			vals_in = np.argwhere(m_equal)[:, 1]+1
			if len(vals_in) == 0:
				# => il n'y a aucun caractère connus
				sub_map[(sub_map >= 54)&(sub_map <= 56)] = 28
				sub_map[sub_map == 57] = 30
				sub_map[(sub_map >= 58)&(sub_map <= 61)] = 32
				sub_map[(sub_map >= 62)&(sub_map <= 63)] = 36
				sub_map[(sub_map >= 64)&(sub_map <= 65)] = 42
				sub_map[(sub_map >= 66)&(sub_map <= 68)] = 48
				sub_map[(sub_map < 27)&(sub_map != 1)] += 26
				values, counts = (np.unique(sub_map, return_counts=True))
				maxi = values[counts == np.max(counts)]
				maxi = maxi[0]-1
				self.propose = DATA['caracteres'][maxi]
				self.get_linked_letters()

			else:
				sub_map = sub_map[:, self.representation == False]
				sub_map[(sub_map >= 54)&(sub_map <= 56)] = 28
				sub_map[sub_map == 57] = 30
				sub_map[(sub_map >= 58)&(sub_map <= 61)] = 32
				sub_map[(sub_map >= 62)&(sub_map <= 63)] = 36
				sub_map[(sub_map >= 64)&(sub_map <= 65)] = 42
				sub_map[(sub_map >= 66)&(sub_map <= 68)] = 48
				sub_map[(sub_map < 27)&(sub_map != 1)] += 26
				values, counts = (np.unique(sub_map, return_counts=True))
				maxi = values[counts == np.max(counts)]
				maxi = maxi[0]-1
				self.propose = DATA['caracteres'][maxi]
				self.get_linked_letters()

		elif sub_map.shape[0] == 2:
			differ = (sub_map[0] != sub_map[1])&(self.representation == False)
			sub_map = sub_map[:, differ]
			sub_map[(sub_map >= 54)&(sub_map <= 56)] = 28
			sub_map[sub_map == 57] = 30
			sub_map[(sub_map >= 58)&(sub_map <= 61)] = 32
			sub_map[(sub_map >= 62)&(sub_map <= 63)] = 36
			sub_map[(sub_map >= 64)&(sub_map <= 65)] = 42
			sub_map[(sub_map >= 66)&(sub_map <= 68)] = 48
			sub_map[(sub_map < 27)&(sub_map != 1)] += 26
			values, counts = (np.unique(sub_map, return_counts=True))
			maxi = values[counts == np.max(counts)]
			maxi = maxi[0]-1
			self.propose = DATA['caracteres'][maxi]
			self.get_linked_letters()

	def update_from_answer(self):
		"""
		Fonction pour enlever les mots ne répondant pas aux caractéristiques
		connues.
		"""
		sub_map = np.copy(self.mapp)
		if self.is_letter:
			for i in range(len(self.choiced)):
				if self.choiced[i] != '_':
					numb = np.where(DATA['caracteres'] == self.choiced[i])[0][0]+1
					sub_map = sub_map[sub_map[:, i] == numb]

				else:
					for j in range(len(self.possibles)):
						numb = np.where(DATA['caracteres'] == self.possibles[j])[0][0]+1
						sub_map = sub_map[sub_map[:, i] != numb]

		else:
			for i in range(len(self.possibles)):
				numb = np.where(DATA['caracteres'] == self.possibles[i])[0][0]+1
				sub_map = sub_map[np.sum(sub_map == numb, axis=1) == 0]

		self.mapp = np.copy(sub_map)

	def get_linked_letters(self):
		"""
		Fonction pour extraire les caractères associées à la lettre "minimale"
		choisit par la fonction 'whats_best'
		"""
		self.possibles = np.array(self.link_dico[self.propose])
		num_p = len(self.possibles)
		self.center_propos = WIDTH/2 + (np.arange(num_p)-num_p/2)*60
		self.m_on_propose = np.zeros(num_p, dtype=bool)
		self.selected = np.zeros(num_p, dtype=bool)

	def guess_victory(self):
		"""
		Fonction pour détecter si l'humain a réussis (gagné) ou non (perdu) à
		trouver le mot choisit par l'ordinateur.
		"""
		if self.health <= 0:
			self.result_g = 'p'
		else:
			if np.sum(self.representation) == self.length:
				self.result_g = 'v'

	def re_init_accueil(self):
		"""
		Fonction pour ré-initialiser le jeu jusqu'à la fenêtre d'accueil.
		"""
		# accueil / general
		self.initialized = False
		self.guess = False
		self.make_guess = False
		self.mouse_on_guess = False
		self.mouse_on_m_guess = False
		self.length = 5
		self.tirets = None
		self.mouse_on_return = False
		self.mouse_on_cr_up = False
		self.mouse_on_mi_up = False

		# guess init
		self.result_g = None
		self.start_g = False
		self.mouse_on_cr_dw = False
		self.mouse_on_mi_dw = False
		self.length_limits = [1, 25]
		self.m_on_start_g = False
		self.show_must_choice_tiret = False
		self.m_on_tiret_t = False
		self.m_on_tiret_f = False

		# make guess init
		self.result_mg = None
		self.m_on_tiret_mg = False
		self.num_tirets = 0
		self.start_m = False
		self.can_start_m = False
		self.m_on_start_m = False
		self.cells_dx = None
		self.profil = np.zeros(5, dtype='int8')
		self.show_no_word = False

		# guess play part
		self.choiced = None
		self.recenter = 0
		self.choice_letter = None
		self.tested_letters = []
		self.representation = None
		self.clavier = np.zeros(26, dtype='int8')
		self.health = 7
		self.show_alredy_tryed = False
		self.m_on_letters = np.zeros(26, dtype=bool)

		# make guess play part
		self.mots = None
		self.mapp = None
		self.rec_mapp = None
		self.propose = None
		self.is_letter = None
		self.m_on_oui_mkg = False
		self.m_on_non_mkg = False
		self.m_on_conf_mkg = False
		self.show_is_there = False
		self.possibles = None
		self.center_propos = None
		self.m_on_propose = None
		self.selected = None
		self.etat = None
		self.must_do_some = False
		self.no_possible = False
		self.one_possible = False

	def re_init_guess(self):
		"""
		Fonction pour ré-initialiser le jeu jusqu'à la fenêtre du choix des
		caractéristiques possible pour deviner un mot choisit par
		l'ordinateur.
		"""
		self.initialized = True
		self.guess = True
		self.make_guess = False
		self.length = 5
		self.length_limits = [1, 27]
		self.tirets = None
		self.show_must_choice_tiret = False
		self.choiced = None
		self.recenter = 0
		self.choice_letter = None
		self.tested_letters = []
		self.representation = None
		self.clavier = np.zeros(26, dtype='int8')
		self.health = 7
		self.start_g = False
		self.show_alredy_tryed = False

	def re_init_make_guess(self):
		"""
		Fonction pour ré-initialiser le jeu jusqu'à la fenêtre du choix des
		caractéristiques du mot choisit par	l'humain.
		"""
		self.health = 7
		self.initialized = True
		self.guess = False
		self.make_guess = True
		self.length = 5
		self.result_mg = None
		self.m_on_tiret_mg = False
		self.num_tirets = 0
		self.start_m = False
		self.can_start_m = False
		self.m_on_start_m = False
		self.cells_dx = None
		self.tested_letters = []
		self.representation = np.zeros(self.length, dtype=bool)
		self.choiced = '_'*self.length
		self.recenter = WIDTH/2-30*self.length/2
		self.profil = np.zeros(5, dtype='int8')
		self.show_no_word = False
		self.mapp = None
		self.rec_mapp = None
		self.propose = None
		self.is_letter = None
		self.m_on_oui_mkg = False
		self.m_on_non_mkg = False
		self.m_on_conf_mkg = False
		self.show_is_there = False
		self.possibles = None
		self.center_propos = None
		self.m_on_propose = None
		self.selected = None
		self.etat = np.zeros(self.length) -1
		self.must_do_some = False
		self.no_possible = False
		self.one_possible = False

	def mouse_mode_on(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		d'un des deux bouttons du choix du type de jeu.
		"""
		if (self.mouse_pos[0] >= 129.4)&(self.mouse_pos[1] >= 282.95)&(
			self.mouse_pos[0] <= 669.6)&(self.mouse_pos[1] <= 317.05):
			self.mouse_on_guess = True
		else:
			self.mouse_on_guess = False

		if (self.mouse_pos[0] >= 155.8)&(self.mouse_pos[1] >= 383.5)&(
			self.mouse_pos[0] <= 644.2)&(self.mouse_pos[1] <= 416.5):
			self.mouse_on_m_guess = True
		else:
			self.mouse_on_m_guess = False

	def mouse_return_on(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		de la flêche permettant de revenir au menu précédant.
		"""
		mouse_p_arr = np.array(self.mouse_pos)
		vect = mouse_p_arr-HEAD
		norm = np.sum(vect**2, 1)**0.5
		prod = np.sum(vect[[0, 0, 1]]*vect[[1, 2, 2]], 1)
		theta = round(np.sum(np.arccos(
						prod/(norm[[0, 0, 1]]*norm[[1, 2, 2]]))), 6)

		if (self.mouse_pos[0] >= ARROW[2, 0])&(
				self.mouse_pos[1] >= ARROW[4, 1])&(
					self.mouse_pos[0] <= ARROW[4, 0])&(
						self.mouse_pos[1] <= ARROW[2, 1]):

			self.mouse_on_return = True

		elif theta == PI2:
			self.mouse_on_return = True
		else:
			self.mouse_on_return = False

	def mouse_on_pm_up(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		des boutons servant à faire varier la valeur de la borne minimal du
		nombre de caractères d'un mot.
		"""
		if (self.mouse_pos[0] >= WIDTH/4-25)&(self.mouse_pos[1] >= 175)&(
			self.mouse_pos[0] <= WIDTH/4+25)&(self.mouse_pos[1] <= 225):
			self.mouse_on_cr_up = True
		else:
			self.mouse_on_cr_up = False

		if (self.mouse_pos[0] >= WIDTH*3/4-25)&(self.mouse_pos[1] >= 175)&(
			self.mouse_pos[0] <= WIDTH*3/4+25)&(self.mouse_pos[1] <= 225):
			self.mouse_on_mi_up = True
		else:
			self.mouse_on_mi_up = False

	def mouse_on_pm_down(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		des boutons servant à faire varier la valeur de la borne maximal du
		nombre de caractères d'un mot.
		"""
		if (self.mouse_pos[0] >= WIDTH/4-25)&(self.mouse_pos[1] >= 300)&(
			self.mouse_pos[0] <= WIDTH/4+25)&(self.mouse_pos[1] <= 350):
			self.mouse_on_cr_dw = True
		else:
			self.mouse_on_cr_dw = False

		if (self.mouse_pos[0] >= WIDTH*3/4-25)&(self.mouse_pos[1] >= 300)&(
			self.mouse_pos[0] <= WIDTH*3/4+25)&(self.mouse_pos[1] <= 350):
			self.mouse_on_mi_dw = True
		else:
			self.mouse_on_mi_dw = False

	def mouse_on_tirets_guess(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		boutons pour la sélection de la présence ou non de tiret(s) dans le
		mot que devra deviner l'humain.
		"""
		if (self.mouse_pos[0] >= WIDTH/4-50)&(self.mouse_pos[1] >= 425)&(
			self.mouse_pos[0] <= WIDTH/4+50)&(self.mouse_pos[1] <= 475):
			self.m_on_tiret_t = True
		else:
			self.m_on_tiret_t = False

		if (self.mouse_pos[0] >= WIDTH*3/4-50)&(self.mouse_pos[1] >= 425)&(
			self.mouse_pos[0] <= WIDTH*3/4+50)&(self.mouse_pos[1] <= 475):
			self.m_on_tiret_f = True
		else:
			self.m_on_tiret_f = False

	def mouse_on_tirets_mg(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		des caractères pouvant être transformé de lettre à tiret ou
		inversement.
		"""
		if (self.mouse_pos[1] >= 365)&(self.mouse_pos[1] <= 410):
			self.cells_dx = np.arange(self.length)*30+self.recenter
			mx = (self.mouse_pos[0] >= self.cells_dx)&(
				  self.mouse_pos[0] <= self.cells_dx+25)

			self.m_on_tiret_mg = mx
		else:
			self.m_on_tiret_mg = np.zeros(self.length, dtype=bool)

	def mouse_on_start_guess(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		du bouton pour lancer une partie où l'humain doit trouver un mot.
		"""
		if (self.mouse_pos[0] >= WIDTH/2-100)&(self.mouse_pos[1] >= 500)&(
			self.mouse_pos[0] <= WIDTH/2+100)&(self.mouse_pos[1] <= 550):
			self.m_on_start_g = True
		else:
			self.m_on_start_g = False

	def mouse_on_letters(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		d'une des lettres du clavier.
		"""
		mx = (self.mouse_pos[0] >= POSITIONS[:, 0])&(
			  self.mouse_pos[0] <= POSITIONS[:, 0]+50)

		my = (self.mouse_pos[1] >= POSITIONS[:, 1])&(
			  self.mouse_pos[1] <= POSITIONS[:, 1]+50)

		self.m_on_letters = mx&my

	def mouse_on_start_mg(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		du bouton pour lancer une partie où l'ordinateur doit trouver le mot
		choisit par l'humain.
		"""
		if (self.mouse_pos[0] >= WIDTH/2-100)&(self.mouse_pos[1] >= 450)&(
			self.mouse_pos[0] <= WIDTH/2+100)&(self.mouse_pos[1] <= 500):
			self.m_on_start_m = True
		else:
			self.m_on_start_m = False

	def mouse_on_repsonse(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		des boutons oui/non/confirmer lors-ce-que c'est à l'ordinateur de
		trouver le mot choisit par l'humain.
		"""
		if (self.mouse_pos[0] >= 50)&(self.mouse_pos[1] >= 150)&(
			self.mouse_pos[0] <= 150)&(self.mouse_pos[1] <= 200):
			self.m_on_oui_mkg = True
		else:
			self.m_on_oui_mkg = False
		
		if (self.mouse_pos[0] >= 200)&(self.mouse_pos[1] >= 150)&(
			self.mouse_pos[0] <= 300)&(self.mouse_pos[1] <= 200):
			self.m_on_non_mkg = True
		else:
			self.m_on_non_mkg = False

		if (self.mouse_pos[0] >= 100)&(self.mouse_pos[1] >= 225)&(
			self.mouse_pos[0] <= 250)&(self.mouse_pos[1] <= 275):
			self.m_on_conf_mkg = True
		else:
			self.m_on_conf_mkg = False

	def mouse_on_propose(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		d'un des caractères associé à une lettre "minimale".
		"""
		if type(self.is_letter) == bool:
			if self.is_letter:
				if (self.mouse_pos[1] >= 400)&(self.mouse_pos[1] <= 450):
					self.m_on_propose = (self.mouse_pos[0] >= self.center_propos)&(
										 self.mouse_pos[0] <= self.center_propos+50)
				else:
					self.m_on_propose[:] = False

	def mouse_on_letters_mg(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		des caractères pouvant être transformé de lettre à tiret ou
		inversement.
		"""
		if (self.mouse_pos[1] >= 315)&(self.mouse_pos[1] <= 355):
			self.cells_dx = np.arange(self.length)*30+self.recenter
			mx = (self.mouse_pos[0] >= self.cells_dx)&(
				  self.mouse_pos[0] <= self.cells_dx+25)

			self.m_on_tiret_mg = mx
		else:
			self.m_on_tiret_mg = np.zeros(self.length, dtype=bool)

	def choice_mode(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		d'un des deux bouttons du choix du type de jeu lors du clique.
		"""
		if (self.mouse_pos[0] >= 129.4)&(self.mouse_pos[1] >= 282.95)&(
			self.mouse_pos[0] <= 669.6)&(self.mouse_pos[1] <= 317.05):
			self.guess = True
			self.make_guess = False
			self.initialized = True
			pygame.time.wait(400)

		if (self.mouse_pos[0] >= 155.8)&(self.mouse_pos[1] >= 383.5)&(
			self.mouse_pos[0] <= 644.2)&(self.mouse_pos[1] <= 416.5):
			self.choiced = '_'*self.length
			self.representation = np.zeros(self.length, dtype=bool)
			self.etat = np.zeros(self.length) -1
			self.recenter = WIDTH/2-30*self.length/2
			self.make_guess = True
			self.guess = False
			self.initialized = True
			pygame.time.wait(400)

	def update_init_guess(self):
		"""
		Fonction pour détecter quelles intéractions sont faîtes sur les
		caractéristiques du mot qui sera deviné par l'humain.
		"""
		if (self.mouse_pos[0] >= WIDTH/4-25)&(self.mouse_pos[1] >= 175)&(
			self.mouse_pos[0] <= WIDTH/4+25)&(self.mouse_pos[1] <= 225):
			if self.length_limits[0] < self.length_limits[1]:
				self.length_limits[0] += 1

		elif (self.mouse_pos[0] >= WIDTH*3/4-25)&(self.mouse_pos[1] >= 175)&(
			  self.mouse_pos[0] <= WIDTH*3/4+25)&(self.mouse_pos[1] <= 225):
			if self.length_limits[0] > 1:
				self.length_limits[0] -= 1

		elif (self.mouse_pos[0] >= WIDTH/4-25)&(self.mouse_pos[1] >= 300)&(
			  self.mouse_pos[0] <= WIDTH/4+25)&(self.mouse_pos[1] <= 350):
			if self.length_limits[1] < 25:
				self.length_limits[1] += 1

		elif (self.mouse_pos[0] >= WIDTH*3/4-25)&(self.mouse_pos[1] >= 300)&(
			  self.mouse_pos[0] <= WIDTH*3/4+25)&(self.mouse_pos[1] <= 350):
			if self.length_limits[0] < self.length_limits[1]:
				self.length_limits[1] -= 1

		elif (self.mouse_pos[0] >= WIDTH/4-50)&(self.mouse_pos[1] >= 425)&(
			  self.mouse_pos[0] <= WIDTH/4+50)&(self.mouse_pos[1] <= 475):
			self.tirets = True
			self.show_must_choice_tiret = False

		elif (self.mouse_pos[0] >= WIDTH*3/4-50)&(self.mouse_pos[1] >= 425)&(
			  self.mouse_pos[0] <= WIDTH*3/4+50)&(self.mouse_pos[1] <= 475):
			self.tirets = False
			self.show_must_choice_tiret = False

		elif (self.mouse_pos[0] >= WIDTH/2-100)&(self.mouse_pos[1] >= 500)&(
			self.mouse_pos[0] <= WIDTH/2+100)&(self.mouse_pos[1] <= 550):
			if type(self.tirets) == bool:
				self.start_g = True
				self.draw_word()
				self.length = len(self.choiced)
				self.representation = np.zeros(self.length, dtype=bool)
				self.recenter = WIDTH/2-30*self.length/2
			else:
				self.show_must_choice_tiret = True

	def update_init_make_guess(self):
		"""
		Fonction d'intéraction de l'humain pour choisir les caractéristiques
		mot qu'il fera deviner à l'ordinateur.	
		"""
		if (self.mouse_pos[0] >= WIDTH/4-25)&(self.mouse_pos[1] >= 175)&(
			self.mouse_pos[0] <= WIDTH/4+25)&(self.mouse_pos[1] <= 225):
			if self.length < 25:
				self.length += 1
				self.choiced += '_'
				self.representation = np.append(self.representation, False)
				self.etat = np.append(self.etat, -1)
				self.profil = np.append(self.profil, 0)
				self.recenter = WIDTH/2-30*self.length/2
				self.show_no_word = False

		elif (self.mouse_pos[0] >= WIDTH*3/4-25)&(self.mouse_pos[1] >= 175)&(
			  self.mouse_pos[0] <= WIDTH*3/4+25)&(self.mouse_pos[1] <= 225):
			if self.length > 1:
				self.length -= 1
				self.choiced = self.choiced[:-1]
				self.representation = self.representation[:-1]
				self.etat = self.etat[:-1]
				self.profil = self.profil[:-1]
				self.recenter = WIDTH/2-30*self.length/2
				self.show_no_word = False

		elif True in self.m_on_tiret_mg:
			#transform : true de _ en - & self.transformation et inversement
			if self.representation[self.m_on_tiret_mg][0]:
				self.representation[self.m_on_tiret_mg] = False
				self.profil[self.m_on_tiret_mg] = 0
				self.choiced = np.array(list(self.choiced), dtype='O')
				self.choiced[self.m_on_tiret_mg] = '_'
				self.etat[self.m_on_tiret_mg] = -1
				self.choiced = np.sum(self.choiced)
				self.num_tirets -= 1
				self.show_no_word = False

			else:
				self.representation[self.m_on_tiret_mg] = True
				self.profil[self.m_on_tiret_mg] = 1
				self.choiced = np.array(list(self.choiced), dtype='O')
				self.choiced[self.m_on_tiret_mg] = '-'
				self.etat[self.m_on_tiret_mg] = 1
				self.choiced = np.sum(self.choiced)
				self.num_tirets += 1
				self.show_no_word = False

		if (self.mouse_pos[0] >= WIDTH/2-100)&(self.mouse_pos[1] >= 450)&(
			self.mouse_pos[0] <= WIDTH/2+100)&(self.mouse_pos[1] <= 500):
			if self.num_tirets == 0:
				self.start_m = True
				self.show_no_word = False
				self.is_possible_start_mg()
			else:
				self.is_possible_start_mg()
				if self.can_start_m:
					self.start_m = True
					self.show_no_word = False
				else:
					self.show_no_word = True

	def choice_letter_guess(self):
		"""
		Fonction d'interaction de l'humain pour choisir quelle lettre
		"minimale" choisir.
		"""
		if (np.sum(self.m_on_letters) > 0)&(self.health > 0):
			mx = (self.mouse_pos[0] >= POSITIONS[:, 0])&(
				  self.mouse_pos[0] <= POSITIONS[:, 0]+50)

			my = (self.mouse_pos[1] >= POSITIONS[:, 1])&(
				  self.mouse_pos[1] <= POSITIONS[:, 1]+50)

			mask = mx&my
			self.choice_letter = LETTERS[mask][0]
			if self.choice_letter in self.tested_letters:
				self.choice_letter = None
				self.show_alredy_tryed = True
			else:
				self.show_alredy_tryed = False
				self.tested_letters.append(self.choice_letter)
				not_in = True
				for i, w in enumerate(self.choiced):
					if w in self.a_like:
						w = 'a'
					elif w in self.c_like:
						w = 'c'
					elif w in self.e_like:
						w = 'e'
					elif w in self.i_like:
						w = 'i'
					elif w in self.o_like:
						w = 'o'
					elif w in self.u_like:
						w = 'u'
		
					if w == self.choice_letter:
						self.representation[i] = True
						not_in = False

				if not_in:
					self.health -= 1
					self.clavier[LETTERS == self.choice_letter] = -1
				else:
					self.clavier[LETTERS == self.choice_letter] = 1

	def make_guess_response(self):
		"""
		Fonction d'interaction de l'humain pour répondre aux propositions de
		l'ordinateur.
		"""
		if self.propose != None:
			if self.m_on_conf_mkg & (type(self.is_letter) == bool):
				self.show_is_there = False
				if self.is_letter:
					if (0 in self.etat)&(self.one_possible == False):
						self.etat[self.etat == 0] = 1
						self.must_do_some = False
						if len(self.etat[self.etat == 1]) == self.length:
							self.result_mg = 'v'
						else:
							self.update_from_answer()
							if self.no_possible == False:
								self.whats_best()
								self.is_letter = None

					elif self.one_possible:
						self.choiced = self.propose
						self.representation[:] = True
						self.etat[:] = 1
						self.must_do_some = False
						self.result_mg = 'v'

					else:
						self.must_do_some = True

				else:
					self.health -= 1
					if self.health == 0:
						self.result_mg = 'p'

					elif self.one_possible:
						self.health = 0
						self.result_mg = 'p'
						self.no_possible = True

					else:
						self.update_from_answer()
						self.whats_best()
						self.is_letter = None

			elif self.m_on_conf_mkg & (type(self.is_letter) != bool):
				self.show_is_there = True

			elif self.m_on_oui_mkg:
				self.is_letter = True
				self.show_is_there = False
				self.must_do_some = False

			elif self.m_on_non_mkg:
				self.is_letter = False
				self.show_is_there = False
				self.choiced = np.array(list(self.choiced), dtype=object)
				self.choiced[self.etat == 0] = '_'
				self.choiced = np.sum(self.choiced)
				self.representation[self.etat == 0] = False
				self.etat[self.etat == 0] = -1
				self.must_do_some = False

			elif self.is_letter:
				if True in self.m_on_propose:
					self.selected = self.m_on_propose*1 + self.selected*2
					self.selected[self.selected > 1] = 0
					self.selected = self.selected.astype(bool)
					self.must_do_some = False

				else:
					if True in self.m_on_tiret_mg:
						if self.etat[self.m_on_tiret_mg] == 1:
							pass

						elif True in self.selected:
							self.etat[self.m_on_tiret_mg] = 0
							self.representation[self.m_on_tiret_mg] = True
							self.choiced = np.array(list(self.choiced), dtype=object)
							self.choiced[self.m_on_tiret_mg] = self.possibles[self.selected]
							self.choiced = np.sum(self.choiced)
							self.must_do_some = False

						else:
							self.etat[self.m_on_tiret_mg] = -1
							self.representation[self.m_on_tiret_mg] = False
							self.choiced = np.array(list(self.choiced), dtype=object)
							self.choiced[self.m_on_tiret_mg] = '_'
							self.choiced = np.sum(self.choiced)

	def draw_init(self, window):
		"""
		Fonction pour afficher l'écrant d'acceuil.
		"""
		window.fill(BG_COLOUR)
		title = TITLE_FONT.render('Bienvenue dans le jeu du pendu !', 1, 'black')
		window.blit(title, (WIDTH/2-title.get_width()/2, 100-title.get_height()/2))
		mode = TEXT_FONT.render('Quel mode voulez-vous tester ?', 1, 'black')
		window.blit(mode, (WIDTH/2-mode.get_width()/2, 200-mode.get_height()/2))

		mode_guess = TEXT_FONT.render("Deviner un mot choisit par l'ordinateur",
									  1, 'black')
		pygame.draw.rect(window, BUTTON_COLOR,
						   (WIDTH/2-mode_guess.get_width()*0.55,
							300-mode_guess.get_height()*0.55,
							mode_guess.get_width()*1.1,
							mode_guess.get_height()*1.1))

		if self.mouse_on_guess:
			pygame.draw.rect(window, (0, 0, 0),
								(WIDTH/2-mode_guess.get_width()*0.55,
								300-mode_guess.get_height()*0.55,
								mode_guess.get_width()*1.1,
								mode_guess.get_height()*1.1), 3)

		window.blit(mode_guess, (WIDTH/2-mode_guess.get_width()/2,
								 300-mode_guess.get_height()/2))

		mode_make_guess = TEXT_FONT.render("Faire deviner un mot à l'ordinateur",
											1, 'black')
		pygame.draw.rect(window, BUTTON_COLOR,
						   (WIDTH/2-mode_make_guess.get_width()*0.55,
							400-mode_make_guess.get_height()*0.55,
							mode_make_guess.get_width()*1.1,
							mode_make_guess.get_height()*1.1))

		if self.mouse_on_m_guess:
			pygame.draw.rect(window, (0, 0, 0),
								(WIDTH/2-mode_make_guess.get_width()*0.55,
								400-mode_make_guess.get_height()*0.55,
								mode_make_guess.get_width()*1.1,
								mode_make_guess.get_height()*1.1), 3)

		window.blit(mode_make_guess, (WIDTH/2-mode_make_guess.get_width()/2,
									  400-mode_make_guess.get_height()/2))

		pygame.display.update()

	def draw_init_guess(self, window):
		"""
		Fonction pour afficher l'écrant du choix des caractéristiques du mot
		tiré par l'ordinateur.
		"""
		window.fill(BG_COLOUR)
		pygame.draw.polygon(window, BUTTON_COLOR, ARROW)
		if self.mouse_on_return:
			pygame.draw.polygon(window, (0, 0, 0), ARROW, 3)

		mode = TEXT_FONT.render("Mode choisit : deviner un mot choisit par l'ordinateur",
								  1, 'black')
		window.blit(mode, (WIDTH/2-mode.get_width()/2, 100-mode.get_height()/2))

		min_tx = TEXT_FONT.render('Nombre minimum de caracteres (tirets inclus)',
									1, 'black')
		window.blit(min_tx, (WIDTH/2-min_tx.get_width()/2,
							 150-min_tx.get_height()/2))

		pygame.draw.rect(window, BUTTON_COLOR, (WIDTH/4-25, 175, 50, 50))
		pygame.draw.polygon(window, (0, 0, 0), CROSS_UP)
		if self.mouse_on_cr_up:
			pygame.draw.rect(window, (0, 0, 0), (WIDTH/4-25, 175, 50, 50), 3)

		numlw_txt = TEXT_FONT.render(str(self.length_limits[0]), 1, 'black')
		pygame.draw.rect(window, (255, 250, 250), (WIDTH/2, 175, 50, 50))
		pygame.draw.rect(window, (0, 0, 0), (WIDTH/2, 175, 50, 50), 3)
		window.blit(numlw_txt, (WIDTH/2-numlw_txt.get_width()/2+25,
								175-numlw_txt.get_height()/2+25))

		pygame.draw.rect(window, BUTTON_COLOR, (WIDTH*3/4-25, 175, 50, 50))
		pygame.draw.rect(window, (0, 0, 0), (WIDTH*3/4+10-25, 195, 30, 10))
		if self.mouse_on_mi_up:
			pygame.draw.rect(window, (0, 0, 0), (WIDTH*3/4-25, 175, 50, 50), 3)

		max_tx = TEXT_FONT.render('nombre maximum de caracteres (tirets inclus)',
									1, 'black')
		window.blit(max_tx, (WIDTH/2-max_tx.get_width()/2,
							 275-max_tx.get_height()/2))

		pygame.draw.rect(window, BUTTON_COLOR, (WIDTH/4-25, 300, 50, 50))
		pygame.draw.polygon(window, (0, 0, 0), CROSS_DW)
		if self.mouse_on_cr_dw:
			pygame.draw.rect(window, (0, 0, 0), (WIDTH/4-25, 300, 50, 50), 3)

		numup_txt = TEXT_FONT.render(str(self.length_limits[1]), 1, 'black')
		pygame.draw.rect(window, (255, 250, 250), (WIDTH/2, 300, 50, 50))
		pygame.draw.rect(window, (0, 0, 0), (WIDTH/2, 300, 50, 50), 3)
		window.blit(numup_txt, (WIDTH/2-numup_txt.get_width()/2+25,
							  300-numup_txt.get_height()/2+25))

		pygame.draw.rect(window, BUTTON_COLOR, (WIDTH*3/4-25, 300, 50, 50))
		pygame.draw.rect(window, (0, 0, 0), (WIDTH*3/4+10-25, 320, 30, 10))
		if self.mouse_on_mi_dw:
			pygame.draw.rect(window, (0, 0, 0), (WIDTH*3/4-25, 300, 50, 50), 3)

		tiret_tx = TEXT_FONT.render("Il peut y avoir un (ou plusieurs) trait d'union",
									1, 'black')
		window.blit(tiret_tx, (WIDTH/2-tiret_tx.get_width()/2,
								400-tiret_tx.get_height()/2))

		if self.tirets:
			pygame.draw.rect(window, (0, 255, 0), (WIDTH/4-50, 425, 100, 50))
		else:
			pygame.draw.rect(window, BUTTON_COLOR, (WIDTH/4-50, 425, 100, 50))

		if self.m_on_tiret_t:
			pygame.draw.rect(window, (0, 0, 0), (WIDTH/4-50, 425, 100, 50), 3)
		
		if self.tirets == False:
			pygame.draw.rect(window, (255, 0, 0), (WIDTH*3/4-50, 425, 100, 50))
		else:
			pygame.draw.rect(window, BUTTON_COLOR, (WIDTH*3/4-50, 425, 100, 50))

		if self.m_on_tiret_f:
			pygame.draw.rect(window, (0, 0, 0), (WIDTH*3/4-50, 425, 100, 50), 3)

		o_tx = TEXT_FONT.render("Oui", 1, 'black')
		window.blit(o_tx, (WIDTH/4-o_tx.get_width()/2,
							425-o_tx.get_height()/2+25))

		n_tx = TEXT_FONT.render("Non", 1, 'black')
		window.blit(n_tx, (WIDTH*3/4-n_tx.get_width()/2,
							425-n_tx.get_height()/2+25))

		pygame.draw.rect(window, BUTTON_COLOR, (WIDTH/2-100, 500, 200, 50))
		if self.m_on_start_g:
			pygame.draw.rect(window, (0, 0, 0), (WIDTH/2-100, 500, 200, 50), 3)

		st_tx = TEXT_FONT.render("Commencer", 1, 'black')
		window.blit(st_tx, (WIDTH/2-st_tx.get_width()/2,
						    500-st_tx.get_height()/2+25))

		if self.show_must_choice_tiret:
			mtir_tx_1 = TEXT_FONT.render(
					"Vous devez indiquer si il est possible de tomber sur un",
					1, 'black')

			window.blit(mtir_tx_1, (WIDTH/2-mtir_tx_1.get_width()/2,
									615-mtir_tx_1.get_height()/2))
			
			must_tiret_tx_2 = TEXT_FONT.render(
					"mot ayant un (ou plusieurs) trait d'union", 1, 'black')

			window.blit(must_tiret_tx_2, (WIDTH/2-must_tiret_tx_2.get_width()/2,
										  650-must_tiret_tx_2.get_height()/2))

		pygame.display.update()

	def draw_init_make_guess(self, window):
		"""
		Fonction pour afficher l'écrant du choix des caractéristiques du mot
		que l'ordinateur devra deviner.
		"""
		window.fill(BG_COLOUR)
		pygame.draw.polygon(window, BUTTON_COLOR, ARROW)

		if self.mouse_on_return:
			pygame.draw.polygon(window, (0, 0, 0), ARROW, 3)

		mode = TEXT_FONT.render(
						"Mode choisit : faire deviner un mot à l'ordinateur",
						1, 'black')

		window.blit(mode, (WIDTH/2-mode.get_width()/2, 100-mode.get_height()/2))

		len_tx = TEXT_FONT.render('Nombre de caracteres (tirets inclus)',
								  1, 'black')

		window.blit(len_tx, (WIDTH/2-len_tx.get_width()/2,
							 150-len_tx.get_height()/2))

		pygame.draw.rect(window, BUTTON_COLOR, (WIDTH/4-25, 175, 50, 50))
		pygame.draw.polygon(window, (0, 0, 0), CROSS_UP)
		if self.mouse_on_cr_up:
			pygame.draw.rect(window, (0, 0, 0), (WIDTH/4-25, 175, 50, 50), 3)

		numlw_txt = TEXT_FONT.render(str(self.length), 1, 'black')
		pygame.draw.rect(window, (255, 250, 250), (WIDTH/2-25, 175, 50, 50))
		pygame.draw.rect(window, (0, 0, 0), (WIDTH/2-25, 175, 50, 50), 3)
		window.blit(numlw_txt, (WIDTH/2-numlw_txt.get_width()/2,
							  175-numlw_txt.get_height()/2+25))

		pygame.draw.rect(window, BUTTON_COLOR, (WIDTH*3/4-25, 175, 50, 50))
		pygame.draw.rect(window, (0, 0, 0), (WIDTH*3/4-15, 195, 30, 10))
		if self.mouse_on_mi_up:
			pygame.draw.rect(window, (0, 0, 0), (WIDTH*3/4-25, 175, 50, 50), 3)

		tir1_tx = TEXT_FONT.render(
				"Cliquez sur les cases où il y a un trait d'union (ignorer cette",
				1, 'black')

		window.blit(tir1_tx, (WIDTH/2-tir1_tx.get_width()/2,
							  265-tir1_tx.get_height()/2))

		tir2_tx = TEXT_FONT.render("étape si il n'y en a pas dans votre mot)",
								   1, 'black')
		window.blit(tir2_tx, (WIDTH/2-tir2_tx.get_width()/2,
							  300-tir2_tx.get_height()/2))

		for i in range(self.length):
			if self.choiced[i] != '-':
				if self.m_on_tiret_mg[i]:
					pygame.draw.rect(window, (255, 0, 0),
									 (i*30+self.recenter, 400, 25, 5))
				else:
					pygame.draw.rect(window, (0, 0, 0),
									 (i*30+self.recenter, 400, 25, 5))
			else:
				if self.m_on_tiret_mg[i]:
					pygame.draw.rect(window, (255, 0, 0),
									 (i*30+self.recenter+2.5, 385, 20, 3))
				else:
					pygame.draw.rect(window, (0, 0, 0),
									 (i*30+self.recenter+2.5, 385, 20, 3))

		pygame.draw.rect(window, BUTTON_COLOR, (WIDTH/2-100, 450, 200, 50))
		if self.m_on_start_m:
			pygame.draw.rect(window, (0, 0, 0), (WIDTH/2-100, 450, 200, 50), 3)

		st_tx = TEXT_FONT.render('Commencer', 1, 'black')
		window.blit(st_tx, (WIDTH/2-st_tx.get_width()/2,
							450-st_tx.get_height()/2+25))

		if self.show_no_word:
			no_tx1 = TEXT_FONT.render(
						"Je n'ai aucun mot dans ma base de données qui puisse",
						1, (0, 0, 0))
			window.blit(no_tx1, (WIDTH/2-no_tx1.get_width()/2,
								 525-no_tx1.get_height()/2+25))

			no_tx2 = TEXT_FONT.render(
					  "corespondre aux caractéristiques entrées", 1, (0, 0, 0))
			window.blit(no_tx2, (WIDTH/2-no_tx2.get_width()/2,
								 550-no_tx2.get_height()/2+25))

		pygame.display.update()

	def draw_guess(self, window):
		"""
		Fonction pour afficher l'écrant du choix des "minimale" lettres
		pouvant être choisit par l'humain pour chercher à trouver le mot tiré
		par l'ordinateur.
		"""
		window.fill(BG_COLOUR)
		pygame.draw.polygon(window, BUTTON_COLOR, ARROW)
		if self.mouse_on_return:
			pygame.draw.polygon(window, (0, 0, 0), ARROW, 3)

		for i in range(self.length):
			if self.choiced[i] != '-':
				pygame.draw.rect(window, (0, 0, 0),
								 (i*30+self.recenter, 400, 25, 5))
			else:
				pygame.draw.rect(window, (0, 0, 0),
								 (i*30+self.recenter+2.5, 385, 20, 3))

			if self.representation[i]:
				tx = TEXT_FONT.render(str(self.choiced[i]), 1, 'black')
				window.blit(tx, (i*30+self.recenter-tx.get_width()/2+12.5, 365))
			elif self.health <= 0:
				tx = TEXT_FONT.render(str(self.choiced[i]), 1, 'red')
				window.blit(tx, (i*30+self.recenter-tx.get_width()/2+12.5, 365))

		for i in range(26):
			if self.clavier[i] == -1:
				pygame.draw.rect(window, (255, 0, 0),
								 (POSITIONS[i, 0], POSITIONS[i, 1], 50, 50))
			elif self.clavier[i] == 1:
				pygame.draw.rect(window, (0, 255, 0),
								 (POSITIONS[i, 0], POSITIONS[i, 1], 50, 50))
			else:
				pygame.draw.rect(window, BUTTON_COLOR,
								 (POSITIONS[i, 0], POSITIONS[i, 1], 50, 50))

			if self.m_on_letters[i] & (self.clavier[i] == 0):
				pygame.draw.rect(window, (0, 0, 0),
								 (POSITIONS[i, 0], POSITIONS[i, 1], 50, 50), 3)

			let_tx = TEXT_FONT.render(str(LETTERS[i]), 1, 'black')
			window.blit(let_tx, (POSITIONS[i, 0]+25-let_tx.get_width()/2,
								 POSITIONS[i, 1]-let_tx.get_height()/2+25))

		if self.health > 1:
			h_tx = TEXT_FONT.render('Points de vie = '+str(self.health),
									1, 'black')
		else:
			h_tx = TEXT_FONT.render('Point de vie = '+str(self.health),
									1, 'black')

		window.blit(h_tx, (25, 175))

		if self.health <= 7:
			pygame.draw.rect(window, (0, 0, 0), (450, 300, 300, 10))
		if self.health <= 6:
			pygame.draw.rect(window, (0, 0, 0), (650, 100, 10, 200))
		if self.health <= 5:
			pygame.draw.rect(window, (0, 0, 0), (525, 100, 150, 10))
		if self.health <= 4:
			pygame.draw.rect(window, (0, 0, 0), (575, 100, 10, 65))
		if self.health <= 3:
			pygame.draw.circle(window, (0, 0, 0), (580, 180), 20)
			pygame.draw.circle(window, BG_COLOUR, (580, 180), 15)
		if self.health <= 2:
			pygame.draw.rect(window, (0, 0, 0), (578.5, 200, 5, 50))
		if self.health <= 1:
			pygame.draw.rect(window, (0, 0, 0), (565, 212.5, 30, 4))
		if self.health <= 0:
			
			pygame.draw.polygon(window, (0, 0, 0), ((580, 235), (590, 280),
												    (585, 280), (580, 250),
													(575, 280), (570, 280)))

		if self.result_g == 'v':
			vic_tx = RESULT_FONT.render('Vous avez trouvé le mot !',
										1, (0, 255, 0))
			window.blit(vic_tx, (25, 215))

		if self.result_g == 'p':
			per_tx = RESULT_FONT.render("Vous n'avez pas trouvé le mot !",
										1, (255, 0, 0))
			window.blit(per_tx, (25, 215))

		if self.show_alredy_tryed:
			tryed_tx = TEXT_FONT.render('Vous avez déjà essayé cette lettre',
										1, 'black')
			window.blit(tryed_tx, (WIDTH/2-tryed_tx.get_width()/2, 600))

		pygame.display.update()

	def draw_make_guess(self, window):
		"""
		Fonction pour afficher l'écrant du choix des lettres "minimale"
		choisient par l'ordinateur et les intéractions possibles pour
		l'humain.
		"""
		window.fill(BG_COLOUR)
		pygame.draw.polygon(window, BUTTON_COLOR, ARROW)
		if self.mouse_on_return:
			pygame.draw.polygon(window, (0, 0, 0), ARROW, 3)

		for i in range(self.length):
			if self.choiced[i] != '-':
				if self.m_on_tiret_mg[i]:
					pygame.draw.rect(window, (0, 0, 255),
									 (i*30+self.recenter, 350, 25, 5))
				else:
					pygame.draw.rect(window, (0, 0, 0),
									 (i*30+self.recenter, 350, 25, 5))

			if self.representation[i]:
				if self.etat[i] == 0:
					tx = TEXT_FONT.render(str(self.choiced[i]), 1, (0, 0, 255))
				else:
					tx = TEXT_FONT.render(str(self.choiced[i]), 1, 'black')

				window.blit(tx, (i*30+self.recenter-tx.get_width()/2+12.5, 320))

		if (self.propose != None)&(self.one_possible == False):
			is_tx1 = TEXT_FONT.render("Est-ce qu'il y a un :", 1, 'black')
			window.blit(is_tx1, (50, 75))
			is_tx2 = TEXT_FONT.render("'"+str(self.propose)+"'", 1, 'black')
			window.blit(is_tx2, (50-is_tx2.get_width()/2+is_tx1.get_width()/2, 100))

		elif (self.propose != None)&(self.one_possible):
			is_tx1 = TEXT_FONT.render("Est-ce qu'il s'agit du mot :", 1, 'black')
			window.blit(is_tx1, (50, 75))
			is_tx2 = TEXT_FONT.render("'"+str(self.propose)+"'", 1, 'black')
			window.blit(is_tx2, (50-is_tx2.get_width()/2+is_tx1.get_width()/2, 100))

		if self.is_letter:
			pygame.draw.rect(window, (0, 255, 0), (50, 150, 100, 50))
			if self.one_possible == False:
				for i in range(len(self.possibles)):
					if self.selected[i]:
						pygame.draw.rect(window, (0, 0, 255), (self.center_propos[i],
												 400, 50, 50))
					else:
						pygame.draw.rect(window, BUTTON_COLOR, (self.center_propos[i],
												 400, 50, 50))
	
					if self.m_on_propose[i]:
						pygame.draw.rect(window, (0, 0, 0), (self.center_propos[i],
											 400, 50, 50), 3)
	
					tx_pl = TEXT_FONT.render(str(self.possibles[i]), 1, 'black')
					window.blit(tx_pl, (self.center_propos[i]+25-tx_pl.get_width()/2,
										425-tx_pl.get_height()/2))

		else:
			pygame.draw.rect(window, BUTTON_COLOR, (50, 150, 100, 50))

		tx_y = TEXT_FONT.render('Oui', 1, (0, 0, 0))
		window.blit(tx_y, (100-tx_y.get_width()/2, 175-tx_y.get_height()/2))
		if self.m_on_oui_mkg:
			pygame.draw.rect(window, (0, 0, 0), (50, 150, 100, 50), 3)

		if self.is_letter == False:
			pygame.draw.rect(window, (255, 0, 0), (200, 150, 100, 50))
		else:
			pygame.draw.rect(window, BUTTON_COLOR, (200, 150, 100, 50))

		tx_n = TEXT_FONT.render('Non', 1, (0, 0, 0))
		window.blit(tx_n, (250-tx_n.get_width()/2, 175-tx_n.get_height()/2))
		if self.m_on_non_mkg:
			pygame.draw.rect(window, (0, 0, 0), (200, 150, 100, 50), 3)

		pygame.draw.rect(window, BUTTON_COLOR, (100, 225, 150, 50))
		tx_c = TEXT_FONT.render('Confirmer', 1, (0, 0, 0))
		window.blit(tx_c, (175-tx_c.get_width()/2, 250-tx_c.get_height()/2))
		if self.m_on_conf_mkg:
			pygame.draw.rect(window, (0, 0, 0), (100, 225, 150, 50), 3)

		if self.show_is_there:
			tx_isth1 = TEXT_FONT.render('Vous devez indiquer si la lettre proposée est présente',
									    1, 'black')
			window.blit(tx_isth1, (WIDTH/2-tx_isth1.get_width()/2, 400))

			tx_isth2 = TEXT_FONT.render('ou non', 1, 'black')
			window.blit(tx_isth2, (WIDTH/2-tx_isth2.get_width()/2, 425))

		if self.must_do_some:
			tx_isth1 = TEXT_FONT.render('Vous devez indiquer où la lettre proposée est présente',
									    1, 'black')
			window.blit(tx_isth1, (WIDTH/2-tx_isth1.get_width()/2, 450))

			tx_isth2 = TEXT_FONT.render('ou changer la sélection à non', 1, 'black')
			window.blit(tx_isth2, (WIDTH/2-tx_isth2.get_width()/2, 475))

		if self.health <= 7:
			pygame.draw.rect(window, (0, 0, 0), (450, 250, 300, 10))
		if self.health <= 6:
			pygame.draw.rect(window, (0, 0, 0), (650, 50, 10, 200))
		if self.health <= 5:
			pygame.draw.rect(window, (0, 0, 0), (525, 50, 150, 10))
		if self.health <= 4:
			pygame.draw.rect(window, (0, 0, 0), (575, 50, 10, 65))
		if self.health <= 3:
			pygame.draw.circle(window, (0, 0, 0), (580, 130), 20)
			pygame.draw.circle(window, BG_COLOUR, (580, 130), 15)
		if self.health <= 2:
			pygame.draw.rect(window, (0, 0, 0), (578.5, 150, 5, 50))
		if self.health <= 1:
			pygame.draw.rect(window, (0, 0, 0), (565, 165.5, 30, 4))
		if self.health <= 0:
			pygame.draw.polygon(window, (0, 0, 0), ((580, 185), (590, 230),
												    (585, 230), (580, 200),
													(575, 230), (570, 230)))

		if self.no_possible:
			tx_isth1 = TEXT_FONT.render("Je n'ai pas de mot corresponant aux caractéristiques que",
									    1, 'black')
			window.blit(tx_isth1, (WIDTH/2-tx_isth1.get_width()/2, 400))

			tx_isth2 = TEXT_FONT.render("vous m'avez fournis. J'ai donc perdus. Je vous conseille",
										1, 'black')
			window.blit(tx_isth2, (WIDTH/2-tx_isth2.get_width()/2, 425))

			tx_isth3 = TEXT_FONT.render("de mettre à jour ma base de données en conséquence.",
										1, 'black')
			window.blit(tx_isth3, (WIDTH/2-tx_isth3.get_width()/2, 450))

		if (self.result_mg == 'p')&(self.one_possible == False):
			tx_re = TEXT_FONT.render("J'ai perdus, je n'ai pas trouvé le mot que vous aviez choisit",
									 1, 'black')
			window.blit(tx_re, (WIDTH/2-tx_re.get_width()/2, 450))

		elif self.result_mg == 'v':
			tx_re = TEXT_FONT.render("J'ai gagné, j'ai trouvé le mot que vous aviez choisit",
									 1, 'black')
			window.blit(tx_re, (WIDTH/2-tx_re.get_width()/2, 450))

		pygame.display.update()

def main():
	"""
	Fonction principal.
	"""
	game = Game()
	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		game.get_mouse_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break

			if event.type == pygame.MOUSEBUTTONDOWN:
				if game.initialized == False:
					game.choice_mode()
				elif game.initialized&(game.start_g == False)&(game.start_m == False):
					if game.mouse_on_return:
						game.re_init_accueil()

					elif game.make_guess:
						game.update_init_make_guess()

					elif game.guess:
						game.update_init_guess()

				elif game.initialized & game.start_g:
					if game.mouse_on_return:
						game.re_init_guess()
					else:
						game.choice_letter_guess()

				elif game.initialized & game.start_m:
					if game.mouse_on_return:
						game.re_init_make_guess()
					else:
						game.make_guess_response()

		if game.initialized:
			if game.guess:
				if game.start_g:
					game.mouse_return_on()
					game.mouse_on_letters()
					game.guess_victory()
					game.draw_guess(WIN)
					if game.result_g != None:
						pygame.time.wait(3000)
						game.re_init_accueil()

				else:
					game.mouse_on_pm_up()
					game.mouse_on_pm_down()
					game.mouse_return_on()
					game.mouse_on_tirets_guess()
					game.mouse_on_start_guess()
					game.draw_init_guess(WIN)

			elif game.make_guess:
				if game.start_m:
					if game.propose == None:
						game.whats_best()

					game.mouse_on_letters_mg()
					game.mouse_on_repsonse()
					game.mouse_on_propose()
					game.mouse_return_on()
					game.draw_make_guess(WIN)
					if game.result_mg != None:
						pygame.time.wait(4000)
						game.re_init_accueil()

				else:
					game.mouse_on_start_mg()
					game.mouse_on_pm_up()
					game.mouse_return_on()
					game.mouse_on_tirets_mg()
					game.draw_init_make_guess(WIN)

			else:
				raise ValueError('guess or make_guess should be True !')

		else:
			game.draw_init(WIN)
			game.mouse_mode_on()

	pygame.quit()

if __name__ == '__main__':
	main()
