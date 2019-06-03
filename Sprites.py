import pygame as pg

import os


pg.init()
# Image chargée de cette manière pour que le jeu fonctionne même sur clef USB
Sheet = pg.image.load(os.path.dirname(os.path.abspath(__file__)) + "\qs.png")

# Choix de l'unité de taille du jeu ( une case ) par le joueur. Valeur par défaut : 64
try:
	scale = float(input("taille sprites ? ( [ENTRÉE] pour le choix optimal ) : "))
except ValueError:
	scale = 1.0
# Taille de l'unité réduite selon la taille de l'écran

taille = min(int(64*scale),(pg.display.Info().current_h-64)//15)

# Choix d'un nom valide par le joueur, si le nom ne contient aucune lettre ou est invalide, le joueur sera nommé Jolly 
alphabet = "abcdefghijklmnopqrstuvwxyz"
try:
	nom_joueur = input("Entrez votre nom : ")
	nom_valide = False
except ValueError:
	nom_joueur = "Jolly"
	
for i in range(len(alphabet)):
	if alphabet[i] in nom_joueur.lower():
		nom_valide = True
		break
if not nom_valide:
	nom_joueur = "Jolly"
else:
	pass


	# Fonction permettant de découper des sous-images (Sprites) à partir d'une image en contenant plusieurs (Spritesheet)
def Sprite(Sheet : pg.Surface,ligne,colonne,TailleSprite,TailleDesiree):

	# Image à découper
	ImageSource = pg.Surface((TailleSprite,TailleSprite))
	# Image découpée
	ImageFinale = pg.Surface((TailleDesiree,TailleDesiree))
	
	# Copier la couleur de chacun des pixels voulus pour découper l'image voulue
	for x in range(TailleSprite):
		for y in range(TailleSprite):
			col = Sheet.get_at((colonne*TailleSprite+x,ligne*TailleSprite+y))
			ImageSource.set_at((x,y),col)
	
	pg.transform.scale(ImageSource,(TailleDesiree,TailleDesiree),ImageFinale)
	return ImageFinale
	
	

	# Fonction permettant la visualisation des Sprites obtenus
def visualisation():
	pg.init()
	screen = pg.display.set_mode((taille,taille))
	t = pg.time.Clock()
	pg.display.set_caption("Sprite test")

	spr = [mur1,mur2,mur3,mur4,sol,mur6,mur7,mur8,mur9,porte_bas,porte_droite,porte_gauche,porte_haut,spawn,escaliers,potion,mechant,player,epee,magie]

	running = True
	i = 0
	re = False
	while running:
		t.tick(60)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
				
		keys = pg.key.get_pressed()
		
		if keys[pg.K_LEFT] and re == False :
			i = max(0,i-1)
			re = True
		if keys[pg.K_RIGHT] and re == False:
			i = min(len(spr)-1,i+1)
			re = True
		if not keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
			re = False
			
		screen.fill((255,0,0))
		pg.draw.rect(screen,(0,255,0),(0,0,taille//2,taille))
		screen.blit(spr[i],(0,0))
				
		pg.display.update()
	pg.quit()
	
# Constituants d'une salle	
sol = Sprite(Sheet,1,1,32,taille)

mur7 = Sprite(Sheet,0,0,32,taille)
mur8 = Sprite(Sheet,0,1,32,taille)
mur9 = Sprite(Sheet,0,2,32,taille)
mur4 = Sprite(Sheet,1,0,32,taille)
mur6 = Sprite(Sheet,1,2,32,taille)
mur1 = Sprite(Sheet,2,0,32,taille)
mur2 = Sprite(Sheet,2,1,32,taille)
mur3 = Sprite(Sheet,2,2,32,taille)

spawn = Sprite(Sheet,0,3,32,taille)
escaliers = Sprite(Sheet,1,3,32,taille)

porte_haut = Sprite(Sheet,2,3,32,taille)

# Images obtenues par rotation de la première

porte_gauche = pg.transform.rotate(porte_haut,90)
porte_bas = pg.transform.rotate(porte_haut,180)
porte_droite = pg.transform.rotate(porte_haut,270)


# Images obtenues différemment pour conserver la transparence

potion = pg.transform.scale(pg.image.load(os.path.dirname(os.path.abspath(__file__)) + "\potion.png"),(taille,taille))

mechant = pg.transform.scale(pg.image.load(os.path.dirname(os.path.abspath(__file__)) + "\scarabee.png"),(taille,taille))

player = pg.transform.scale(pg.image.load(os.path.dirname(os.path.abspath(__file__)) + "\joueur.png"),(taille,taille))
epee = pg.transform.scale(pg.image.load(os.path.dirname(os.path.abspath(__file__)) + "\epee.png"),(taille,taille))
magie = pg.transform.scale(pg.image.load(os.path.dirname(os.path.abspath(__file__)) + "\magie.png"),(taille,taille))
