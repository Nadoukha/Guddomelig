import pygame
import time
import Sprites
import Alt

import random
import os
 
pygame.init()
 
# Définition de constantes
dim = Sprites.taille*9 

gris = (110,110,110)
noir = (0,0,0)
vert = (0,200,0)
vert_claire = (0,255,0)
rouge = (200,0,0)
rouge_claire = (255,0,0)
bleu = (0,0,200)
bleu_claire = (50,50,250)


petittexte = pygame.font.SysFont("Verdana",Sprites.taille//2)
grandtexte = pygame.font.SysFont('Verdana',Sprites.taille)


page_aide = 0
 
gameDisplay = pygame.display.set_mode((dim,dim))
clock = pygame.time.Clock()

def text_objects(text, font):
    textSurface = font.render(text, True, noir)
    return textSurface, textSurface.get_rect()
    
def quitterlejeu():
    pygame.quit()
    quit()
    
def autre_page():
	global page_aide
	page_aide = (page_aide+1)%2
    
def boutons(msg,x,y,longueur,hauteur,ci,ca,action= None):

    souri = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+longueur > souri[0] > x and y+hauteur > souri[1] > y:
        # print(action)
        pygame.draw.rect(gameDisplay, ca,(x,y,longueur,hauteur))
        if click[0] == 1 and action != None:
            action()
            
    else:
        pygame.draw.rect(gameDisplay, ci,(x,y,longueur,hauteur))

    textSurf, textRect = text_objects(msg, petittexte)
    textRect.center = ( (x+(longueur/2)), (y+(hauteur/2)) )
    gameDisplay.blit(textSurf, textRect)
    
salle = []


	
def fond():
	for i in range(9) :
		if i==0 or i==(8):
			salle.append([2]*9*dim)
		else :
			salle.append([2]+ 7*[0] +[2])	
			
	background= pygame.Surface( (9*64 , 9*64) )  
	
	for x in range(9):
			for y in range(9):
				if x == 0 :
					if y == 0:
						background.blit(Sprites.mur7,(x*Sprites.taille,y*Sprites.taille))
					elif y == 8:
						background.blit(Sprites.mur1,(x*Sprites.taille,y*Sprites.taille))
					else:
						background.blit(Sprites.mur4,(x*Sprites.taille,y*Sprites.taille))
				elif x == 8:
					if y == 0:
						background.blit(Sprites.mur9,(x*Sprites.taille,y*Sprites.taille))
					elif y == 8:
						background.blit(Sprites.mur3,(x*Sprites.taille,y*Sprites.taille))
					else:
						background.blit(Sprites.mur6,(x*Sprites.taille,y*Sprites.taille))
				else : 
					if y == 0:
						background.blit(Sprites.mur8,(x*Sprites.taille,y*Sprites.taille))
					elif y == 8:
						background.blit(Sprites.mur2,(x*Sprites.taille,y*Sprites.taille))
					else:
						background.blit(Sprites.sol,(x*Sprites.taille,y*Sprites.taille))
	return(background)			

arriere_plan=fond()	
        
    
def perdu():

    perdu  = True 
    while perdu:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        
        gameDisplay.blit(arriere_plan,(0,0))
      
        TextSurf, TextRect = text_objects("Vous avez perdu :( ", grandtexte)
        TextRect.center = ((dim/2),(dim/4))
        gameDisplay.blit(TextSurf, TextRect)
        
        boutons("Recommencer", (dim/4),(dim/2),Sprites.taille*2.5,Sprites.taille,vert,vert_claire,intro)
        boutons("Quitter", (dim*3/4),(dim/2),Sprites.taille*2,Sprites.taille,rouge,rouge_claire,quitterlejeu)
        
        pygame.display.update()
        clock.tick(15)
           
def regles(): 
    
	regles = True
   
	while regles:
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				pygame.quit()
				quit()
				pass
		
		
		gameDisplay.blit(arriere_plan,(0,0))
        
		if not page_aide:
			TextSurf, TextRect = text_objects("Règles (1):", grandtexte)
			TextRect.center = ((dim/2),(dim/6))
			gameDisplay.blit(TextSurf, TextRect)
			
			TextSurf, TextRect = text_objects("Z,Q,S,D : se déplacer", petittexte)
			TextRect.center = ((dim/2),3.5*Sprites.taille)
			gameDisplay.blit(TextSurf, TextRect)
			
			TextSurf, TextRect = text_objects("Flèches : donner des coups d'épée", petittexte)
			TextRect.center = ((dim/2),4.5*Sprites.taille)
			gameDisplay.blit(TextSurf, TextRect)
			
			TextSurf, TextRect = text_objects("Espace : utiliser de la magie", petittexte)
			TextRect.center = ((dim/2),5.5*Sprites.taille)
			gameDisplay.blit(TextSurf, TextRect)
			
			TextSurf, TextRect = text_objects("A/J et E/K : choisir un objet", petittexte)
			TextRect.center = ((dim/2),6.5*Sprites.taille)
			gameDisplay.blit(TextSurf, TextRect)
			
			TextSurf, TextRect = text_objects("Entree : utiliser un objet", petittexte)
			TextRect.center = ((dim/2),7.5*Sprites.taille)
			gameDisplay.blit(TextSurf, TextRect)
			
			boutons(" => ",7*Sprites.taille,0,2*Sprites.taille,Sprites.taille,bleu,bleu_claire,autre_page)
			
			boutons("C'est bon!", 0,Sprites.taille*8,9*Sprites.taille,Sprites.taille,vert,vert_claire,Alt.visualisation)
		
		if page_aide:
			gameDisplay.blit(arriere_plan,(0,0))
			TextSurf, TextRect = text_objects("Règles (2) :", grandtexte)
			TextRect.center = ((dim/2),(dim/6))
			gameDisplay.blit(TextSurf, TextRect)
			
			TextSurf, TextRect = text_objects("Épée : 2 de dégats, 1 de portée ", petittexte)
			TextRect.center = ((dim/2),3.5*Sprites.taille)
			gameDisplay.blit(TextSurf, TextRect)
			
			TextSurf, TextRect = text_objects("Magie : 1 de dégat, 5 de portée ", petittexte)
			TextRect.center = ((dim/2),4.5*Sprites.taille)
			gameDisplay.blit(TextSurf, TextRect)
			
			TextSurf, TextRect = text_objects("Scarabée : 4 de vie", petittexte)
			TextRect.center = ((dim/2),5.5*Sprites.taille)
			gameDisplay.blit(TextSurf, TextRect)
			
			TextSurf, TextRect = text_objects("Gemme : etourdit et blesse tlm.", petittexte)
			TextRect.center = ((dim/2),6.5*Sprites.taille)
			gameDisplay.blit(TextSurf, TextRect)
			
			TextSurf, TextRect = text_objects("Potion : Guerit les blessuress", petittexte)
			TextRect.center = ((dim/2),7.5*Sprites.taille)
			gameDisplay.blit(TextSurf, TextRect)
			
			boutons(" <= ",0,0,2*Sprites.taille,Sprites.taille,bleu,bleu_claire,autre_page)
			
			boutons("C'est bon!", 0,Sprites.taille*8,9*Sprites.taille,Sprites.taille,vert,vert_claire,Alt.visualisation)
	
	
		pygame.display.update()
		clock.tick(15)

def menu():
	
	menu = True

	while menu:
	
		for event in pygame.event.get():
            
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				pygame.quit()
				quit()
				
		gameDisplay.blit(arriere_plan,(0,0))

		TextSurf, TextRect = text_objects("Guddomelig", grandtexte)
		TextRect.center = ((dim/2),(dim/4))
		gameDisplay.blit(TextSurf, TextRect)
        
		boutons("GO!",Sprites.taille,5*Sprites.taille,7*Sprites.taille,Sprites.taille,vert,vert_claire,Alt.visualisation)
		boutons("Règles du jeu",Sprites.taille,6*Sprites.taille,7*Sprites.taille,Sprites.taille,bleu,bleu_claire,regles)
		boutons("Quitter",Sprites.taille,7*Sprites.taille,7*Sprites.taille,Sprites.taille,rouge,rouge_claire,quitterlejeu)
           
        
		pygame.display.update()
		clock.tick(15)
        

    
menu()
