import numpy as np
import pygame

pygame.init()


def draw_init(window, bg_colour, width, title_font, text_font, button_color,
			  mouse_on_guess, mouse_on_m_guess, mouse_on_2_player):
	"""
	Fonction pour afficher l'écrant d'acceuil.
	"""
	window.fill(bg_colour)
	title = title_font.render('Bienvenue dans le jeu du pendu !', 1, 'black')
	window.blit(title, (width/2-title.get_width()/2, 100-title.get_height()/2))
	mode = text_font.render('Quel mode voulez-vous tester ?', 1, 'black')
	window.blit(mode, (width/2-mode.get_width()/2, 200-mode.get_height()/2))

	mode_guess = text_font.render("Deviner un mot choisit par l'ordinateur",
								  1, 'black')

	pygame.draw.rect(window, button_color,
					   (width/2-mode_guess.get_width()*0.55,
						300-mode_guess.get_height()*0.55,
						mode_guess.get_width()*1.1,
						mode_guess.get_height()*1.1))

	if mouse_on_guess:
		pygame.draw.rect(window, (0, 0, 0),
						 (width/2-mode_guess.get_width()*0.55,
						 300-mode_guess.get_height()*0.55,
						 mode_guess.get_width()*1.1,
						 mode_guess.get_height()*1.1), 3)

	window.blit(mode_guess, (width/2-mode_guess.get_width()/2,
							 300-mode_guess.get_height()/2))

	mode_make_guess = text_font.render("Faire deviner un mot à l'ordinateur",
										1, 'black')

	pygame.draw.rect(window, button_color,
					 (width/2-mode_make_guess.get_width()*0.55,
					  400-mode_make_guess.get_height()*0.55,
					  mode_make_guess.get_width()*1.1,
					  mode_make_guess.get_height()*1.1))

	if mouse_on_m_guess:
		pygame.draw.rect(window, (0, 0, 0),
						 (width/2-mode_make_guess.get_width()*0.55,
						  400-mode_make_guess.get_height()*0.55,
						  mode_make_guess.get_width()*1.1,
						  mode_make_guess.get_height()*1.1), 3)

	window.blit(mode_make_guess, (width/2-mode_make_guess.get_width()/2,
								  400-mode_make_guess.get_height()/2))

	mode_2ply_guess = text_font.render("Mode 2 joueurs", 1, 'black')
	pygame.draw.rect(window, button_color,
					   (width/2-mode_2ply_guess.get_width()*0.55,
						500-mode_2ply_guess.get_height()*0.55,
						mode_2ply_guess.get_width()*1.1,
						mode_2ply_guess.get_height()*1.1))

	if mouse_on_2_player:
		pygame.draw.rect(window, (0, 0, 0),
							(width/2-mode_2ply_guess.get_width()*0.55,
							500-mode_2ply_guess.get_height()*0.55,
							mode_2ply_guess.get_width()*1.1,
							mode_2ply_guess.get_height()*1.1), 3)

	window.blit(mode_2ply_guess, (width/2-mode_2ply_guess.get_width()/2,
								  500-mode_2ply_guess.get_height()/2))

	pygame.display.update()

	pygame.display.update()

def draw_init_guess(window, bg_colour, width, text_font, button_color,
					arrow, cross_up, cross_dw, mouse_on_return,
					mouse_on_cr_up, mouse_on_mi_up, mouse_on_cr_dw,
					mouse_on_mi_dw, m_on_tiret_t, m_on_tiret_f, m_on_start_g,
					length_limits, tirets, show_must_choice_tiret):
	"""
	Fonction pour afficher l'écrant du choix des caractéristiques du mot
	tiré par l'ordinateur.
	"""
	window.fill(bg_colour)
	pygame.draw.polygon(window, button_color, arrow)
	if mouse_on_return:
		pygame.draw.polygon(window, (0, 0, 0), arrow, 3)

	mode = text_font.render("Mode choisit : deviner un mot choisit par l'ordinateur",
							  1, 'black')
	window.blit(mode, (width/2-mode.get_width()/2, 100-mode.get_height()/2))

	min_tx = text_font.render('Nombre minimum de caracteres (tirets inclus)',
								1, 'black')
	window.blit(min_tx, (width/2-min_tx.get_width()/2,
						 150-min_tx.get_height()/2))

	pygame.draw.rect(window, button_color, (width/4-25, 175, 50, 50))
	pygame.draw.polygon(window, (0, 0, 0), cross_up)
	if mouse_on_cr_up:
		pygame.draw.rect(window, (0, 0, 0), (width/4-25, 175, 50, 50), 3)

	numlw_txt = text_font.render(str(length_limits[0]), 1, 'black')
	pygame.draw.rect(window, (255, 250, 250), (width/2, 175, 50, 50))
	pygame.draw.rect(window, (0, 0, 0), (width/2, 175, 50, 50), 3)
	window.blit(numlw_txt, (width/2-numlw_txt.get_width()/2+25,
							175-numlw_txt.get_height()/2+25))

	pygame.draw.rect(window, button_color, (width*3/4-25, 175, 50, 50))
	pygame.draw.rect(window, (0, 0, 0), (width*3/4+10-25, 195, 30, 10))
	if mouse_on_mi_up:
		pygame.draw.rect(window, (0, 0, 0), (width*3/4-25, 175, 50, 50), 3)

	max_tx = text_font.render('nombre maximum de caracteres (tirets inclus)',
								1, 'black')
	window.blit(max_tx, (width/2-max_tx.get_width()/2,
						 275-max_tx.get_height()/2))

	pygame.draw.rect(window, button_color, (width/4-25, 300, 50, 50))
	pygame.draw.polygon(window, (0, 0, 0), cross_dw)
	if mouse_on_cr_dw:
		pygame.draw.rect(window, (0, 0, 0), (width/4-25, 300, 50, 50), 3)

	numup_txt = text_font.render(str(length_limits[1]), 1, 'black')
	pygame.draw.rect(window, (255, 250, 250), (width/2, 300, 50, 50))
	pygame.draw.rect(window, (0, 0, 0), (width/2, 300, 50, 50), 3)
	window.blit(numup_txt, (width/2-numup_txt.get_width()/2+25,
						  300-numup_txt.get_height()/2+25))

	pygame.draw.rect(window, button_color, (width*3/4-25, 300, 50, 50))
	pygame.draw.rect(window, (0, 0, 0), (width*3/4+10-25, 320, 30, 10))
	if mouse_on_mi_dw:
		pygame.draw.rect(window, (0, 0, 0), (width*3/4-25, 300, 50, 50), 3)

	tiret_tx = text_font.render("Il peut y avoir un (ou plusieurs) trait d'union",
								1, 'black')
	window.blit(tiret_tx, (width/2-tiret_tx.get_width()/2,
							400-tiret_tx.get_height()/2))

	if tirets:
		pygame.draw.rect(window, (0, 255, 0), (width/4-50, 425, 100, 50))
	else:
		pygame.draw.rect(window, button_color, (width/4-50, 425, 100, 50))

	if m_on_tiret_t:
		pygame.draw.rect(window, (0, 0, 0), (width/4-50, 425, 100, 50), 3)
	
	if tirets == False:
		pygame.draw.rect(window, (255, 0, 0), (width*3/4-50, 425, 100, 50))
	else:
		pygame.draw.rect(window, button_color, (width*3/4-50, 425, 100, 50))

	if m_on_tiret_f:
		pygame.draw.rect(window, (0, 0, 0), (width*3/4-50, 425, 100, 50), 3)

	o_tx = text_font.render("Oui", 1, 'black')
	window.blit(o_tx, (width/4-o_tx.get_width()/2,
						425-o_tx.get_height()/2+25))

	n_tx = text_font.render("Non", 1, 'black')
	window.blit(n_tx, (width*3/4-n_tx.get_width()/2,
						425-n_tx.get_height()/2+25))

	pygame.draw.rect(window, button_color, (width/2-100, 500, 200, 50))
	if m_on_start_g:
		pygame.draw.rect(window, (0, 0, 0), (width/2-100, 500, 200, 50), 3)

	st_tx = text_font.render("Commencer", 1, 'black')
	window.blit(st_tx, (width/2-st_tx.get_width()/2,
						500-st_tx.get_height()/2+25))

	if show_must_choice_tiret:
		mtir_tx_1 = text_font.render(
				"Vous devez indiquer si il est possible de tomber sur un",
				1, 'black')

		window.blit(mtir_tx_1, (width/2-mtir_tx_1.get_width()/2,
								615-mtir_tx_1.get_height()/2))

		must_tiret_tx_2 = text_font.render(
				"mot ayant un (ou plusieurs) trait d'union", 1, 'black')

		window.blit(must_tiret_tx_2, (width/2-must_tiret_tx_2.get_width()/2,
									  650-must_tiret_tx_2.get_height()/2))

	pygame.display.update()

def draw_init_make_guess(window, width, bg_colour, button_color, text_font,
						 arrow, cross_up, mouse_on_return, mouse_on_cr_up,
						 mouse_on_mi_up, m_on_tiret_mg, m_on_start_m, length,
						 choiced, recenter, show_no_word):
	"""
	Fonction pour afficher l'écrant du choix des caractéristiques du mot
	que l'ordinateur devra deviner.
	"""
	window.fill(bg_colour)
	pygame.draw.polygon(window, button_color, arrow)

	if mouse_on_return:
		pygame.draw.polygon(window, (0, 0, 0), arrow, 3)

	mode = text_font.render(
					"Mode choisit : faire deviner un mot à l'ordinateur",
					1, 'black')

	window.blit(mode, (width/2-mode.get_width()/2, 100-mode.get_height()/2))

	len_tx = text_font.render('Nombre de caracteres (tirets inclus)',
							  1, 'black')

	window.blit(len_tx, (width/2-len_tx.get_width()/2,
						 150-len_tx.get_height()/2))

	pygame.draw.rect(window, button_color, (width/4-25, 175, 50, 50))
	pygame.draw.polygon(window, (0, 0, 0), cross_up)
	if mouse_on_cr_up:
		pygame.draw.rect(window, (0, 0, 0), (width/4-25, 175, 50, 50), 3)

	numlw_txt = text_font.render(str(length), 1, 'black')
	pygame.draw.rect(window, (255, 250, 250), (width/2-25, 175, 50, 50))
	pygame.draw.rect(window, (0, 0, 0), (width/2-25, 175, 50, 50), 3)
	window.blit(numlw_txt, (width/2-numlw_txt.get_width()/2,
						  175-numlw_txt.get_height()/2+25))

	pygame.draw.rect(window, button_color, (width*3/4-25, 175, 50, 50))
	pygame.draw.rect(window, (0, 0, 0), (width*3/4-15, 195, 30, 10))
	if mouse_on_mi_up:
		pygame.draw.rect(window, (0, 0, 0), (width*3/4-25, 175, 50, 50), 3)

	tir1_tx = text_font.render(
			"Cliquez sur les cases où il y a un trait d'union (ignorer cette",
			1, 'black')

	window.blit(tir1_tx, (width/2-tir1_tx.get_width()/2,
						  265-tir1_tx.get_height()/2))

	tir2_tx = text_font.render("étape si il n'y en a pas dans votre mot)",
							   1, 'black')
	window.blit(tir2_tx, (width/2-tir2_tx.get_width()/2,
						  300-tir2_tx.get_height()/2))

	for i in range(length):
		if choiced[i] != '-':
			if m_on_tiret_mg[i]:
				pygame.draw.rect(window, (255, 0, 0),
								 (i*30+recenter, 400, 25, 5))
			else:
				pygame.draw.rect(window, (0, 0, 0),
								 (i*30+recenter, 400, 25, 5))
		else:
			if m_on_tiret_mg[i]:
				pygame.draw.rect(window, (255, 0, 0),
								 (i*30+recenter+2.5, 385, 20, 3))
			else:
				pygame.draw.rect(window, (0, 0, 0),
								 (i*30+recenter+2.5, 385, 20, 3))

	pygame.draw.rect(window, button_color, (width/2-100, 450, 200, 50))
	if m_on_start_m:
		pygame.draw.rect(window, (0, 0, 0), (width/2-100, 450, 200, 50), 3)

	st_tx = text_font.render('Commencer', 1, 'black')
	window.blit(st_tx, (width/2-st_tx.get_width()/2,
						450-st_tx.get_height()/2+25))

	if show_no_word:
		no_tx1 = text_font.render(
					"Je n'ai aucun mot dans ma base de données qui puisse",
					1, (0, 0, 0))
		window.blit(no_tx1, (width/2-no_tx1.get_width()/2,
							 525-no_tx1.get_height()/2+25))

		no_tx2 = text_font.render(
				  "corespondre aux caractéristiques entrées", 1, (0, 0, 0))
		window.blit(no_tx2, (width/2-no_tx2.get_width()/2,
							 550-no_tx2.get_height()/2+25))

	pygame.display.update()

def draw_init_2_player(window, width, bg_colour, button_color, arrow,
					   cross_up, text_font, mouse_on_return,
					   mouse_on_cr_up, mouse_on_mi_up, m_on_tiret_mg,
					   m_on_start_m, mouse_on_p1, mouse_on_p2,
					   length, choiced, recenter, turn, vict_1,
					   defai_1, vict_2, defai_2):
	"""
	Fonction pour afficher l'écrant du choix des caractéristiques du mot
	que l'autre humain devra deviner.
	"""
	window.fill(bg_colour)
	pygame.draw.polygon(window, button_color, arrow)

	if mouse_on_return:
		pygame.draw.polygon(window, (0, 0, 0), arrow, 3)

	mode = text_font.render(
					"Mode choisit : 2 joueurs (humain)",
					1, 'black')

	window.blit(mode, (width/2-mode.get_width()/2, 100-mode.get_height()/2))

	len_tx = text_font.render('Nombre de caracteres (tirets inclus)',
							  1, 'black')

	window.blit(len_tx, (width/2-len_tx.get_width()/2,
						 150-len_tx.get_height()/2))

	pygame.draw.rect(window, button_color, (width/4-25, 175, 50, 50))
	pygame.draw.polygon(window, (0, 0, 0), cross_up)
	if mouse_on_cr_up:
		pygame.draw.rect(window, (0, 0, 0), (width/4-25, 175, 50, 50), 3)

	numlw_txt = text_font.render(str(length), 1, 'black')
	pygame.draw.rect(window, (255, 250, 250), (width/2-25, 175, 50, 50))
	pygame.draw.rect(window, (0, 0, 0), (width/2-25, 175, 50, 50), 3)
	window.blit(numlw_txt, (width/2-numlw_txt.get_width()/2,
						  175-numlw_txt.get_height()/2+25))

	pygame.draw.rect(window, button_color, (width*3/4-25, 175, 50, 50))
	pygame.draw.rect(window, (0, 0, 0), (width*3/4-15, 195, 30, 10))
	if mouse_on_mi_up:
		pygame.draw.rect(window, (0, 0, 0), (width*3/4-25, 175, 50, 50), 3)

	tir1_tx = text_font.render(
			"Cliquez sur les cases où il y a un trait d'union (ignorer cette",
			1, 'black')

	window.blit(tir1_tx, (width/2-tir1_tx.get_width()/2,
						  265-tir1_tx.get_height()/2))

	tir2_tx = text_font.render("étape si il n'y en a pas dans votre mot)",
							   1, 'black')
	window.blit(tir2_tx, (width/2-tir2_tx.get_width()/2,
						  300-tir2_tx.get_height()/2))

	for i in range(length):
		if choiced[i] != '-':
			if m_on_tiret_mg[i]:
				pygame.draw.rect(window, (255, 0, 0),
								 (i*30+recenter, 400, 25, 5))
			else:
				pygame.draw.rect(window, (0, 0, 0),
								 (i*30+recenter, 400, 25, 5))
		else:
			if m_on_tiret_mg[i]:
				pygame.draw.rect(window, (255, 0, 0),
								 (i*30+recenter+2.5, 385, 20, 3))
			else:
				pygame.draw.rect(window, (0, 0, 0),
								 (i*30+recenter+2.5, 385, 20, 3))

	pygame.draw.rect(window, button_color, (width/2-100, 450, 200, 50))
	if m_on_start_m:
		pygame.draw.rect(window, (0, 0, 0), (width/2-100, 450, 200, 50), 3)

	st_tx = text_font.render('Commencer', 1, 'black')
	window.blit(st_tx, (width/2-st_tx.get_width()/2,
						450-st_tx.get_height()/2+25))

	tx = text_font.render('Joueur 1', 1, 'black')

	if turn == 1:
		pygame.draw.rect(window, (0, 0, 255), (width/3-75, 525, 150, 50))
	else:
		pygame.draw.rect(window, button_color, (width/3-75, 525, 150, 50))

	if mouse_on_p1:
		pygame.draw.rect(window, (0, 0, 0), (width/3-75, 525, 150, 50), 3)

	window.blit(tx, (width/3-tx.get_width()/2, 525-tx.get_height()/2+25))
	tx = text_font.render('Victoire : '+str(vict_1), 1, 'black')
	window.blit(tx, (width/3-tx.get_width()/2, 575-tx.get_height()/2+25))
	tx = text_font.render('Defaite : '+str(defai_1), 1, 'black')
	window.blit(tx, (width/3-tx.get_width()/2, 625-tx.get_height()/2+25))

	tx = text_font.render('Joueur 2', 1, 'black')

	if turn == 2:
		pygame.draw.rect(window, (0, 0, 255), (width*2/3-75, 525, 150, 50))
	else:
		pygame.draw.rect(window, button_color, (width*2/3-75, 525, 150, 50))

	if mouse_on_p2:
		pygame.draw.rect(window, (0, 0, 0), (width*2/3-75, 525, 150, 50), 3)

	window.blit(tx, (width*2/3-tx.get_width()/2, 525-tx.get_height()/2+25))
	tx = text_font.render('Victoire : '+str(vict_2), 1, 'black')
	window.blit(tx, (width*2/3-tx.get_width()/2, 575-tx.get_height()/2+25))
	tx = text_font.render('Defaite : '+str(defai_2), 1, 'black')
	window.blit(tx, (width*2/3-tx.get_width()/2, 625-tx.get_height()/2+25))

	pygame.display.update()


def draw_guess(window, width, bg_colour, button_color, text_font, result_font,
			   arrow, positions, letters, mouse_on_return, m_on_letters,
			   length, choiced, recenter, representation, clavier, health,
			   result_g, show_alredy_tryed):
	"""
	Fonction pour afficher l'écrant du choix des "minimale" lettres
	pouvant être choisit par l'humain pour chercher à trouver le mot tiré
	par l'ordinateur.
	"""
	window.fill(bg_colour)
	pygame.draw.polygon(window, button_color, arrow)
	if mouse_on_return:
		pygame.draw.polygon(window, (0, 0, 0), arrow, 3)

	for i in range(length):
		if choiced[i] != '-':
			pygame.draw.rect(window, (0, 0, 0),
							 (i*30+recenter, 400, 25, 5))
		else:
			pygame.draw.rect(window, (0, 0, 0),
							 (i*30+recenter+2.5, 385, 20, 3))

		if representation[i]:
			tx = text_font.render(str(choiced[i]), 1, 'black')
			window.blit(tx, (i*30+recenter-tx.get_width()/2+12.5, 365))
		elif health <= 0:
			tx = text_font.render(str(choiced[i]), 1, 'red')
			window.blit(tx, (i*30+recenter-tx.get_width()/2+12.5, 365))

	for i in range(26):
		if clavier[i] == -1:
			pygame.draw.rect(window, (255, 0, 0),
							 (positions[i, 0], positions[i, 1], 50, 50))
		elif clavier[i] == 1:
			pygame.draw.rect(window, (0, 255, 0),
							 (positions[i, 0], positions[i, 1], 50, 50))
		else:
			pygame.draw.rect(window, button_color,
							 (positions[i, 0], positions[i, 1], 50, 50))

		if m_on_letters[i] & (clavier[i] == 0):
			pygame.draw.rect(window, (0, 0, 0),
							 (positions[i, 0], positions[i, 1], 50, 50), 3)

		let_tx = text_font.render(str(letters[i]), 1, 'black')
		window.blit(let_tx, (positions[i, 0]+25-let_tx.get_width()/2,
							 positions[i, 1]-let_tx.get_height()/2+25))

	if health > 1:
		h_tx = text_font.render('Points de vie = '+str(health),
								1, 'black')
	else:
		h_tx = text_font.render('Point de vie = '+str(health),
								1, 'black')

	window.blit(h_tx, (25, 175))

	if health <= 7:
		pygame.draw.rect(window, (0, 0, 0), (450, 300, 300, 10))
	if health <= 6:
		pygame.draw.rect(window, (0, 0, 0), (650, 100, 10, 200))
	if health <= 5:
		pygame.draw.rect(window, (0, 0, 0), (525, 100, 150, 10))
	if health <= 4:
		pygame.draw.rect(window, (0, 0, 0), (575, 100, 10, 65))
	if health <= 3:
		pygame.draw.circle(window, (0, 0, 0), (580, 180), 20)
		pygame.draw.circle(window, bg_colour, (580, 180), 15)
	if health <= 2:
		pygame.draw.rect(window, (0, 0, 0), (578.5, 200, 5, 50))
	if health <= 1:
		pygame.draw.rect(window, (0, 0, 0), (565, 212.5, 30, 4))
	if health <= 0:
		pygame.draw.polygon(window, (0, 0, 0), ((580, 235), (590, 280),
												(585, 280), (580, 250),
												(575, 280), (570, 280)))

	if result_g == 'v':
		vic_tx = result_font.render('Vous avez trouvé le mot !',
									1, (0, 255, 0))
		window.blit(vic_tx, (25, 215))

	if result_g == 'p':
		per_tx = result_font.render("Vous n'avez pas trouvé le mot !",
									1, (255, 0, 0))
		window.blit(per_tx, (25, 215))

	if show_alredy_tryed:
		tryed_tx = text_font.render('Vous avez déjà essayé cette lettre',
									1, 'black')
		window.blit(tryed_tx, (width/2-tryed_tx.get_width()/2, 600))

	pygame.display.update()

def draw_make_guess(window, width, arrow, bg_colour, button_color, text_font,
					mouse_on_return, m_on_tiret_mg, m_on_propose,
					m_on_oui_mkg, m_on_non_mkg, m_on_conf_mkg,
					length, choiced, recenter, representation, etat,
					propose, one_possible, is_letter, possibles, selected,
					center_propos, show_is_there, must_do_some, health,
					no_possible, result_mg):
	"""
	Fonction pour afficher l'écrant du choix des lettres "minimale"
	choisient par l'ordinateur et les intéractions possibles pour
	l'humain.

	etat : list/array ; -1 for unfouded letter of the word
	propose : str ; letter proposed by the computer
	one_possible : bool ; if there is only one possible word
	is_letter : None/nool ; if the proposed letter is in the word or not
	selected : list ; letter which can be selected
	center_propos : list ; positions of where to show affilated letters
	possibles : list ; possible affiliated letters
	no_possible : bool ; if no word is possible
	"""

	window.fill(bg_colour)
	pygame.draw.polygon(window, button_color, arrow)
	if mouse_on_return:
		pygame.draw.polygon(window, (0, 0, 0), arrow, 3)

	# to show the word letters found/not found
	for i in range(length):
		if choiced[i] != '-':
			if m_on_tiret_mg[i]:
				pygame.draw.rect(window, (0, 0, 255),
								 (i*30+recenter, 350, 25, 5))
			else:
				pygame.draw.rect(window, (0, 0, 0),
								 (i*30+recenter, 350, 25, 5))

		if representation[i]:
			if etat[i] == 0:
				tx = text_font.render(str(choiced[i]), 1, (0, 0, 255))
			else:
				tx = text_font.render(str(choiced[i]), 1, 'black')

			window.blit(tx, (i*30+recenter-tx.get_width()/2+12.5, 320))

	if (propose != None)&(one_possible == False):
		is_tx1 = text_font.render("Est-ce qu'il y a un :", 1, 'black')
		window.blit(is_tx1, (50, 75))
		is_tx2 = text_font.render("'"+str(propose)+"'", 1, 'black')
		window.blit(is_tx2, (50-is_tx2.get_width()/2+is_tx1.get_width()/2, 100))

	elif (propose != None)&(one_possible):
		is_tx1 = text_font.render("Est-ce qu'il s'agit du mot :", 1, 'black')
		window.blit(is_tx1, (50, 75))
		is_tx2 = text_font.render("'"+str(propose)+"'", 1, 'black')
		window.blit(is_tx2, (50-is_tx2.get_width()/2+is_tx1.get_width()/2, 100))

	if is_letter:
		pygame.draw.rect(window, (0, 255, 0), (50, 150, 100, 50))
		if one_possible == False:
			for i in range(len(possibles)):
				if selected[i]:
					pygame.draw.rect(window, (0, 0, 255), (center_propos[i],
											 400, 50, 50))
				else:
					pygame.draw.rect(window, button_color, (center_propos[i],
											 400, 50, 50))

				if m_on_propose[i]:
					pygame.draw.rect(window, (0, 0, 0), (center_propos[i],
										 400, 50, 50), 3)

				tx_pl = text_font.render(str(possibles[i]), 1, 'black')
				window.blit(tx_pl, (center_propos[i]+25-tx_pl.get_width()/2,
									425-tx_pl.get_height()/2))

	else:
		pygame.draw.rect(window, button_color, (50, 150, 100, 50))

	tx_y = text_font.render('Oui', 1, (0, 0, 0))
	window.blit(tx_y, (100-tx_y.get_width()/2, 175-tx_y.get_height()/2))
	if m_on_oui_mkg:
		pygame.draw.rect(window, (0, 0, 0), (50, 150, 100, 50), 3)

	if is_letter == False:
		pygame.draw.rect(window, (255, 0, 0), (200, 150, 100, 50))
	else:
		pygame.draw.rect(window, button_color, (200, 150, 100, 50))

	tx_n = text_font.render('Non', 1, (0, 0, 0))
	window.blit(tx_n, (250-tx_n.get_width()/2, 175-tx_n.get_height()/2))
	if m_on_non_mkg:
		pygame.draw.rect(window, (0, 0, 0), (200, 150, 100, 50), 3)

	pygame.draw.rect(window, button_color, (100, 225, 150, 50))
	tx_c = text_font.render('Confirmer', 1, (0, 0, 0))
	window.blit(tx_c, (175-tx_c.get_width()/2, 250-tx_c.get_height()/2))
	if m_on_conf_mkg:
		pygame.draw.rect(window, (0, 0, 0), (100, 225, 150, 50), 3)

	if show_is_there:
		tx_isth1 = text_font.render('Vous devez indiquer si la lettre proposée est présente',
									1, 'black')
		window.blit(tx_isth1, (width/2-tx_isth1.get_width()/2, 400))

		tx_isth2 = text_font.render('ou non', 1, 'black')
		window.blit(tx_isth2, (width/2-tx_isth2.get_width()/2, 425))

	if must_do_some:
		tx_isth1 = text_font.render('Vous devez indiquer où la lettre proposée est présente',
									1, 'black')
		window.blit(tx_isth1, (width/2-tx_isth1.get_width()/2, 450))

		tx_isth2 = text_font.render('ou changer la sélection à non', 1, 'black')
		window.blit(tx_isth2, (width/2-tx_isth2.get_width()/2, 475))

	if health <= 7:
		pygame.draw.rect(window, (0, 0, 0), (450, 250, 300, 10))
	if health <= 6:
		pygame.draw.rect(window, (0, 0, 0), (650, 50, 10, 200))
	if health <= 5:
		pygame.draw.rect(window, (0, 0, 0), (525, 50, 150, 10))
	if health <= 4:
		pygame.draw.rect(window, (0, 0, 0), (575, 50, 10, 65))
	if health <= 3:
		pygame.draw.circle(window, (0, 0, 0), (580, 130), 20)
		pygame.draw.circle(window, bg_colour, (580, 130), 15)
	if health <= 2:
		pygame.draw.rect(window, (0, 0, 0), (578.5, 150, 5, 50))
	if health <= 1:
		pygame.draw.rect(window, (0, 0, 0), (565, 165.5, 30, 4))
	if health <= 0:
		pygame.draw.polygon(window, (0, 0, 0), ((580, 185), (590, 230),
												(585, 230), (580, 200),
												(575, 230), (570, 230)))

	if no_possible:
		tx_isth1 = text_font.render("Je n'ai pas de mot corresponant aux caractéristiques que",
									1, 'black')
		window.blit(tx_isth1, (width/2-tx_isth1.get_width()/2, 400))

		tx_isth2 = text_font.render("vous m'avez fournis. J'ai donc perdus. Je vous conseille",
									1, 'black')
		window.blit(tx_isth2, (width/2-tx_isth2.get_width()/2, 425))

		tx_isth3 = text_font.render("de mettre à jour ma base de données en conséquence.",
									1, 'black')
		window.blit(tx_isth3, (width/2-tx_isth3.get_width()/2, 450))

	if (result_mg == 'p')&(one_possible == False):
		tx_re = text_font.render("J'ai perdus, je n'ai pas trouvé le mot que vous aviez choisit",
								 1, 'black')
		window.blit(tx_re, (width/2-tx_re.get_width()/2, 450))

	elif result_mg == 'v':
		tx_re = text_font.render("J'ai gagné, j'ai trouvé le mot que vous aviez choisit",
								 1, 'black')
		window.blit(tx_re, (width/2-tx_re.get_width()/2, 450))

	pygame.display.update()

def draw_2_player(window, width, arrow, bg_colour, button_color, text_font,
				  result_font, positions, letters,
				  mouse_on_return, m_on_letters, m_on_oui_mkg, m_on_non_mkg,
				  m_on_conf_mkg, m_on_propose, m_on_tiret_mg,
				  health, length, choiced, recenter, representation, step,
				  clavier, choice_letter, is_letter, possibles, selected,
				  center_propos, etat, result_mg,
				  vict_1, vict_2, defai_1, defai_2, turn):
	"""
	Function pour afficher l'écran de jeu en mode deux joueurs (humains).
	"""
	window.fill(bg_colour)
	pygame.draw.polygon(window, button_color, arrow)
	if mouse_on_return:
		pygame.draw.polygon(window, (0, 0, 0), arrow, 3)

	# to show the word letters found/not found
	for i in range(length):
		if choiced[i] != '-':
			if m_on_tiret_mg[i]:
				pygame.draw.rect(window, (0, 0, 255),
								 (i*30+recenter, 350, 25, 5))
			else:
				pygame.draw.rect(window, (0, 0, 0),
								 (i*30+recenter, 350, 25, 5))

		if representation[i]:
			if etat[i] == 0:
				tx = text_font.render(str(choiced[i]), 1, (0, 0, 255))
			else:
				tx = text_font.render(str(choiced[i]), 1, 'black')

			window.blit(tx, (i*30+recenter-tx.get_width()/2+12.5, 320))

	if step == 'g':
		for i in range(26):
			if clavier[i] == -1:
				pygame.draw.rect(window, (255, 0, 0),
								 (positions[i, 0], positions[i, 1], 50, 50))

			elif clavier[i] == 1:
				pygame.draw.rect(window, (0, 255, 0),
								 (positions[i, 0], positions[i, 1], 50, 50))

			else:
				pygame.draw.rect(window, button_color,
								 (positions[i, 0], positions[i, 1], 50, 50))

			if m_on_letters[i] & (clavier[i] == 0):
				pygame.draw.rect(window, (0, 0, 0),
								 (positions[i, 0], positions[i, 1], 50, 50), 3)

			let_tx = text_font.render(str(letters[i]), 1, 'black')
			window.blit(let_tx, (positions[i, 0]+25-let_tx.get_width()/2,
								 positions[i, 1]-let_tx.get_height()/2+25))

	elif step == 'e':
		is_tx1 = text_font.render("Est-ce qu'il y a un :", 1, 'black')
		window.blit(is_tx1, (50, 75))
		is_tx2 = text_font.render("'"+choice_letter+"'", 1, 'black')
		window.blit(is_tx2, (50-is_tx2.get_width()/2+is_tx1.get_width()/2, 100))

		if is_letter:
			pygame.draw.rect(window, (0, 255, 0), (50, 150, 100, 50))
			for i in range(len(possibles)):
				if selected[i]:
					pygame.draw.rect(window, (0, 0, 255), (center_propos[i],
											 400, 50, 50))
				else:
					pygame.draw.rect(window, button_color, (center_propos[i],
											 400, 50, 50))

				if m_on_propose[i]:
					pygame.draw.rect(window, (0, 0, 0), (center_propos[i],
										 400, 50, 50), 3)

				tx_pl = text_font.render(str(possibles[i]), 1, 'black')
				window.blit(tx_pl, (center_propos[i]+25-tx_pl.get_width()/2,
									425-tx_pl.get_height()/2))

		else:
			pygame.draw.rect(window, button_color, (50, 150, 100, 50))

		tx_y = text_font.render('Oui', 1, (0, 0, 0))
		window.blit(tx_y, (100-tx_y.get_width()/2, 175-tx_y.get_height()/2))
		if m_on_oui_mkg:
			pygame.draw.rect(window, (0, 0, 0), (50, 150, 100, 50), 3)

		if is_letter == False:
			pygame.draw.rect(window, (255, 0, 0), (200, 150, 100, 50))
		else:
			pygame.draw.rect(window, button_color, (200, 150, 100, 50))

		tx_n = text_font.render('Non', 1, (0, 0, 0))
		window.blit(tx_n, (250-tx_n.get_width()/2, 175-tx_n.get_height()/2))
		if m_on_non_mkg:
			pygame.draw.rect(window, (0, 0, 0), (200, 150, 100, 50), 3)

		pygame.draw.rect(window, button_color, (100, 225, 150, 50))
		tx_c = text_font.render('Confirmer', 1, (0, 0, 0))
		window.blit(tx_c, (175-tx_c.get_width()/2, 250-tx_c.get_height()/2))
		if m_on_conf_mkg:
			pygame.draw.rect(window, (0, 0, 0), (100, 225, 150, 50), 3)

	if health <= 7:
		pygame.draw.rect(window, (0, 0, 0), (450, 250, 300, 10))
	if health <= 6:
		pygame.draw.rect(window, (0, 0, 0), (650, 50, 10, 200))
	if health <= 5:
		pygame.draw.rect(window, (0, 0, 0), (525, 50, 150, 10))
	if health <= 4:
		pygame.draw.rect(window, (0, 0, 0), (575, 50, 10, 65))
	if health <= 3:
		pygame.draw.circle(window, (0, 0, 0), (580, 130), 20)
		pygame.draw.circle(window, bg_colour, (580, 130), 15)
	if health <= 2:
		pygame.draw.rect(window, (0, 0, 0), (578.5, 150, 5, 50))
	if health <= 1:
		pygame.draw.rect(window, (0, 0, 0), (565, 165.5, 30, 4))
	if health <= 0:
		pygame.draw.polygon(window, (0, 0, 0), ((580, 185), (590, 230),
												(585, 230), (580, 200),
												(575, 230), (570, 230)))

	if result_mg == 'v':
		vic_tx = result_font.render('Le joueur '+str(turn)+' a trouvé le mot !',
									1, (0, 255, 0))
		window.blit(vic_tx, (25, 210))

	if result_mg == 'p':
		per_tx = result_font.render('Le joueur '+str(turn)+" n'a pas trouvé le mot !",
									1, (255, 0, 0))
		window.blit(per_tx, (25, 210))

	tx = text_font.render("Joueur 1", 1, (0, 0, 0))
	window.blit(tx, (width/3-tx.get_width()/2, 565))
	tx = text_font.render("Victoire : "+str(vict_1), 1, (0, 0, 0))
	window.blit(tx, (width/3-tx.get_width()/2, 600))
	tx = text_font.render("Defaite : "+str(defai_1), 1, (0, 0, 0))
	window.blit(tx, (width/3-tx.get_width()/2, 625))

	tx = text_font.render("Joueur 2", 1, (0, 0, 0))
	window.blit(tx, (width*2/3-tx.get_width()/2, 565))
	tx = text_font.render("Victoire : "+str(vict_2), 1, (0, 0, 0))
	window.blit(tx, (width*2/3-tx.get_width()/2, 600))
	tx = text_font.render("Defaite : "+str(defai_2), 1, (0, 0, 0))
	window.blit(tx, (width*2/3-tx.get_width()/2, 625))

	pygame.display.update()