"""
Script for the actions for the game.
"""

import numpy as np
import pygame

pygame.init()

def choice_mode(width, mouse_on_guess, mouse_on_m_guess, mouse_on_2_player,
				guess, make_guess, two_player, initialized, length, choiced,
				representation, etat, recenter):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	d'un des deux bouttons du choix du type de jeu lors du clique.
	"""
	if mouse_on_guess:
		guess = True
		make_guess = False
		two_player = False
		initialized = True
		pygame.time.wait(400)

	if mouse_on_m_guess:
		choiced = '_'*length
		representation = np.zeros(length, dtype=bool)
		etat = np.zeros(length) -1
		recenter = width/2-30*length/2
		guess = False
		make_guess = True
		two_player = False
		initialized = True
		pygame.time.wait(400)

	if mouse_on_2_player:
		choiced = '_'*length
		representation = np.zeros(length, dtype=bool)
		etat = np.zeros(length) -1
		recenter = width/2-30*length/2
		guess = False
		make_guess = False
		two_player = True
		initialized = True
		pygame.time.wait(400)

	return (guess, make_guess, two_player, initialized, choiced,
			representation, etat, recenter)

def draw_word(data, length_limits, tirets):
	"""
	Fonction pour tirer aléatoirement un mot répondant aux
	caractéristiques données par l'utilisateur.
	"""
	mots = np.copy(data['mots'])
	tire = np.copy(data['rec_map'][:, 0])
	mask = (data['longueur'] >= length_limits[0])&(
			data['longueur'] <= length_limits[1])

	mots = mots[mask]
	tire = tire[mask]
	if tirets == False:
		mots = mots[tire == 0]

	choiced = mots[np.random.randint(0, len(mots))]
	return choiced

def update_init_guess(width, data, mouse_on_cr_up, mouse_on_mi_up,
					  mouse_on_cr_dw, mouse_on_mi_dw, m_on_tiret_t,
					  m_on_tiret_f, m_on_start_g, length_limits, tirets,
					  choiced, start_g, length, representation, recenter,
					  show_must_choice_tiret):
	"""
	Fonction pour détecter quelles intéractions sont faîtes sur les
	caractéristiques du mot qui sera deviné par l'humain.
	"""
	if mouse_on_cr_up:
		if length_limits[0] < length_limits[1]:
			length_limits[0] += 1

	elif mouse_on_mi_up:
		if length_limits[0] > 1:
			length_limits[0] -= 1

	elif mouse_on_cr_dw:
		if length_limits[1] < 25:
			length_limits[1] += 1

	elif mouse_on_mi_dw:
		if length_limits[0] < length_limits[1]:
			length_limits[1] -= 1

	elif m_on_tiret_t:
		tirets = True
		show_must_choice_tiret = False

	elif m_on_tiret_f:
		tirets = False
		show_must_choice_tiret = False

	elif m_on_start_g:
		if type(tirets) == bool:
			start_g = True
			choiced = draw_word(data, length_limits, tirets)

			length = len(choiced)
			representation = np.zeros(length, dtype=bool)
			recenter = width/2-30*length/2
		else:
			show_must_choice_tiret = True

	return (length_limits, tirets, choiced, start_g, length, representation,
			recenter, show_must_choice_tiret)

def update_init_2_player(width,
						 mouse_on_cr_up, mouse_on_mi_up, m_on_tiret_mg,
						 mouse_on_p1, mouse_on_p2, m_on_start_m,
						 length, choiced, representation, etat, profil,
						 recenter, show_no_word, num_tirets, turn, start_2p,
						 step):
	"""
	Fonction d'intéraction de l'humain pour choisir les caractéristiques
	mot qu'il fera deviner à l'autre humain.	
	"""
	if mouse_on_cr_up:
		if length < 25:
			length += 1
			choiced += '_'
			representation = np.append(representation, False)
			etat = np.append(etat, -1)
			profil = np.append(profil, 0)
			recenter = width/2-30*length/2
			show_no_word = False

	elif mouse_on_mi_up:
		if length > 1:
			length -= 1
			choiced = choiced[:-1]
			representation = representation[:-1]
			etat = etat[:-1]
			profil = profil[:-1]
			recenter = width/2-30*length/2
			show_no_word = False

	elif type(m_on_tiret_mg) == np.ndarray:
		if True in m_on_tiret_mg:
			#transform : true de _ en - & self.transformation et inversement
			if representation[m_on_tiret_mg][0]:
				representation[m_on_tiret_mg] = False
				profil[m_on_tiret_mg] = 0
				choiced = np.array(list(choiced), dtype='O')
				choiced[m_on_tiret_mg] = '_'
				etat[m_on_tiret_mg] = -1
				choiced = np.sum(choiced)
				num_tirets -= 1
				show_no_word = False

			else:
				representation[m_on_tiret_mg] = True
				profil[m_on_tiret_mg] = 1
				choiced = np.array(list(choiced), dtype='O')
				choiced[m_on_tiret_mg] = '-'
				etat[m_on_tiret_mg] = 1
				choiced = np.sum(choiced)
				num_tirets += 1
				show_no_word = False

	if mouse_on_p1:
		turn = 1

	elif mouse_on_p2:
		turn = 2

	if m_on_start_m and (turn is not None):
		start_2p = True
		step = 'g'

	return (choiced, representation, etat, profil, recenter, show_no_word,
			num_tirets, turn, start_2p, step, length)

def is_possible_start_mg(data, length, num_tirets, profil):
	"""
	Fonction pour voir si il y a au moins un mots répondant aux
	caractéristiques données par l'utilisateur.
	"""
	mapp = np.copy(data['map'])[:, :length]
	rec_mapp = np.copy(data['rec_map'])
	caracteres = np.copy(data['caracteres'])
	mask = data['longueur'] == length
	mapp = mapp[mask]
	rec_mapp = rec_mapp[mask]
	if num_tirets > 0:
		mask = rec_mapp[:, 0] == num_tirets
		mapp = mapp[mask]
		rec_mapp = rec_mapp[mask]
		known = len(profil[profil != 0])
		perf = mapp == profil
		occur = np.sum(perf, axis=1)
		mask = occur == known
		mapp = mapp[mask]
		rec_mapp = rec_mapp[mask]

	else:
		mask = rec_mapp[:, 0] == 0
		mapp = mapp[mask]
		rec_mapp = rec_mapp[mask]

	mapp = np.copy(mapp)
	rec_mapp = np.copy(rec_mapp)
	can_start_m = len(rec_mapp) > 0
	return mapp, rec_mapp, can_start_m

def update_init_make_guess(data, width,
						   mouse_on_cr_up, mouse_on_mi_up, m_on_tiret_mg,
						   m_on_start_m,
						   length, choiced, representation, etat, profil,
						   recenter, show_no_word, num_tirets, start_m,
						   can_start_m, mapp, rec_mapp):
	"""
	Fonction d'intéraction de l'humain pour choisir les caractéristiques
	mot qu'il fera deviner à l'ordinateur.	
	"""
	if mouse_on_cr_up:
		if length < 25:
			length += 1
			choiced += '_'
			representation = np.append(representation, False)
			etat = np.append(etat, -1)
			profil = np.append(profil, 0)
			recenter = width/2-30*length/2
			show_no_word = False

	elif mouse_on_mi_up:
		if length > 1:
			length -= 1
			choiced = choiced[:-1]
			representation = representation[:-1]
			etat = etat[:-1]
			profil = profil[:-1]
			recenter = width/2-30*length/2
			show_no_word = False

	elif True in m_on_tiret_mg:
		#transform : true de _ en - & self.transformation et inversement
		if representation[m_on_tiret_mg][0]:
			representation[m_on_tiret_mg] = False
			profil[m_on_tiret_mg] = 0
			choiced = np.array(list(choiced), dtype='O')
			choiced[m_on_tiret_mg] = '_'
			etat[m_on_tiret_mg] = -1
			choiced = np.sum(choiced)
			num_tirets -= 1
			show_no_word = False

		else:
			representation[m_on_tiret_mg] = True
			profil[m_on_tiret_mg] = 1
			choiced = np.array(list(choiced), dtype='O')
			choiced[m_on_tiret_mg] = '-'
			etat[m_on_tiret_mg] = 1
			choiced = np.sum(choiced)
			num_tirets += 1
			show_no_word = False

	if m_on_start_m:
		if num_tirets == 0:
			start_m = True
			show_no_word = False
			mapp, rec_mapp, can_start_m = is_possible_start_mg(data, length,
															   num_tirets,
															   profil)

		else:
			mapp, rec_mapp, can_start_m = is_possible_start_mg(data, length,
															   num_tirets,
															   profil)

			if can_start_m:
				start_m = True
				show_no_word = False
			else:
				show_no_word = True

	return (length, choiced, representation, etat, profil, show_no_word,
			num_tirets, start_m, mapp, rec_mapp, can_start_m, recenter)

def update_from_answer(mapp, is_letter, choiced, possibles, data):
	"""
	Fonction pour enlever les mots ne répondant pas aux caractéristiques
	connues.
	"""
	sub_map = np.copy(mapp)
	if is_letter:
		for i in range(len(choiced)):
			if choiced[i] != '_':
				numb = np.where(data['caracteres'] == choiced[i])[0][0]+1
				sub_map = sub_map[sub_map[:, i] == numb]

			else:
				for j in range(len(possibles)):
					numb = np.where(data['caracteres'] == possibles[j])[0][0]+1
					sub_map = sub_map[sub_map[:, i] != numb]

	else:
		for i in range(len(possibles)):
			numb = np.where(data['caracteres'] == possibles[i])[0][0]+1
			sub_map = sub_map[np.sum(sub_map == numb, axis=1) == 0]

	mapp = np.copy(sub_map)
	return mapp

def guess_victory(health, representation, length, result_g):
	"""
	Fonction pour détecter si l'humain a réussis (gagné) ou non (perdu) à
	trouver le mot choisit par l'ordinateur.
	"""
	if health <= 0:
		result_g = 'p'
	else:
		if np.sum(representation) == length:
			result_g = 'v'

	return result_g

def choice_letter_guess(m_on_letters, health, choice_letter,
						tested_letters, show_alredy_tryed, choiced, a_like,
						c_like, e_like, i_like, o_like, u_like,
						representation, clavier,
						positions, letters):
	"""
	Fonction d'interaction de l'humain pour choisir quelle lettre
	"minimale" choisir.

	Parameters
	----------
	m_on_letters : list, audessus de quelle lettre est la souris.
	health : int, points de vie.
	choice_letter : lettre choisit.
	tested_letters : lettres déjà testé.
	show_alredy_tryed : afficher : "lettres déjà testé".
	choiced : str, mot à trouver.
	a_like : list.
	c_like : list.
	e_like : list.
	i_like : list.
	o_like : list.
	u_like : list.
	representation : TYPE
		DESCRIPTION.
	clavier : TYPE
		DESCRIPTION.
	positions : TYPE
		DESCRIPTION.
	letters : TYPE
		DESCRIPTION.

	Returns
	-------
	health : int, nmobre de points de vie.
	choice_letter : str, lettre choisit.
	tested_letters : list, liste des lettres déjà testé.
	show_alredy_tryed : bool, si le message : "lettre déjà essayé".
	representation : list, liste des emplacements du mot dont les lettres ont
		été trouvées.
	clavier : list, par emplacement du clavier (0 = lettre pas essayer, 
		1 = lettre correcte, -1 = lettre incorecte).

	"""
	if (np.sum(m_on_letters) > 0)&(health > 0):
		choice_letter = letters[m_on_letters][0]
		if choice_letter in tested_letters:
			choice_letter = None
			show_alredy_tryed = True
		else:
			show_alredy_tryed = False
			tested_letters.append(choice_letter)
			not_in = True
			for i, w in enumerate(choiced):
				if w in a_like:
					w = 'a'
				elif w in c_like:
					w = 'c'
				elif w in e_like:
					w = 'e'
				elif w in i_like:
					w = 'i'
				elif w in o_like:
					w = 'o'
				elif w in u_like:
					w = 'u'

				if w == choice_letter:
					representation[i] = True
					not_in = False

			if not_in:
				health -= 1
				clavier[letters == choice_letter] = -1
			else:
				clavier[letters == choice_letter] = 1

	return (health, choice_letter, tested_letters, show_alredy_tryed,
			representation, clavier)

def make_guess_response(data, width, link_dico, m_on_conf_mkg,
						show_is_there, must_do_some, m_on_oui_mkg,
						m_on_non_mkg, m_on_propose, m_on_tiret_mg,
						propose, is_letter, etat, one_possible, no_possible,
						length, result_mg, choiced, representation, health,
						selected, possibles, center_propos, mapp):
	"""
	Fonction d'interaction de l'humain pour répondre aux propositions de
	l'ordinateur.
	"""
	if propose != None:
		if m_on_conf_mkg & (type(is_letter) == bool):
			show_is_there = False
			if is_letter:
				if (0 in etat)&(one_possible == False):
					etat[etat == 0] = 1
					must_do_some = False
					if len(etat[etat == 1]) == length:
						result_mg = 'v'
					else:
						mapp = update_from_answer(mapp, is_letter, choiced,
												  possibles, data)

						if no_possible == False:
							(no_possible, health, result_mg, one_possible,
							 propose, possibles, center_propos, m_on_propose,
							 selected) = whats_best(data, mapp, no_possible,
								health, result_mg, one_possible, propose,
								choiced, link_dico, width, representation,
								center_propos, possibles, m_on_propose,
								selected)

							is_letter = None

				elif one_possible:
					choiced = propose
					representation[:] = True
					etat[:] = 1
					must_do_some = False
					result_mg = 'v'

				else:
					must_do_some = True

			else:
				health -= 1
				if health == 0:
					result_mg = 'p'

				elif one_possible:
					health = 0
					result_mg = 'p'
					no_possible = True

				else:
					mapp = update_from_answer(mapp, is_letter, choiced,
											  possibles, data)

					(no_possible, health, result_mg, one_possible, propose,
					 possibles, center_propos, m_on_propose, selected
					 ) = whats_best(
						data, mapp, no_possible, health, result_mg,
						one_possible, propose, choiced, link_dico, width,
						representation, center_propos, possibles,
						m_on_propose, selected)

					is_letter = None

		elif m_on_conf_mkg & (type(is_letter) != bool):
			show_is_there = True

		elif m_on_oui_mkg:
			is_letter = True
			show_is_there = False
			must_do_some = False

		elif m_on_non_mkg:
			is_letter = False
			show_is_there = False
			choiced = np.array(list(choiced), dtype=object)
			choiced[etat == 0] = '_'
			choiced = np.sum(choiced)
			representation[etat == 0] = False
			etat[etat == 0] = -1
			must_do_some = False

		elif is_letter:
			if True in m_on_propose:
				selected = m_on_propose*1 + selected*2
				selected[selected > 1] = 0
				selected = selected.astype(bool)
				must_do_some = False

			else:
				if True in m_on_tiret_mg:
					if etat[m_on_tiret_mg] == 1:
						pass

					elif True in selected:
						etat[m_on_tiret_mg] = 0
						representation[m_on_tiret_mg] = True
						choiced = np.array(list(choiced), dtype=object)
						choiced[m_on_tiret_mg] = possibles[selected]
						choiced = np.sum(choiced)
						must_do_some = False

					else:
						etat[m_on_tiret_mg] = -1
						representation[m_on_tiret_mg] = False
						choiced = np.array(list(choiced), dtype=object)
						choiced[m_on_tiret_mg] = '_'
						choiced = np.sum(choiced)

	return (is_letter, show_is_there, etat, must_do_some, result_mg,
			no_possible, choiced, representation, health, selected,
			m_on_propose, possibles, center_propos, propose, one_possible,
			mapp)

def make_guess_human(width, positions, letters,
					 m_on_letters, m_on_oui_mkg, m_on_non_mkg, m_on_conf_mkg,
					 m_on_tiret_mg, m_on_propose,
					 step, health, vict_1, vict_2, defai_1, defai_2,
					 representation, clavier, is_letter, choice_letter,
					 tested_letters, choiced, etat, link_dico, propose,
					 possibles, center_propos, selected, length, result_mg,
					 turn,
					 a_like, c_like, e_like, i_like, o_like, u_like):

	# setp (g=guess, e=examine)
	if step == 'g':
		if (np.sum(m_on_letters) > 0)&(health > 0):
			choice_letter = letters[m_on_letters][0]
			if choice_letter not in tested_letters:
				tested_letters.append(choice_letter)
				step = 'e'
			else:
				choice_letter = None

	if step == 'e':
		if m_on_oui_mkg:
			(possibles, center_propos, m_on_propose, selected
			 ) = get_linked_letters(link_dico, choice_letter, width)
			is_letter = True

		elif m_on_non_mkg:
			is_letter = False
			choiced = np.array(list(choiced), dtype=object)
			choiced[etat == 0] = '_'
			choiced = np.sum(choiced)
			representation[etat == 0] = False
			etat[etat == 0] = -1

		elif m_on_conf_mkg & (type(is_letter) == bool):
			if is_letter & (0. in etat):
				step = 'g'
				is_letter = None
				clavier[letters == choice_letter] = 1
				if 0 in etat:
					etat[etat == 0] = 1
					if len(etat[etat == 1]) == length:
						result_mg = 'v'
					if turn == 1:
						vict_1 = vict_1 + 1
					else:
						vict_2 = vict_2 + 1

			elif not is_letter:
				step = 'g'
				is_letter = None
				clavier[letters == choice_letter] = -1
				health -= 1
				if health == 0:
					result_mg = 'p'
					if turn == 1:
						defai_1 = defai_1 + 1
					else:
						defai_2 = defai_2 + 1

		elif type(is_letter) == bool:
			if is_letter:
				if True in m_on_propose:
					selected = m_on_propose*1 + selected*2
					selected[selected > 1] = 0
					selected = selected.astype(bool)

				else:
					if True in m_on_tiret_mg:
						if etat[m_on_tiret_mg] == 1:
							pass

						elif True in selected:
							etat[m_on_tiret_mg] = 0
							representation[m_on_tiret_mg] = True
							choiced = np.array(list(choiced), dtype=object)
							choiced[m_on_tiret_mg] = possibles[selected]
							choiced = np.sum(choiced)

						else:
							etat[m_on_tiret_mg] = -1
							representation[m_on_tiret_mg] = False
							choiced = np.array(list(choiced), dtype=object)
							choiced[m_on_tiret_mg] = '_'
							choiced = np.sum(choiced)

	return (step, health, vict_1, vict_2, defai_1, defai_2,
			choice_letter, tested_letters, choiced, is_letter, etat,
			representation, clavier, possibles, center_propos, m_on_propose,
			selected, result_mg)


def get_linked_letters(link_dico, propose, width):
	"""
	Fonction pour extraire les caractères associées à la lettre "minimale"
	choisit par la fonction 'whats_best'
	"""
	possibles = np.array(link_dico[propose])
	num_p = len(possibles)
	center_propos = width/2 + (np.arange(num_p)-num_p/2)*60
	m_on_propose = np.zeros(num_p, dtype=bool)
	selected = np.zeros(num_p, dtype=bool)
	return possibles, center_propos, m_on_propose, selected

def whats_best(data, mapp, no_possible, health, result_mg, one_possible,
			   propose, choiced, link_dico, width, representation,
			   center_propos, possibles, m_on_propose, selected):
	"""
	Fonction pour chercher le meilleur caractère à utiliser pour trouver
	le mot choisit par l'humain. L'approche est baser sur la fréquence d'
	apparition de chaque lettre "minimale".
	"""
	sub_map = np.copy(mapp)
	if len(sub_map) == 0:
		no_possible = True # No possible word from the data
		health = 0
		result_mg = 'p'

	elif len(sub_map) == 1:
		one_possible = True
		mot = np.sum(data['caracteres'][sub_map[0]-1].astype(object))
		propose = mot

	elif sub_map.shape[0] > 2:
		m_equal = data['caracteres'] == np.array(list(choiced))[:, np.newaxis]
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
			propose = data['caracteres'][maxi]
			(possibles, center_propos, m_on_propose,
			 selected) = get_linked_letters(link_dico, propose, width)

		else:
			sub_map = sub_map[:, representation == False]
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
			propose = data['caracteres'][maxi]
			(possibles, center_propos, m_on_propose,
			 selected) = get_linked_letters(link_dico, propose, width)

	elif sub_map.shape[0] == 2:
		differ = (sub_map[0] != sub_map[1])&(representation == False)
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
		propose = data['caracteres'][maxi]
		(possibles, center_propos, m_on_propose,
		 selected) = get_linked_letters(link_dico, propose, width)

	return (no_possible, health, result_mg, one_possible, propose, possibles,
			center_propos, m_on_propose, selected)

def mouse_mode_on(mouse_pos):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	d'un des deux bouttons du choix du type de jeu.
	"""
	if (mouse_pos[0] >= 129.4)&(mouse_pos[1] >= 282.95)&(
		mouse_pos[0] <= 669.6)&(mouse_pos[1] <= 317.05):
		mouse_on_guess = True
	else:
		mouse_on_guess = False

	if (mouse_pos[0] >= 155.8)&(mouse_pos[1] >= 383.5)&(
		mouse_pos[0] <= 644.2)&(mouse_pos[1] <= 416.5):
		mouse_on_m_guess = True
	else:
		mouse_on_m_guess = False

	if (mouse_pos[0] >= 286)&(mouse_pos[1] >= 482)&(
		mouse_pos[0] <= 513)&(mouse_pos[1] <= 518):
		mouse_on_2_player = True
	else:
		mouse_on_2_player = False

	return mouse_on_guess, mouse_on_m_guess, mouse_on_2_player

def mouse_return_on(mouse_pos, head, arrow, pi2):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	de la flêche permettant de revenir au menu précédant.
	"""
	mouse_p_arr = np.array(mouse_pos)
	vect = mouse_p_arr-head
	norm = np.sum(vect**2, 1)**0.5
	prod = np.sum(vect[[0, 0, 1]]*vect[[1, 2, 2]], 1)
	theta = round(np.sum(np.arccos(
					prod/(norm[[0, 0, 1]]*norm[[1, 2, 2]]))), 6)

	if (mouse_pos[0] >= arrow[2, 0])&(mouse_pos[1] >= arrow[4, 1])&(
			mouse_pos[0] <= arrow[4, 0])&(mouse_pos[1] <= arrow[2, 1]):
		mouse_on_return = True

	elif theta == pi2:
		mouse_on_return = True
	else:
		mouse_on_return = False

	return mouse_on_return

def mouse_on_pm_up(mouse_pos, width):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	des boutons servant à faire varier la valeur de la borne minimal du
	nombre de caractères d'un mot.
	"""
	if (mouse_pos[0] >= width/4-25)&(mouse_pos[1] >= 175)&(
		mouse_pos[0] <= width/4+25)&(mouse_pos[1] <= 225):
		mouse_on_cr_up = True
	else:
		mouse_on_cr_up = False

	if (mouse_pos[0] >= width*3/4-25)&(mouse_pos[1] >= 175)&(
		mouse_pos[0] <= width*3/4+25)&(mouse_pos[1] <= 225):
		mouse_on_mi_up = True
	else:
		mouse_on_mi_up = False

	return mouse_on_cr_up, mouse_on_mi_up

def mouse_on_pm_down(mouse_pos, width):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	des boutons servant à faire varier la valeur de la borne maximal du
	nombre de caractères d'un mot.
	"""
	if (mouse_pos[0] >= width/4-25)&(mouse_pos[1] >= 300)&(
		mouse_pos[0] <= width/4+25)&(mouse_pos[1] <= 350):
		mouse_on_cr_dw = True
	else:
		mouse_on_cr_dw = False

	if (mouse_pos[0] >= width*3/4-25)&(mouse_pos[1] >= 300)&(
		mouse_pos[0] <= width*3/4+25)&(mouse_pos[1] <= 350):
		mouse_on_mi_dw = True
	else:
		mouse_on_mi_dw = False

	return mouse_on_cr_dw, mouse_on_mi_dw

def mouse_on_tirets_guess(mouse_pos, width):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	boutons pour la sélection de la présence ou non de tiret(s) dans le
	mot que devra deviner l'humain.
	"""
	if (mouse_pos[0] >= width/4-50)&(mouse_pos[1] >= 425)&(
		mouse_pos[0] <= width/4+50)&(mouse_pos[1] <= 475):
		m_on_tiret_t = True
	else:
		m_on_tiret_t = False

	if (mouse_pos[0] >= width*3/4-50)&(mouse_pos[1] >= 425)&(
		mouse_pos[0] <= width*3/4+50)&(mouse_pos[1] <= 475):
		m_on_tiret_f = True
	else:
		m_on_tiret_f = False

	return m_on_tiret_t, m_on_tiret_f

def mouse_on_tirets_mg(mouse_pos, length, recenter):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	des caractères pouvant être transformé de lettre à tiret ou
	inversement.
	"""
	if (mouse_pos[1] >= 365)&(mouse_pos[1] <= 410):
		cells_dx = np.arange(length)*30+recenter
		mx = (mouse_pos[0] >= cells_dx)&(
			  mouse_pos[0] <= cells_dx+25)

		m_on_tiret_mg = mx
	else:
		m_on_tiret_mg = np.zeros(length, dtype=bool)

	return m_on_tiret_mg

def mouse_on_start_guess(mouse_pos, width):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	du bouton pour lancer une partie où l'humain doit trouver un mot.
	"""
	if (mouse_pos[0] >= width/2-100)&(mouse_pos[1] >= 500)&(
		mouse_pos[0] <= width/2+100)&(mouse_pos[1] <= 550):
		m_on_start_g = True
	else:
		m_on_start_g = False

	return m_on_start_g

def mouse_on_letters(mouse_pos, positions):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	d'une des lettres du clavier.
	"""
	mx = (mouse_pos[0] >= positions[:, 0])&(
		  mouse_pos[0] <= positions[:, 0]+50)

	my = (mouse_pos[1] >= positions[:, 1])&(
		  mouse_pos[1] <= positions[:, 1]+50)

	m_on_letters = mx&my

	return m_on_letters

def mouse_on_start_mg(mouse_pos, width):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	du bouton pour lancer une partie où l'ordinateur doit trouver le mot
	choisit par l'humain.
	"""
	if (mouse_pos[0] >= width/2-100)&(mouse_pos[1] >= 450)&(
		mouse_pos[0] <= width/2+100)&(mouse_pos[1] <= 500):
		m_on_start_m = True
	else:
		m_on_start_m = False

	return m_on_start_m

def mouse_on_repsonse(mouse_pos):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	des boutons oui/non/confirmer lors-ce-que c'est à l'ordinateur de
	trouver le mot choisit par l'humain.
	"""
	if (mouse_pos[0] >= 50)&(mouse_pos[1] >= 150)&(
		mouse_pos[0] <= 150)&(mouse_pos[1] <= 200):
		m_on_oui_mkg = True
	else:
		m_on_oui_mkg = False
	
	if (mouse_pos[0] >= 200)&(mouse_pos[1] >= 150)&(
		mouse_pos[0] <= 300)&(mouse_pos[1] <= 200):
		m_on_non_mkg = True
	else:
		m_on_non_mkg = False

	if (mouse_pos[0] >= 100)&(mouse_pos[1] >= 225)&(
		mouse_pos[0] <= 250)&(mouse_pos[1] <= 275):
		m_on_conf_mkg = True
	else:
		m_on_conf_mkg = False

	return m_on_oui_mkg, m_on_non_mkg, m_on_conf_mkg

def mouse_on_propose(mouse_pos, is_letter, center_propos, m_on_propose):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	d'un des caractères associé à une lettre "minimale".
	"""
	if type(is_letter) == bool:
		if is_letter:
			if (mouse_pos[1] >= 400)&(mouse_pos[1] <= 450):
				m_on_propose = (mouse_pos[0] >= center_propos)&(
								mouse_pos[0] <= center_propos+50)

			else:
				m_on_propose[:] = False

	return m_on_propose

def mouse_on_letters_mg(mouse_pos, length, recenter):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	des caractères pouvant être transformé de lettre à tiret ou
	inversement.
	"""
	if (mouse_pos[1] >= 315)&(mouse_pos[1] <= 355):
		cells_dx = np.arange(length)*30+recenter
		mx = (mouse_pos[0] >= cells_dx)&(
			  mouse_pos[0] <= cells_dx+25)

		m_on_tiret_mg = mx

	else:
		m_on_tiret_mg = np.zeros(length, dtype=bool)

	return m_on_tiret_mg

def mouse_on_player(mouse_pos):
	"""
	Fonction pour détecter si le curseur de la souris se trouve au-dessus
	des boutons de selection du joueur qui devra deviner / faire deviner un
	mot à l'autre joueur.
	"""
	if (mouse_pos[0] >= 191.6)&(mouse_pos[1] >= 525)&(
		mouse_pos[0] <= 341.7)&(mouse_pos[1] <= 575):
		m_on_p1 = True
	else:
		m_on_p1 = False
	
	if (mouse_pos[0] >= 458.3)&(mouse_pos[1] >= 525)&(
		mouse_pos[0] <= 608.4)&(mouse_pos[1] <= 575):
		m_on_p2 = True
	else:
		m_on_p2 = False

	return m_on_p1, m_on_p2
	
