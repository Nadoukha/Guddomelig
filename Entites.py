import pygame as pg
import Sprites
import Alt
from random import randrange

class Player:
	
	def __init__ (self,x,y) :
		self.x=x
		self.y=y
		
		self.score = 0
		
		self.etage = 1
		self.vie = 10
		self.vie_max = 10
		self.range = 5
		
		self.vel=1
		
		self.dx = 0
		self.dy = 0
		
		self.objets = []
		
		self.etage = 1
		self.niv = Alt.Niveau(self.etage)
		
		self.fini_move=False
		self.tour = True
		self.mort = False
		
		self.cd = False
		self.pos_sac = 0
		
		self.sprite_joueur = Sprites.player
		self.sprite_epee = Sprites.epee
		self.sprite_projectile = Sprites.magie
		
		
	
	def move(self) :
	
		self.keys = pg.key.get_pressed()
		
		
		if self.keys[pg.K_a] :
			
			if self.keys[pg.K_LCTRL]:
				self.dx=-1
				self.dy=0
			elif self.niv.salle_active.salle[self.y][self.x-1] != 2 and not(self.fini_move) and not(self.niv.salle_active.ennemi_ici(self.x-1,self.y)):
				self.x -= 1
				self.dx=-1
				self.dy=0
				
				if self.niv.salle_active.salle[self.y][self.x] == 1:
					self.niv.ind_salle_prev = self.niv.ind_salle_active
					
					self.donnees = [self.niv.salle_active.xi,self.niv.salle_active.yi,self.niv.salle_active.l,self.niv.salle_active.h,self.niv.salle_active.taille_unite]
					self.coords = [self.donnees[0] - 1,self.donnees[1] + (self.y // self.donnees[4])]
					
					
					self.niv.ind_salle_active = self.niv.carte[self.coords[1]][self.coords[0]] - 1
					self.niv.salles[self.niv.ind_salle_prev] = self.niv.salle_active
					self.niv.salle_active = self.niv.salles[self.niv.ind_salle_active]
					
					self.x = len(self.niv.salle_active.salle[0])-2
					self.y = (self.coords[1] - self.niv.salle_active.yi  )*self.niv.salle_active.taille_unite + self.niv.salle_active.taille_unite//2
					self.fini_move= True
					
					
				if self.niv.salle_active.objet_ici(self.x,self.y):
					self.ind_objet = self.niv.salle_active.objet_ici(self.x,self.y)-1
					self.pickup(self.niv.salle_active.objets[self.ind_objet])
					self.niv.salle_active.objets.pop(self.ind_objet)
					
					
				self.tour = False
				self.fini_move= True

		if self.keys[pg.K_d] :
			
			if self.keys[pg.K_LCTRL]:
				self.dx=1
				self.dy=0
			
			
			elif self.niv.salle_active.salle[self.y][self.x+1] != 2 and not(self.fini_move)and not(self.niv.salle_active.ennemi_ici(self.x+1,self.y)):
				self.x += 1
				self.dx=1
				self.dy=0
				if self.niv.salle_active.salle[self.y][self.x] == 1:
					
					
					
					self.niv.ind_salle_prev = self.niv.ind_salle_active
					
					
					
					self.donnees = [self.niv.salle_active.xi,self.niv.salle_active.yi,self.niv.salle_active.l,self.niv.salle_active.h,self.niv.salle_active.taille_unite]
					
					self.coords = [self.donnees[0] + self.donnees[2],self.donnees[1] + (self.y // self.donnees[4])]
					
					self.niv.ind_salle_active = self.niv.carte[ self.coords[1] ][ self.coords[0] ] - 1
					
					self.niv.salles[self.niv.ind_salle_prev] = self.niv.salle_active
					self.niv.salle_active = self.niv.salles[self.niv.ind_salle_active]
					
					self.x = 1
					self.y = (self.coords[1] - self.niv.salle_active.yi)*self.niv.salle_active.taille_unite + self.niv.salle_active.taille_unite//2
				
					self.fini_move= True
					
					
				if self.niv.salle_active.objet_ici(self.x,self.y):
					self.ind_objet = self.niv.salle_active.objet_ici(self.x,self.y)-1
					self.pickup(self.niv.salle_active.objets[self.ind_objet])
					self.niv.salle_active.objets.pop(self.ind_objet)
				
				
				self.fini_move= True
				self.tour = False
		
		if self.keys[pg.K_w] :
			
			
			if self.keys[pg.K_LCTRL]:
					
				self.dx=0
				self.dy=-1
				
			elif self.niv.salle_active.salle[self.y-1][self.x] != 2 and not(self.fini_move) and not(self.niv.salle_active.ennemi_ici(self.x,self.y-1)):
				self.y -= 1
				self.dx=0
				self.dy=-1

				if self.niv.salle_active.salle[self.y][self.x] == 1:
					self.niv.ind_salle_prev = self.niv.ind_salle_active
					
					self.donnees = [self.niv.salle_active.xi,self.niv.salle_active.yi,self.niv.salle_active.l,self.niv.salle_active.h,self.niv.salle_active.taille_unite]
					self.coords = [self.donnees[0] + ( self.x // self.donnees[4] ),self.donnees[1]-1]
					
					
					self.niv.ind_salle_active = self.niv.carte[self.coords[1]][self.coords[0]] - 1
					self.niv.salles[self.niv.ind_salle_prev] = self.niv.salle_active
					self.niv.salle_active = self.niv.salles[self.niv.ind_salle_active]
					
					self.x = (self.coords[0]-self.niv.salle_active.xi)*self.niv.salle_active.taille_unite + self.niv.salle_active.taille_unite//2
					self.y = len(self.niv.salle_active.salle)-2
					
					
					self.fini_move= True
					
				if self.niv.salle_active.objet_ici(self.x,self.y):
					self.ind_objet = self.niv.salle_active.objet_ici(self.x,self.y)-1
					self.pickup(self.niv.salle_active.objets[self.ind_objet])
					self.niv.salle_active.objets.pop(self.ind_objet)
				
			
				self.fini_move= True
				self.tour = False
		
		
		if self.keys[pg.K_s] :
			
			if self.keys[pg.K_LCTRL]:
				self.dx=0
				self.dy=1
			elif self.niv.salle_active.salle[self.y+1][self.x] != 2 and not(self.fini_move)and not(self.niv.salle_active.ennemi_ici(self.x,self.y+1)):
		
				self.y += 1
				self.dx=0
				self.dy=1
				
				if self.niv.salle_active.salle[self.y][self.x] == 1:
					self.niv.ind_salle_prev = self.niv.ind_salle_active
					
					self.donnees = [self.niv.salle_active.xi,self.niv.salle_active.yi,self.niv.salle_active.l,self.niv.salle_active.h,self.niv.salle_active.taille_unite]
					self.coords = [self.donnees[0] + ( self.x // self.donnees[4] ),self.donnees[1] + self.donnees[3]]
					
					
					self.niv.ind_salle_active = self.niv.carte[self.coords[1]][self.coords[0]] - 1
					self.niv.salles[self.niv.ind_salle_prev] = self.niv.salle_active
					self.niv.salle_active = self.niv.salles[self.niv.ind_salle_active]
					self.x = (self.coords[0]-self.niv.salle_active.xi)*self.niv.salle_active.taille_unite + self.niv.salle_active.taille_unite//2
					self.y = 1
					
					self.fini_move= True
					
					
				if self.niv.salle_active.objet_ici(self.x,self.y):
					self.ind_objet = self.niv.salle_active.objet_ici(self.x,self.y)-1
					self.pickup(self.niv.salle_active.objets[self.ind_objet])
					self.niv.salle_active.objets.pop(self.ind_objet)
				
					
				self.fini_move= True
				self.tour = False
		
		if not(self.keys[pg.K_a] or self.keys[pg.K_d] or self.keys[pg.K_w] or self.keys[pg.K_s]):
			self.fini_move = False
			
		if self.niv.salle_active.salle[self.y][self.x] == 3:
				self.ind_salle_active = 0
				self.etage += 1
				self.niv = Alt.Niveau(self.etage)
				self.x,self.y = 3,3
				self.score += 20
				
	
	def melee(self,screen):
		keys= pg.key.get_pressed()
		
		if keys[pg.K_UP]:
			self.render(screen)
			screen.blit(self.sprite_epee,(self.niv.salle_active.dif_affichage[0]+self.x * Sprites.taille,self.niv.salle_active.dif_affichage[1] + self.y*Sprites.taille-Sprites.taille//2))
			pg.display.update()
			pg.time.delay(200)
			
			if self.niv.salle_active.ennemi_ici(self.x,self.y-1) :
				self.ind_ennemi = self.niv.salle_active.ennemi_ici(self.x,self.y-1)-1
				
				self.niv.salle_active.ennemis[self.ind_ennemi].hit(2,1,self)
				
			self.fini_move=True
			self.tour = False
			pg.time.delay(200)
		
		if keys[pg.K_DOWN]:
			self.render(screen)
			screen.blit(pg.transform.rotate(self.sprite_epee,180),(self.niv.salle_active.dif_affichage[0] + self.x*Sprites.taille ,self.niv.salle_active.dif_affichage[1] + self.y*Sprites.taille + Sprites.taille//2))
			pg.display.update()
			pg.time.delay(200)
			if self.niv.salle_active.ennemi_ici(self.x,self.y+1):
				
				self.ind_ennemi = self.niv.salle_active.ennemi_ici(self.x,self.y+1)-1
				self.niv.salle_active.ennemis[self.ind_ennemi].hit(2,1,self)
							
			self.fini_move=True
			self.tour = False
			pg.time.delay(200)
		
		if keys[pg.K_LEFT]:
			self.render(screen)
			screen.blit(pg.transform.rotate(self.sprite_epee,90),(self.niv.salle_active.dif_affichage[0] + self.x*Sprites.taille - Sprites.taille//2 ,self.niv.salle_active.dif_affichage[1] + self.y*Sprites.taille ))
			pg.display.update()
			pg.time.delay(200)
			if self.niv.salle_active.ennemi_ici(self.x-1,self.y):
				
				self.ind_ennemi = self.niv.salle_active.ennemi_ici(self.x-1,self.y)-1
				self.niv.salle_active.ennemis[self.ind_ennemi].hit(2,1,self)
				
			self.fini_move=True
			self.tour = False
			pg.time.delay(200)
			
		if keys[pg.K_RIGHT]:
			self.render(screen)
			screen.blit(pg.transform.rotate(self.sprite_epee,270),(self.niv.salle_active.dif_affichage[0] + self.x*Sprites.taille + Sprites.taille//2 ,self.niv.salle_active.dif_affichage[1] + self.y*Sprites.taille))
			pg.display.update()
			pg.time.delay(200)
			if self.niv.salle_active.ennemi_ici(self.x+1,self.y):
				
				self.ind_ennemi = self.niv.salle_active.ennemi_ici(self.x+1,self.y)-1
				self.niv.salle_active.ennemis[self.ind_ennemi].hit(2,1,self)
				
			self.fini_move=True
			self.tour = False
			pg.time.delay(200)
	
	def shoot(self,screen):

		keys= pg.key.get_pressed()
		if keys[pg.K_SPACE]:
		
			
			self.stop=False
			range_check=self.range * Sprites.taille
			x= 0
			y= 0
			
			dif = self.niv.salle_active.dif_affichage
			
			while self.stop == False:
				x=x+self.dx
				y=y+self.dy
				range_check=range_check-1
				
				self.niv.salle_active.aff(screen)
				if self.dy == 0 :
					screen.blit(pg.transform.rotate(self.sprite_projectile,-self.dx*90),(self.x*Sprites.taille + dif[0] + x , self.y*Sprites.taille + dif[1] + y ))
				elif self.dy == -1 :
					screen.blit(self.sprite_projectile,(self.x*Sprites.taille + dif[0] + x*Sprites.taille,self.y*Sprites.taille + dif[1] + y))
				elif self.dy== 1 :
					screen.blit(pg.transform.rotate(self.sprite_projectile,180),(self.x*Sprites.taille + dif[0] + x ,self.y*Sprites.taille + dif[1] + y))
				
				
				self.render(screen)
				
				pg.display.update()
			
				if 0 < self.niv.salle_active.salle[self.y + y//Sprites.taille][self.x + x//Sprites.taille] <= 2 or range_check < 0 :
					
					self.stop = True
					self.fini_move = True
					self.tour = False
					break
				
				if self.niv.salle_active.ennemi_ici(self.x + x// Sprites.taille,self.y + y//Sprites.taille) : 
					
					self.stop = True
					self.fini_move = True
					self.tour = False
					self.ind_ennemi = self.niv.salle_active.ennemi_ici(self.x + x// Sprites.taille,self.y + y//Sprites.taille,)-1
					
					self.niv.salle_active.ennemis[self.ind_ennemi].hit(1,1,self)
					
	
	def render(self,screen) :
		
		screen.blit(self.sprite_joueur,(self.niv.salle_active.dif_affichage[0] + Sprites.taille*self.x,self.niv.salle_active.dif_affichage[1] + Sprites.taille*self.y))
	
	def hit(self):
		
		self.vie-=1
		if self.vie<=0:
			self.mort = True
	
	def backpack(self,screen):
		keys = pg.key.get_pressed()
		
		if len(self.objets)>0: 
			
			if (keys[pg.K_k] or keys[pg.K_e]) and not self.cd :
				self.pos_sac= min(len(self.objets)-1,self.pos_sac+1)
				self.cd = True
							
			if (keys[pg.K_j] or keys[pg.K_q]) and not self.cd:
				self.pos_sac= max(0,self.pos_sac-1)
				self.cd = True
						
			if keys[pg.K_RETURN] and not self.cd:
				
				self.cd = True
				self.objets[self.pos_sac].use(self,screen)
				del self.objets[self.pos_sac]
				self.pos_sac = min(self.pos_sac,len(self.objets)-1)
				self.score -= 5
				
	
			if not (keys[pg.K_RETURN] or keys[pg.K_k] or keys[pg.K_j] or keys[pg.K_q] or keys[pg.K_e]):
				self.cd = False
			
	def pickup(self,item):
		item.x = 17
		item.y = 7
		self.objets.append(item)
		self.pos_sac = len(self.objets)-1
			
	def tick(self,screen): 
		
		self.backpack(screen)
		self.move()
		self.melee(screen)
		self.shoot(screen)
		

class Ennemi:	
	
	def __init__(self,x,y,salle):
		self.x = x
		self.y = y
		
		self.vie = 4
		self.stun = 0
		self.sprite = Sprites.mechant
		
		self.salle = salle
		self.dif_affichage = self.salle.dif_affichage
	
		self.visible = True
	
	def deplacement (self,joueur,screen):
		
			
		if self.x+self.dx == joueur.x and self.y + self.dy == joueur.y:	
			joueur.hit()
		
		elif not joueur.niv.salle_active.ennemi_ici(self.x+self.dx,self.y+self.dy) :
			self.x=self.x+self.dx
			self.y=self.y+self.dy
		else :
			pass
		
	
	def find (self,joueur):
		
		for i in range(len(self.salle.salle)):
			for j in range(len(self.salle.salle[0])):
				
				if self.x > joueur.x :
					self.dx=-1
				elif self.x == joueur.x:
					self.dx=0 
				else: 
					self.dx=1
					
				if self.y > joueur.y :
					self.dy=-1
				elif self.y == joueur.y:
					self.dy=0
				else:
					self.dy=1
	
	def hit(self,dmg,stun,joueur):
		
		self.vie -= dmg 
		self.stun += stun
		if self.vie<=0:

			self.mort()
			joueur.score += 10
	
	def tick(self,joueur,screen): 
		if self.stun==0: 
			self.find(joueur)
			self.deplacement(joueur,screen)
		else:
			self.stun=self.stun-1	
		
		
	def aff(self,screen,coords):
		screen.blit(self.sprite,( coords[0] + self.x*Sprites.taille, coords[1] + self.y*Sprites.taille))
		
	def mort(self):
		self.visible = False
		self.x,self.y = -1,-1
		print(self.x,self.y,self.visible)
		
		
class Potion:
	def __init__(self,x,y,deb=False):
		
		self.x = x
		self.y = y
		
		if not deb:
			self.vie= randrange(1,7)
		else:
			self.vie= randrange(1,3)
		self.Sprite= Sprites.potion
		self.nom="Potion de vie ( " + str(self.vie) + " )"
		self.sous_nom = ""
	
	def use(self,joueur,screen):
		joueur.vie= min(joueur.vie_max,joueur.vie +self.vie)
			
	def draw(self,screen,salle,show = False):
		dif_affichage = [0,0]
		if not show:
			dif_affichage = salle.dif_affichage
		screen.blit((self.Sprite),(self.x*Sprites.taille + dif_affichage[0]  ,self.y*Sprites.taille + dif_affichage[1]))

class Gemme:

	def __init__(self,x,y):
		
		self.x=x
		self.y=y

		self.stun=randrange(4)+1
		self.dmg=randrange(4)+1

		
		
		self.color_circle=(randrange(120,255),randrange(120,255),randrange(120,255))
		
		self.nom="Gemme d'attaque" 
		self.sous_nom = "Étourd. : "+ str(self.stun) + ", Dégats :" + str(self.dmg)
	
	def use(self,joueur,screen):
		
		for i in range(len(joueur.niv.salle_active.ennemis)):
			joueur.niv.salle_active.ennemis[i].hit(self.dmg,self.stun,joueur)
		
		pg.draw.rect(screen,(self.color_circle),(0,0,15*Sprites.taille,15*Sprites.taille),Sprites.taille//2)
		pg.display.update()
		pg.time.delay(250)
		pg.draw.rect(screen,(0,0,0),(0,0,15*Sprites.taille,15*Sprites.taille),Sprites.taille//2)
		pg.display.update()
	
	def draw(self,screen,salle,show=False):
		dif_affichage = [0,0]
		if not show:
			dif_affichage = salle.dif_affichage
		pg.draw.circle(screen,(self.color_circle),( self.x * Sprites.taille + Sprites.taille//2 + dif_affichage[0] , self.y * Sprites.taille + Sprites.taille//2 + dif_affichage[1]),Sprites.taille//4,0)
		pg.draw.circle(screen,(200,200,200) ,( self.x * Sprites.taille + Sprites.taille//2+ dif_affichage[0], self.y * Sprites.taille + Sprites.taille // 2 + dif_affichage[1]),Sprites.taille//4,2)
		
