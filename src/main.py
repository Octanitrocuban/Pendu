"""
Interface graphique et logique pour le jeu du pendu.
"""

import numpy as np
import graphical
import actions
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
		self.two_player = False
		self.mouse_on_guess = False
		self.mouse_on_m_guess = False
		self.mouse_on_2_player = False
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
		self.profil = np.zeros(5, dtype='int8')
		self.show_no_word = False

		# two human player
		self.start_2p = False
		self.health_p1 = 7
		self.health_p2 = 7
		self.vict_1 = 0
		self.vict_2 = 0
		self.defai_1 = 0
		self.defai_2 = 0
		self.turn = None
		self.step = None
		self.mouse_on_p1 = False
		self.mouse_on_p2= False

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

	def is_possible_start_mg(self): # 185 -> 163
		"""
		Fonction pour voir si il y a au moins un mots répondant aux
		caractéristiques données par l'utilisateur.
		"""
		(self.mapp, self.rec_mapp, self.can_start_m
		 ) = actions.is_possible_start_mg(DATA, self.length, self.num_tirets,
										  self.profil)

	def whats_best(self): # 229 -> 177
		"""
		Fonction pour chercher le meilleur caractère à utiliser pour trouver
		le mot choisit par l'humain. L'approche est baser sur la fréquence d'
		apparition de chaque lettre "minimale".
		"""
		(self.no_possible, self.health, self.result_mg, self.one_possible,
		 self.propose, self.possibles, self.center_propos, self.m_on_propose,
		 self.selected) = actions.whats_best(DATA, self.mapp, self.no_possible,
											 self.health, self.result_mg,
											 self.one_possible, self.propose,
											 self.choiced, self.link_dico,
											 WIDTH, self.representation,
											 self.center_propos, self.possibles,
											 self.m_on_propose, self.selected)

	def update_from_answer(self): # 253 -> 238
		"""
		Fonction pour enlever les mots ne répondant pas aux caractéristiques
		connues.
		"""
		self.mapp = actions.update_from_answer(self.mapp, self.is_letter,
											   self.choiced, self.possibles,
											   DATA)

	def guess_victory(self): # 260 -> 2558
		"""
		Fonction pour détecter si l'humain a réussis (gagné) ou non (perdu) à
		trouver le mot choisit par l'ordinateur.
		"""
		self.result_g = actions.guess_victory(self.health,
											  self.representation,
											  self.length, self.result_g)

	def re_init_accueil(self):
		"""
		Fonction pour ré-initialiser le jeu jusqu'à la fenêtre d'accueil.
		"""
		# accueil / general
		self.initialized = False
		self.guess = False
		self.make_guess = False
		self.two_player = False
		self.mouse_on_guess = False
		self.mouse_on_m_guess = False
		self.mouse_on_2_player = False
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
		self.profil = np.zeros(5, dtype='int8')
		self.show_no_word = False

		# two human player
		self.start_2p = False
		self.health_p1 = 7
		self.health_p2 = 7
		self.vict_1 = 0
		self.vict_2 = 0
		self.defai_1 = 0
		self.defai_2 = 0
		self.turn = None
		self.step = None
		self.mouse_on_p1 = False
		self.mouse_on_p2= False

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
		self.two_player = False
		self.length = 5
		self.length_limits = [1, 25]
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
		self.two_player = False
		self.length = 5
		self.result_mg = None
		self.m_on_tiret_mg = False
		self.num_tirets = 0
		self.start_m = False
		self.can_start_m = False
		self.m_on_start_m = False
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

	def re_init_2_player(self):
		self.health = 7
		self.initialized = True
		self.guess = False
		self.make_guess = False
		self.two_player = True
		self.length = 5
		self.start_2p = False
		self.turn = None
		self.step = None
		self.result_mg = None
		self.clavier = np.zeros(26, dtype='int8')

		self.tested_letters = []
		self.representation = np.zeros(self.length, dtype=bool)
		self.choiced = '_'*self.length
		self.recenter = WIDTH/2-30*self.length/2
		self.profil = np.zeros(5, dtype='int8')
		self.etat = np.zeros(self.length) -1
		self.possibles = None
		self.selected = None
		self.center_propos = None
		self.is_letter = None

		self.mouse_on_cr_up = False
		self.mouse_on_mi_up = False
		self.mouse_on_return = False
		self.m_on_tiret_mg = False
		self.m_on_start_m = False
		self.mouse_on_p1 = False
		self.mouse_on_p2 = False
		self.m_on_propose = None
		self.m_on_conf_mkg = False
		self.m_on_oui_mkg = False
		self.m_on_non_mkg = False

	def mouse_mode_on(self): # 452 -> 443
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		d'un des deux bouttons du choix du type de jeu.
		"""
		(self.mouse_on_guess, self.mouse_on_m_guess,
		 self.mouse_on_2_player) = actions.mouse_mode_on(self.mouse_pos)

	def mouse_return_on(self): # 467 -> 451
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		de la flêche permettant de revenir au menu précédant.
		"""
		self.mouse_on_return = actions.mouse_return_on(self.mouse_pos,
														HEAD, ARROW, PI2)

	def mouse_on_pm_up(self): # 494 -> 485
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		des boutons servant à faire varier la valeur de la borne minimal du
		nombre de caractères d'un mot.
		"""
		(self.mouse_on_cr_up, 
		 self.mouse_on_mi_up) = actions.mouse_on_pm_up(self.mouse_pos, WIDTH)

	def mouse_on_pm_down(self): # 512 -> 503
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		des boutons servant à faire varier la valeur de la borne maximal du
		nombre de caractères d'un mot.
		"""
		(self.mouse_on_cr_dw, self.mouse_on_mi_dw
		 ) = actions.mouse_on_pm_down(self.mouse_pos, WIDTH)

	def mouse_on_tirets_guess(self): # 530 -> 521
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		boutons pour la sélection de la présence ou non de tiret(s) dans le
		mot que devra deviner l'humain.
		"""
		(self.m_on_tiret_t, self.m_on_tiret_f
		 ) = actions.mouse_on_tirets_guess(self.mouse_pos, WIDTH)

	def mouse_on_tirets_mg(self): # 545 -> 540
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		des caractères pouvant être transformé de lettre à tiret ou
		inversement.
		"""
		self.m_on_tiret_mg = actions.mouse_on_tirets_mg(self.mouse_pos,
										  				self.length,
										  				self.recenter)

	def mouse_on_start_guess(self): # 556 -> 553
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		du bouton pour lancer une partie où l'humain doit trouver un mot.
		"""
		self.m_on_start_g = actions.mouse_on_start_guess(self.mouse_pos,
														 WIDTH)

	def mouse_on_letters(self): # 569 -> 563
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		d'une des lettres du clavier.
		"""
		self.m_on_letters = actions.mouse_on_letters(self.mouse_pos, POSITIONS)

	def mouse_on_start_mg(self): # 581 -> 577
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		du bouton pour lancer une partie où l'ordinateur doit trouver le mot
		choisit par l'humain.
		"""
		self.m_on_start_m = actions.mouse_on_start_mg(self.mouse_pos, WIDTH)

	def mouse_on_repsonse(self): # 605 -> 590
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		des boutons oui/non/confirmer lors-ce-que c'est à l'ordinateur de
		trouver le mot choisit par l'humain.
		"""
		(self.m_on_oui_mkg, self.m_on_non_mkg,
		 self.m_on_conf_mkg) = actions.mouse_on_repsonse(self.mouse_pos)

	def mouse_on_propose(self): # 618 -> 614
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		d'un des caractères associé à une lettre "minimale".
		"""
		self.m_on_propose = actions.mouse_on_propose(self.mouse_pos,
													 self.is_letter,
													 self.center_propos,
													 self.m_on_propose)

	def mouse_on_letters_mg(self): # 633 -> 628
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		des caractères pouvant être transformé de lettre à tiret ou
		inversement.
		"""
		self.m_on_tiret_mg = actions.mouse_on_letters_mg(self.mouse_pos,
														 self.length,
														 self.recenter)

	def mouse_on_player(self):
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		des boutons de selection du joueur qui devra deviner / faire deviner un
		mot à l'autre joueur.
		"""
		(self.mouse_on_p1,
		 self.mouse_on_p2) = actions.mouse_on_player(self.mouse_pos)

	def choice_mode(self): # 536 -> 517
		"""
		Fonction pour détecter si le curseur de la souris se trouve au-dessus
		d'un des deux bouttons du choix du type de jeu lors du clique.
		"""
		(self.guess, self.make_guess, self.two_player, self.initialized,
		 self.choiced, self.representation, self.etat, self.recenter
		 ) = actions.choice_mode(WIDTH, self.mouse_on_guess,
								 self.mouse_on_m_guess,
								 self.mouse_on_2_player, self.guess,
								 self.make_guess, self.two_player,
								 self.initialized, self.length, self.choiced,
								 self.representation, self.etat,
								 self.recenter)

	def update_init_guess(self): # 584 -> 550
		"""
		Fonction pour détecter quelles intéractions sont faîtes sur les
		caractéristiques du mot qui sera deviné par l'humain.
		"""
		(self.length_limits, self.tirets, self.choiced, self.start_g,
		 self.length, self.representation, self.recenter,
		 self.show_must_choice_tiret) = actions.update_init_guess(
			 WIDTH, DATA, self.mouse_on_cr_up, self.mouse_on_mi_up,
			 self.mouse_on_cr_dw, self.mouse_on_mi_dw, self.m_on_tiret_t,
			 self.m_on_tiret_f, self.m_on_start_g, self.length_limits,
			 self.tirets, self.choiced, self.start_g, self.length,
			 self.representation, self.recenter, self.show_must_choice_tiret)

	def update_init_make_guess(self): # 594 -> 546
		"""
		Fonction d'intéraction de l'humain pour choisir les caractéristiques
		mot qu'il fera deviner à l'ordinateur.	
		"""
		(self.length, self.choiced, self.representation, self.etat,
		 self.profil, self.show_no_word, self.num_tirets, self.start_m,
		 self.mapp, self.rec_mapp, self.can_start_m, self.recenter
		 ) = actions.update_init_make_guess(
			DATA, WIDTH, self.mouse_on_cr_up, self.mouse_on_mi_up,
			self.m_on_tiret_mg, self.m_on_start_m, self.length, self.choiced,
			self.representation, self.etat, self.profil, self.recenter,
			self.show_no_word, self.num_tirets, self.start_m,
			self.can_start_m, self.mapp, self.rec_mapp)

	def update_init_2_player(self): # 652 -> 613
		"""
		Fonction d'intéraction de l'humain pour choisir les caractéristiques
		mot qu'il fera deviner à l'autre humain.	
		"""
		(self.choiced, self.representation, self.etat, self.profil,
		 self.recenter, self.show_no_word, self.num_tirets, self.turn,
		 self.start_2p, self.step, self.length
		 ) = actions.update_init_2_player(WIDTH, self.mouse_on_cr_up,
										  self.mouse_on_mi_up,
										  self.m_on_tiret_mg,
										  self.mouse_on_p1, self.mouse_on_p2,
										  self.m_on_start_m, self.length,
										  self.choiced, self.representation,
										  self.etat, self.profil,
										  self.recenter, self.show_no_word,
										  self.num_tirets, self.turn,
										  self.start_2p, self.step)

	def choice_letter_guess(self): # 668 -> 640
		"""
		Fonction d'interaction de l'humain pour choisir quelle lettre
		"minimale" choisir.
		"""
		(self.health, self.choice_letter, self.tested_letters,
		 self.show_alredy_tryed, self.representation, self.clavier
		 ) = actions.choice_letter_guess(self.m_on_letters, self.health,
										 self.choice_letter,
										 self.tested_letters,
										 self.show_alredy_tryed,
										 self.choiced, self.a_like,
										 self.c_like, self.e_like,
										 self.i_like, self.o_like,
										 self.u_like, self.representation,
										 self.clavier, LETTERS)

	def make_guess_response(self): # 672 -> 600
		"""
		Fonction d'interaction de l'humain pour répondre aux propositions de
		l'ordinateur.
		"""
		(self.is_letter, self.show_is_there, self.etat, self.must_do_some,
		 self.result_mg, self.no_possible, self.choiced, self.representation,
		 self.health, self.selected, self.m_on_propose, self.possibles,
		 self.center_propos, self.propose, self.one_possible, self.mapp
		 ) = actions.make_guess_response(
			DATA, WIDTH, self.link_dico, self.m_on_conf_mkg,
			self.show_is_there, self.must_do_some, self.m_on_oui_mkg,
			self.m_on_non_mkg, self.m_on_propose, self.m_on_tiret_mg,
			self.propose, self.is_letter, self.etat, self.one_possible,
			self.no_possible, self.length, self.result_mg, self.choiced,
			self.representation, self.health, self.selected, self.possibles,
			self.center_propos, self.mapp)

	def make_guess_human(self):
		"""
		Fonction où un joueur choisit / confirme / remplit le mot.
		"""
		(self.step, self.health, self.vict_1, self.vict_2,
		 self.defai_1, self.defai_2, self.choice_letter, self.tested_letters,
		 self.choiced, self.is_letter, self.etat, self.representation,
		 self.clavier, self.possibles, self.center_propos, self.m_on_propose,
		 self.selected, self.result_mg
		 ) = actions.make_guess_human(
			WIDTH, LETTERS,
			self.m_on_letters, self.m_on_oui_mkg, self.m_on_non_mkg,
			self.m_on_conf_mkg, self.m_on_tiret_mg, self.m_on_propose,
			self.step, self.health, self.vict_1,
			self.vict_2, self.defai_1, self.defai_2, self.representation,
			self.clavier, self.is_letter, self.choice_letter,
			self.tested_letters, self.choiced, self.etat, self.link_dico,
			self.propose, self.possibles, self.center_propos,
			self.selected, self.length, self.result_mg, self.turn,
			self.a_like, self.c_like, self.e_like, self.i_like, self.o_like,
			self.u_like)

	def draw_init(self, window): # 719 -> 681
		"""
		Fonction pour afficher l'écrant d'acceuil.
		"""
		graphical.draw_init(window, BG_COLOUR, WIDTH, TITLE_FONT, TEXT_FONT,
							BUTTON_COLOR, self.mouse_on_guess,
							self.mouse_on_m_guess, self.mouse_on_2_player)

	def draw_init_guess(self, window): # 791 -> 696
		"""
		Fonction pour afficher l'écrant du choix des caractéristiques du mot
		tiré par l'ordinateur.
		"""
		graphical.draw_init_guess(window, BG_COLOUR, WIDTH, TEXT_FONT,
								  BUTTON_COLOR, ARROW, CROSS_UP, CROSS_DW,
								  self.mouse_on_return, self.mouse_on_cr_up,
								  self.mouse_on_mi_up, self.mouse_on_cr_dw,
								  self.mouse_on_mi_dw, self.m_on_tiret_t,
								  self.m_on_tiret_f, self.m_on_start_g,
								  self.length_limits, self.tirets,
								  self.show_must_choice_tiret)


	def draw_init_make_guess(self, window): # 786 -> 711
		"""
		Fonction pour afficher l'écrant du choix des caractéristiques du mot
		que l'ordinateur devra deviner.
		"""
		graphical.draw_init_make_guess(window, WIDTH, BG_COLOUR, BUTTON_COLOR,
									   TEXT_FONT, ARROW, CROSS_UP,
									   self.mouse_on_return,
									   self.mouse_on_cr_up,
									   self.mouse_on_mi_up,
									   self.m_on_tiret_mg, self.m_on_start_m,
									   self.length, self.choiced,
									   self.recenter, self.show_no_word)

	def draw_init_2_player(self, window): # 910 -> 832
		"""
		Fonction pour afficher l'écrant du choix des caractéristiques du mot
		que l'autre humain devra deviner.
		"""
		graphical.draw_init_2_player(window, WIDTH, BG_COLOUR, BUTTON_COLOR,
									 ARROW, CROSS_UP, TEXT_FONT,
									 self.mouse_on_return, self.mouse_on_cr_up,
									 self.mouse_on_mi_up, self.m_on_tiret_mg,
									 self.m_on_start_m, self.mouse_on_p1,
									 self.mouse_on_p2, self.length,
									 self.choiced, self.recenter, self.turn,
									 self.vict_1, self.defai_1, self.vict_2,
									 self.defai_2)

	def draw_guess(self, window): # 803 -> 724
		"""
		Fonction pour afficher l'écrant du choix des "minimale" lettres
		pouvant être choisit par l'humain pour chercher à trouver le mot tiré
		par l'ordinateur.
		"""
		graphical.draw_guess(window, WIDTH, BG_COLOUR, BUTTON_COLOR,
							 TEXT_FONT, RESULT_FONT, ARROW, POSITIONS,
							 LETTERS, self.mouse_on_return, self.m_on_letters,
							 self.length, self.choiced, self.recenter,
							 self.representation, self.clavier, self.health,
							 self.result_g, self.show_alredy_tryed)

	def draw_make_guess(self, window): # 868 -> 744
		"""
		Fonction pour afficher l'écrant du choix des lettres "minimale"
		choisient par l'ordinateur et les intéractions possibles pour
		l'humain.
		"""
		graphical.draw_make_guess(window, WIDTH, ARROW, BG_COLOUR,
								  BUTTON_COLOR, TEXT_FONT,
								  self.mouse_on_return, self.m_on_tiret_mg,
								  self.m_on_propose, self.m_on_oui_mkg,
								  self.m_on_non_mkg, self.m_on_conf_mkg,
								  self.length, self.choiced, self.recenter,
								  self.representation, self.etat,
								  self.propose, self.one_possible,
								  self.is_letter, self.possibles,
								  self.selected, self.center_propos,
								  self.show_is_there, self.must_do_some,
								  self.health, self.no_possible,
								  self.result_mg)

	def draw_2_player(self, window):
		"""
		Function pour afficher l'écran de jeu en mode deux joueurs (humains).
		"""
		graphical.draw_2_player(window, WIDTH, ARROW, BG_COLOUR,
								BUTTON_COLOR, TEXT_FONT, RESULT_FONT,
								POSITIONS, LETTERS,
								self.mouse_on_return, self.m_on_letters,
								self.m_on_oui_mkg, self.m_on_non_mkg,
								self.m_on_conf_mkg, self.m_on_propose,
								self.m_on_tiret_mg,
								self.health, self.length, self.choiced,
								self.recenter, self.representation, self.step,
								self.clavier, self.choice_letter,
								self.is_letter, self.possibles,
								self.selected, self.center_propos, self.etat,
								self.result_mg, self.vict_1, self.vict_2,
								self.defai_1, self.defai_2, self.turn)


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

				elif game.initialized&(not game.start_g)&(not game.start_m)&(not game.start_2p):
					if game.mouse_on_return:
						game.re_init_accueil()

					elif game.make_guess:
						game.update_init_make_guess()

					elif game.guess:
						game.update_init_guess()

					elif game.two_player:
						game.update_init_2_player()

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

				elif game.initialized & game.start_2p:
					if game.mouse_on_return:
						game.re_init_2_player()
					else:
						game.make_guess_human()

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

			elif game.two_player:
				if game.start_2p:
					game.mouse_return_on()
					game.mouse_on_letters_mg()
					game.mouse_on_repsonse()
					game.mouse_on_propose()
					game.mouse_on_letters()
					game.draw_2_player(WIN)
					if game.result_mg != None:
						pygame.time.wait(4000)
						game.re_init_2_player()

				else:
					game.mouse_on_player()
					game.mouse_on_start_mg()
					game.mouse_on_pm_up()
					game.mouse_return_on()
					game.mouse_on_tirets_mg()
					game.draw_init_2_player(WIN)

			else:
				raise ValueError(
					'guess, make_guess or two_player should be True !')

		else:
			game.draw_init(WIN)
			game.mouse_mode_on()

	pygame.quit()

if __name__ == '__main__':
	main()
