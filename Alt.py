import pygame as pg
from random import *
import Sprites
import Entites
# import Behold

captaille = 8
nsallesmax = 12
dimsalles = [(1,2),(1,3),(2,1),(2,2),(3,1)]

		

class Niveau:

	def __init__(self, niv : int):
		self.niv = niv
		self.w = self.h = 4 + (2 * (self.niv // 6))
		if self.w > captaille:
			self.w = self.h = captaille
		self.nsalles = 4 + (self.niv // 3)
		if self.nsalles > nsallesmax :
			self.nsalles = nsallesmax
		
		self.nobjets = self.nsalles-2
		
		self.salles = []
		
		self.carte = []
		self.carteblanche()
		
		self.randomap()
		self.map = pg.Surface((Sprites.taille*3,Sprites.taille*3))
		self.dispcarte()
		
		self.ind_salle_prev = 0
		self.ind_salle_active = 0
		
		
		self.salle_active = self.salles[self.ind_salle_active]
		
		self.salles[0].image_salle.blit(Sprites.spawn,(3*Sprites.taille,3*Sprites.taille))
		
		self.generer_ennemis()
		self.generer_objets()
		
		self.dif_affichage = [0,0]
		
		self.salles[0].objets.append(Entites.Potion(1,1,deb = True))
		
		
		
	def carteblanche(self):
		for i in range(self.h):
			self.carte.append([0] * self.w)
			
		
	def generer_ennemis(self):

		for i in range(len(self.salles)-1):
			self.nombre_ennemis = randrange((self.salles[i+1].l*self.salles[i+1].h) ,5)
			
			for j in range(self.nombre_ennemis):
				self.coords_ennemi = [randrange(2,len(self.salles[i+1].salle[0])-2), randrange(2,len(self.salles[i+1].salle)-2)]
				
				
				while not(self.salles[i+1].ennemi_placable(self.coords_ennemi[0],self.coords_ennemi[1])):
					self.coords_ennemi = [randrange(2,len(self.salles[i+1].salle[0])-1), randrange(2,len(self.salles[i+1].salle)-1)]
					

				
				self.salles[i+1].ennemis.append(Entites.Ennemi(self.coords_ennemi[0],self.coords_ennemi[1],self.salles[i]))

		
	def generer_objets(self):
		for i in range(self.nobjets):
			self.ind = self.carte[randrange(self.h)][randrange(self.w)]-1
			while self.ind <= 0:
				self.ind = self.carte[randrange(self.h)][randrange(self.w)]-1
			
			self.pos = [ randrange(1,len(self.salles[self.ind].salle[0])-2) , randrange(1,len(self.salles[self.ind].salle)-2) ]
			
			while not self.salles[self.ind].ennemi_placable(self.pos[0],self.pos[1]):
				self.pos = [randrange(1,len(self.salles[self.ind].salle[0])-2),randrange(1,len(self.salles[self.ind].salle)-2)]
		
			self.type = randrange(2)
		
			if self.type:
				self.salles[self.ind].objets.append(Entites.Potion(self.pos[0],self.pos[1]))
			else:
				self.salles[self.ind].objets.append(Entites.Gemme(self.pos[0],self.pos[1]))
				
	def randomap(self):
			
		self.dim_salle = (1,1)
		self.xi = randrange(self.w)
		self.yi = randrange(self.h)
		
		self.salles.append( Salle(self.dim_salle[0],self.dim_salle[1],self.xi,self.yi,self) ) 
		self.salles[0].salles_liees.append(1)
		
		self.carte[self.yi][self.xi] = 1
		
		self.refaire = 0
		for i in range(self.nsalles-1):
			
			self.bon = len(self.salles) 
			while self.bon <= len(self.salles): 
			
				self.ind = len(self.salles)-1
				self.salleprev = self.salles[self.ind]
				self.dir = randrange(4)
				
				self.s_l = 'x'
				self.s_h = 'x'
					
				self.xi = 'x'
				self.yi = 'x'
				
				while self.salleprev.haut and self.salleprev.bas and self.salleprev.gauche and self.salleprev.droite:
					self.ind = randrange(len(self.salles)) 
					self.salleprev = self.salles[self.ind]
				
				if self.dir == 0 :
					if self.salleprev.haut == False:
						self.construire_en_haut()
					else:
						self.dir += 1
						self.dir = self.dir%4
					
				if self.dir == 1 :
					if self.salleprev.gauche == False:
				
						self.construire_a_gauche()
						
					else:
						self.dir += 1
						self.dir = self.dir%4
				
				if self.dir == 2:
					if self.salleprev.bas == False:
						self.construire_en_bas()
					else:
						self.dir += 1
						self.dir = self.dir%4
					
					
				if self.dir == 3:  
					if self.salleprev.droite == False:
						self.construire_a_droite()
					else:
						self.dir += 1
						self.dir = self.dir%4
				
				if( self.xi + self.yi + self.s_l + self.s_h == 'xxxx'):
					self.refaire += 1
					
				if len(self.salles) > self.bon:
					self.salles[len(self.salles)-1].salles_liees.append(len(self.salles))
					break
			
		self.generer_escaliers()
		self.construire_portes()

	def construire_en_haut(self):
		
		self.dim_ideales = dimsalles[randrange(1,len(dimsalles))]
		
		self.s_l = min(self.w-1,self.salleprev.xi+self.dim_ideales[0]-1)+1 - self.salleprev.xi
		self.s_h = self.salleprev.yi - max(0,self.salleprev.yi-self.dim_ideales[1])
		
		self.xi = self.salleprev.xi
		self.yi = self.salleprev.yi - self.s_h
		
		self.deb = False
		self.fin_h = False
		self.repousse = 0
		self.redo = False

		for y in range(self.s_h):
			
			for x in range(self.s_l):
				
				if x >= self.s_l :
					break
				
				if self.carte[min(self.yi + self.s_h - 1 - y,self.h-1)][min(self.xi + x,self.w-1)]:

					if  self.deb == False: 

						self.repousse += 1
						self.xi += 1 

						if self.repousse > (self.salleprev.l) - 1 :
							self.salles[self.ind].haut = True
							return							
						else :
							
							while self.xi+self.s_l-1 >= self.w:
								self.s_l -=1

					else : 
						self.s_l = min(x,self.s_l)
				
					
				if self.xi + self.s_l - self.w-1 > 0:
					self.s_l -= (self.xi + self.s_l)-self.w-1
					
				if self.yi + self.s_h - 1 - y > 0:
					if self.carte[min(self.h-1,self.yi + self.s_h - 2 - y)][min(self.w-1,self.xi + x)]:
						self.fin_h = True
						self.s_h = y+1
				
				if self.carte[min(self.h-1,self.yi + self.s_h - 1 - y)][min(self.w-1,self.xi + x)] == 0 : 
					
					if self.deb == False:
						self.deb = True
					self.carte[min(self.h-1,self.yi + self.s_h - 1 - y)][min(self.w-1,self.xi + x)] = len(self.salles)+1
					
				if self.deb == False : 
					self.s_h == min(y+1,self.s_h)
					
			if self.fin_h == True:
				self.s_h = y+1
				break
			
			if self.redo:
				break
			
		if self.xi >= self.w or self.yi >= self.h or self.s_h <= 0 or self.s_l <= 0:
			self.salles[self.ind].haut = True
			self.corriger(len(self.salles)+1)
			return
		else:		
			if not self.redo:
				self.salles.append(Salle(self.s_l,self.s_h,self.xi,self.yi,self))
				self.salles[len(self.salles)-1].bas = True
			self.salles[self.ind].haut = True

	
	def construire_a_gauche(self):
	
		self.dim_ideales = dimsalles[randrange(1,len(dimsalles))]
					
		self.s_h = min(self.h-1,self.salleprev.yi+self.dim_ideales[1]-1)+1 - self.salleprev.yi
		self.s_l = self.salleprev.xi - max(0,self.salleprev.xi-self.dim_ideales[0])
		
		
		self.yi = self.salleprev.yi
		self.xi = self.salleprev.xi - self.s_l 
		
		self.deb = False
		self.fin_l = False
		self.repousse = 0
		self.redo = False

		for x in range(self.s_l):
			
			if x >= self.s_l:
				break
			
			if self.redo == True:
				break
			
			for y in range(self.s_h):
				
				if y >= self.s_h :
					break

				if self.carte[min(self.h-1,self.yi + y)][min(self.w-1,self.xi + self.s_l - 1 - x)]:

					if  self.deb == False: 
						self.repousse += 1
						
						if self.repousse > (self.salleprev.h) - 1 :
							self.salles[self.ind].gauche = True
							return			
						else :
							self.yi += 1
							if self.yi+self.s_h-1 >= self.h:
								self.s_h = y-1
								
					else : 
						self.s_h = min(y,self.s_h)
				
					
				if self.yi + self.s_h - self.h-1 > 0:
					self.s_h -= (self.yi + self.s_h)-self.h-1
					
				if self.xi + self.s_l - 1 - x > 0:
					if self.carte[min(self.h-1,self.yi + y)][self.xi + self.s_l - 2 - x]:
						self.fin_l = True
						self.xi = self.xi + self.s_l - 1 - x
						self.s_l = x+1
			
				if self.carte[min(self.h-1,self.yi + y)][self.xi + self.s_l - 1 - x] == 0 : 
					
					if self.deb == False:
						self.deb = True
					self.carte[min(self.h-1,self.yi + y)][self.xi + self.s_l - 1 - x] = len(self.salles)+1
					
			if self.fin_l == True:
				self.s_l = x+1
				break
				
			
			
		if self.xi >= self.w or self.yi >= self.h or self.s_h <= 0 or self.s_l <= 0:
			self.salles[self.ind].gauche = True
			self.corriger(len(self.salles)+1)
			return
		else:
			if not self.redo:
				self.salles.append(Salle(self.s_l,self.s_h,self.xi,self.yi,self))
				self.salles[len(self.salles)-1].droite = True
			self.salles[self.ind].gauche = True

	
	def construire_en_bas(self):
		
		self.dim_ideales = dimsalles[randrange(1,len(dimsalles))]	
		
		self.s_l = min(self.w-1,self.salleprev.xi+self.dim_ideales[0]-1)+1 - self.salleprev.xi
		self.s_h = min(self.h-1,self.salleprev.yi + self.salleprev.h+self.dim_ideales[1]-1)+1 - self.salleprev.yi - self.salleprev.h
	
		
		self.xi = self.salleprev.xi
		self.yi = self.salleprev.yi +self.salleprev.h
		
		self.deb = False
		self.fin_h = False
		self.redo = False
		self.repousse = 0

		for y in range(self.s_h):
			
			if y >= self.s_h :
				break
			
			for x in range(self.s_l):
				
				
				if x >= self.s_l:
					break
				
				if self.carte[min(self.yi + y,self.h-1)][min(self.xi + x,self.w-1)]:
					
					if  self.deb == False: 
						self.repousse += 1
						
						if self.repousse > (self.salleprev.l) - 1 :
							self.salles[self.ind].bas = True
							return 0				
						else :
							self.xi += 1 
							while self.xi+self.s_l-1 >= self.w:
								self.s_l -=1

					else : 
						self.s_l = min(x,self.s_l)
				 
					
				if self.xi + self.s_l  > self.w-1 :
					self.s_l = (self.xi + self.s_l)-self.w-1
					
				if self.yi + self.s_h - 1 > 0:
					if self.carte[min(self.yi + y,self.h-1)][min(self.w-1,self.xi + x+1)]:
						self.s_h = y+1
				
				if self.carte[min(self.h-1,self.yi + y)][min(self.w-1,self.xi + x)] == 0 : 
					
					if self.deb == False:
						self.deb = True
					self.carte[self.yi + y][self.xi + x] = len(self.salles)+1
					
			if self.fin_h == True:
				self.s_h = y+1
				break
			
			if self.redo == True:
				break
		
		if self.xi >= self.w or self.yi >= self.h or self.s_h <= 0 or self.s_l <= 0:
			self.salles[self.ind].bas = True
			self.corriger(len(self.salles)+1)
			return
		else:	
			if self.redo == False:
				self.salles.append(Salle(self.s_l,self.s_h,self.xi,self.yi,self))
				self.salles[len(self.salles)-1].haut = True
		self.salles[self.ind].bas = True

		
	
		
	def construire_a_droite(self):
			
			self.dim_ideales = dimsalles[randrange(1,len(dimsalles))]
						
			self.s_h = min(self.h-1,self.salleprev.yi+self.dim_ideales[1]-1)+1 - self.salleprev.yi
			self.s_l = min(self.w-1,self.salleprev.xi+self.salleprev.l+self.dim_ideales[0]-1)+1 - self.salleprev.xi - self.salleprev.l
			
			
			self.yi = self.salleprev.yi
			self.xi = self.salleprev.xi + self.salleprev.l 
			
			self.deb = False
			self.fin_l = False
			self.repousse = 0
			self.redo = False
			
			for x in range(self.s_l):
				
				for y in range(self.s_h):
					
					if y >= self.s_h:
						break
					
					if self.carte[min(self.h-1,self.yi + y)][min(self.w-1,self.xi + x)]:

						if  self.deb == False: 

							self.repousse += 1

							if self.repousse > (self.salleprev.h) - 1 :
								self.salles[self.ind].droite = True
								return			
							else :
								self.yi += 1
								if self.yi+self.s_h-1 >= self.h:
									self.s_h -=1

						else : 

							self.s_h = min(y,self.s_h)
					
						
					if self.yi + self.s_h - self.h > 0:
						self.s_h -= (self.yi + self.s_h)-self.h-1


					if self.xi + x < self.w-1:
						if self.carte[min(self.h-1,self.yi + y)][min(self.xi + x + 1,self.w-1)]:
							self.fin_l = True
							self.s_l = x+1
				
				

					if self.carte[min(self.h-1,self.yi + y)][min(self.w-1,self.xi + x)] == 0 : 
						
						if self.deb == False:
							self.deb = True
						self.carte[min(self.h-1,self.yi + y)][self.xi + x] = len(self.salles)+1
						
				if self.fin_l == True:
					self.s_l = x+1
					break
					
				if self.redo:	
					break
					
				if x >= self.s_l:
					break
			
			if self.xi >= self.w or self.yi >= self.h or self.s_h <= 0 or self.s_l <= 0:
				self.salles[self.ind].droite = True
				self.corriger(len(self.salles)+1)
				return
			else:
				if not self.redo:
					self.salles.append(Salle(self.s_l,self.s_h,self.xi,self.yi,self))
					self.salles[len(self.salles)-1].gauche = True
				self.salles[self.ind].droite = True
	
	def corriger(self, x ):
		for i in range(self.w):
			for j in range(self.h):
				if self.carte[j][i] == x:
					self.carte[j][i] = 0

		
	def construire_portes(self):
		for salle in self.salles:
			for i in range(salle.l):
				for j in range(salle.h):
			
					if self.carte[max(0,salle.yi+j-1)][salle.xi+i] not in salle.salles_liees:
						salle.salle[0][i*salle.taille_unite + salle.taille_unite//2] = 1
						salle.salles_liees.append(self.carte[max(0,salle.yi+j-1)][salle.xi+i])
					
					if self.carte[min(self.h-1,salle.yi+j+1)][salle.xi+i] not in salle.salles_liees:
						salle.salle[salle.h*salle.taille_unite-1][i*salle.taille_unite + salle.taille_unite//2] = 1
						salle.salles_liees.append(self.carte[min(self.h-1,salle.yi+j+1)][salle.xi+i])
		
					if self.carte[salle.yi+j][max(0,salle.xi+i-1)] not in salle.salles_liees:
						salle.salle[j*salle.taille_unite + salle.taille_unite//2][0] = 1
						salle.salles_liees.append(self.carte[salle.yi+j][max(0,salle.xi+i-1)])
					
					if self.carte[salle.yi+j][min(self.w-1,salle.xi+i+1)] not in salle.salles_liees:
						salle.salle[j*salle.taille_unite + salle.taille_unite//2][salle.l*salle.taille_unite - 1] = 1
						salle.salles_liees.append(self.carte[salle.yi+j][min(self.w-1,salle.xi+i+1)])
				
				pass
			
			salle.creer_image_salle()

			
	def generer_escaliers(self):
		self.ind = 0
		while self.ind <= 3:
			self.ind = self.carte[randrange(0,self.w)][randrange(0,self.h)]
		
		self.coords_escalier = (len(self.salles[self.ind-1].salle[0])//2, len(self.salles[self.ind-1].salle)//2 )
		
		self.salles[self.ind-1].salle[self.coords_escalier[1]][self.coords_escalier[0]] = 3
		
		
	def dispcarte(self):
	
		couleurs = [(255,0,16),(0,117,220),(43,206,72),(255,255,0),(255,164,5),(240,163,255),(94,241,242),(157,204,0),(194,0,136),
		(153,63,0),(148,255,181),(116,10,255)]
		
				
		for i in range(self.h):
			for j in range(self.w):
				if not self.carte[i][j] :
					pg.draw.rect(self.map,(0,0,0),(j*Sprites.taille,i*Sprites.taille,Sprites.taille,Sprites.taille))
				else:
					try :
						pg.draw.rect(self.map,couleurs[self.carte[i][j] - 1],(j*Sprites.taille*3//self.w+1,i*Sprites.taille*3//self.h+1,Sprites.taille*3//self.w - 2,Sprites.taille*3//self.h - 2))
					except IndexError:
						pass
	
class Salle:
	def __init__(self,l,h,xi,yi,niv : Niveau):
	
		if l == h == 1:
			self.taille_unite = 7
		else :
			self.taille_unite = 5
		
		self.haut = self.bas = self.gauche = self.droite = False
		
		self.xi = xi
		self.yi = yi
		
		self.haut = self.yi == 0
		self.gauche = self.xi == 0
		self.droite = (self.xi + l - 1)==(niv.w-1)
		self.bas = (self.yi + h - 1)==(niv.h-1)		
	
		self.entouree = self.haut and self.bas and self.gauche and self.droite
			
		self.l = l
		self.h = h
		
		self.salle = []
		self.salles_liees = [0]
		self.salles_liees.append(niv.carte[self.yi][self.xi])
		self.ennemis = []
		self.objets = []
		
		self.salleblanche()
		self.image_salle = pg.Surface((Sprites.taille * (self.l * self.taille_unite) , Sprites.taille * self.h * self.taille_unite ))
		
		self.dif_affichage = [15*Sprites.taille//2 - (self.image_salle.get_width()//2),15*Sprites.taille//2 - (self.image_salle.get_height()//2)]
		
		self.triggered = False
		
		
	def tick(self,joueur,screen):
		
		for ennemi in self.ennemis:
			if not self.triggered:
				self.triggered = True
				break
			if ennemi.visible:
				ennemi.tick(joueur,screen)
			
			
	def aff(self,ecran : pg.Surface):
	

		ecran.blit(self.image_salle,(self.dif_affichage[0],self.dif_affichage[1]))
		
		for objet in self.objets:
			objet.draw(ecran,self)
		
		for ennemi in self.ennemis:
			if ennemi.visible:
				ennemi.aff(ecran,self.dif_affichage)
		
		
	def ennemi_placable(self,x,y,generation = True):	
		for ennemi in self.ennemis:
			if ennemi.x == x and ennemi.y == y:
				return False
		
		if generation:
			if self.salle[y][x-1] == 1 or self.salle[y][x+1] == 1 or self.salle[y-1][x] == 1 or self.salle[y+1][x] == 1:
				return False
			if self.salle[y][x] == 3:
				return False
		else:
			pass
				
		return True

	def ennemi_ici(self,x,y):
		for ennemi in self.ennemis:
			if ennemi.x == x and ennemi.y == y:
				return self.ennemis.index(ennemi) + 1
		return 0
		
	def objet_ici(self,x,y):
		for i in range(len(self.objets)):
			if self.objets[i].x == x and self.objets[i].y == y:
				return i+1
		return 0
		
		
	def creer_image_salle(self):
		for x in range(self.l*self.taille_unite):
			for y in range(self.h*self.taille_unite):
				if x == 0 :
					if y == 0:
						self.image_salle.blit(Sprites.mur7,(x*Sprites.taille,y*Sprites.taille))
					elif y == self.h*self.taille_unite-1:
						self.image_salle.blit(Sprites.mur1,(x*Sprites.taille,y*Sprites.taille))
					else:
						self.image_salle.blit(Sprites.mur4,(x*Sprites.taille,y*Sprites.taille))
				elif x == self.l*self.taille_unite-1:
					if y == 0:
						self.image_salle.blit(Sprites.mur9,(x*Sprites.taille,y*Sprites.taille))
					elif y == self.h*self.taille_unite-1:
						self.image_salle.blit(Sprites.mur3,(x*Sprites.taille,y*Sprites.taille))
					else:
						self.image_salle.blit(Sprites.mur6,(x*Sprites.taille,y*Sprites.taille))
				else : 
					if y == 0:
						self.image_salle.blit(Sprites.mur8,(x*Sprites.taille,y*Sprites.taille))
					elif y == self.h*self.taille_unite-1:
						self.image_salle.blit(Sprites.mur2,(x*Sprites.taille,y*Sprites.taille))
					else:
						self.image_salle.blit(Sprites.sol,(x*Sprites.taille,y*Sprites.taille))
						
				if self.salle[y][x] == 1:
					if x == 0:
						self.image_salle.blit(Sprites.porte_droite,(x*Sprites.taille,y*Sprites.taille))
					if x == self.l*self.taille_unite-1:
						self.image_salle.blit(Sprites.porte_gauche,(x*Sprites.taille,y*Sprites.taille))
					if y == 0:
						self.image_salle.blit(Sprites.porte_bas,(x*Sprites.taille,y*Sprites.taille))
					if y == self.h*self.taille_unite-1:
						self.image_salle.blit(Sprites.porte_haut,(x*Sprites.taille,y*Sprites.taille))
						
				if self.salle[y][x] == 3:
					self.image_salle.blit(Sprites.escaliers,(x*Sprites.taille,y*Sprites.taille))			
	
	def salleblanche(self):
		for i in range(self.h * self.taille_unite):
			if i == 0 or i == self.h*self.taille_unite-1:
				self.salle.append( [2]*self.l*self.taille_unite )
			else:
				self.salle.append( [2]+(self.l*self.taille_unite-2)*[0]+[2] )
		pass

	
def texte_etage(screen,pl):
	police = pg.font.SysFont("Verdana",3*Sprites.taille//4)
	texte_etage = police.render("Etage "+str(pl.etage),1,(255,255,255))
	screen.blit(texte_etage,(2.5*Sprites.taille- texte_etage.get_width()//2 + 15*Sprites.taille, 0))
	
def barre_de_vie(screen,joueur):
	police = pg.font.SysFont("Verdana",2*Sprites.taille//3)
	texte_vie = police.render("Vie :",1,(255,255,255))
	screen.blit(texte_vie,(2.5*Sprites.taille- texte_vie.get_width()//2 + 15*Sprites.taille, Sprites.taille//2- texte_vie.get_height()//2 + 4*Sprites.taille))
	
	pg.draw.rect(screen,(255,15,25),(16*Sprites.taille, 5*Sprites.taille, 3*Sprites.taille, Sprites.taille) )
	
	pg.draw.rect(screen,(135,255,0),(16*Sprites.taille, 5*Sprites.taille, int(3*Sprites.taille*(joueur.vie/joueur.vie_max)), Sprites.taille) )
	pg.draw.rect(screen,(85,195,0),(16*Sprites.taille, 5*Sprites.taille, int(3*Sprites.taille*(joueur.vie/joueur.vie_max)), Sprites.taille),Sprites.taille//15 )
	
	
	pg.draw.rect(screen,(80,80,80),(16*Sprites.taille, 5*Sprites.taille, 3*Sprites.taille, Sprites.taille),Sprites.taille//10 )
	
	police = pg.font.SysFont("Verdana",Sprites.taille//2)
	texte_vie = police.render(str(joueur.vie)+" / "+str(joueur.vie_max),1,(0,0,0))
	screen.blit(texte_vie,(2.5*Sprites.taille- texte_vie.get_width()//2 + 15*Sprites.taille, Sprites.taille//2- texte_vie.get_height()//2 + 5*Sprites.taille))
	
def sac_a_dos(screen,joueur):
	police = pg.font.SysFont("Verdana",Sprites.taille//2)
	texte = police.render("Objet selectionné :",1,(255,255,255))
	screen.blit(texte,(15*Sprites.taille+ 2.5*Sprites.taille- texte.get_width()//2 , 6*Sprites.taille + Sprites.taille//2 -  texte.get_height()//2 ))
	
	if len(joueur.objets) == 0:
		police = pg.font.SysFont("Verdana",Sprites.taille)
		texte = police.render("X",1,(255,0,0))
		screen.blit(texte,(15*Sprites.taille + 2.5*Sprites.taille- texte.get_width()//2 , 7*Sprites.taille + Sprites.taille//2 -  texte.get_height()//2 ))
		police = pg.font.SysFont("Verdana",Sprites.taille//2)
		texte = police.render("Aucun",1,(255,255,255))
		screen.blit(texte,(15*Sprites.taille+ 2.5*Sprites.taille- texte.get_width()//2 , 8*Sprites.taille + Sprites.taille//2 -  texte.get_height()//2 ))
	else:
		joueur.objets[joueur.pos_sac].draw(screen,joueur.niv.salle_active,show=True)
		texte = police.render(joueur.objets[joueur.pos_sac].nom,1,(255,255,255))
		screen.blit(texte,(15*Sprites.taille+ 2.5*Sprites.taille- texte.get_width()//2 , 8*Sprites.taille + Sprites.taille//2 -  texte.get_height()//2 ))
		police = pg.font.SysFont("Verdana",Sprites.taille//4)
		texte = police.render(joueur.objets[joueur.pos_sac].sous_nom,1,(255,255,255))
		screen.blit(texte,(15*Sprites.taille+ 2.5*Sprites.taille- texte.get_width()//2 , 8.5*Sprites.taille + Sprites.taille//2 -  texte.get_height()//2 ))
		
	pg.draw.rect(screen,(250,250,130),(17*Sprites.taille,7*Sprites.taille,Sprites.taille,Sprites.taille),Sprites.taille//10)
	
def score(screen,joueur):
	police = pg.font.SysFont("Verdana",Sprites.taille//2)
	texte = police.render("Score : "+str(joueur.score),1,(255,255,255))
	screen.blit(texte,(15*Sprites.taille+ 2.5*Sprites.taille- texte.get_width()//2 , 9*Sprites.taille + Sprites.taille//2 -  texte.get_height()//2 ))
	police = pg.font.SysFont("Verdana",Sprites.taille//2)
	texte = police.render("[F] : Plein ecran",1,(255,255,255))
	screen.blit(texte,(15*Sprites.taille + 2.5*Sprites.taille - texte.get_width()//2 ,10*Sprites.taille + 2*Sprites.taille -  texte.get_height()//2 ))
	texte = police.render("[ECHAP] : Quitter",1,(255,255,255))
	screen.blit(texte,(15*Sprites.taille + 2.5*Sprites.taille - texte.get_width()//2 ,11*Sprites.taille + 2*Sprites.taille -  texte.get_height()//2 ))
	
	
def texte_mort(screen,joueur):
	
	police = pg.font.SysFont("Verdana",Sprites.taille*2)
	texte = police.render("Vous êtes mort!!!",1,(255,0,0))
	screen.blit(texte,(10*Sprites.taille - texte.get_width()//2 , 5*Sprites.taille -  texte.get_height()//2 ))
	
	police = pg.font.SysFont("Verdana",Sprites.taille//2)
	texte = police.render(Sprites.nom_joueur+" est mort à l'Etage "+str(joueur.etage)+" avec un score de "+str(joueur.score)+".",1,(255,255,255))
	screen.blit(texte,(10*Sprites.taille - texte.get_width()//2 ,10*Sprites.taille + 2*Sprites.taille -  texte.get_height()//2 ))
	texte = police.render("Appuyez sur [espace] pour recommencer, [échap] pour quitter le jeu.",1,(255,255,255))
	screen.blit(texte,(10*Sprites.taille - texte.get_width()//2 ,12*Sprites.taille + 2*Sprites.taille -  texte.get_height()//2 ))
	
	
	
def visualisation():
	running = True
	pg.init()
	pl = Entites.Player(3,3)
	
	
	fullscreen = False
	screen = pg.display.set_mode((20*Sprites.taille,15*Sprites.taille))
	pg.display.set_caption("Gudomellig")
	cl = pg.time.Clock()
	cd = False
	
	
	while running:
	
		for event in pg.event.get():
			if event.type == pg.QUIT :
				running = False
	
		ctrl = pg.key.get_pressed()
		if ctrl[pg.K_ESCAPE]:
			running = False
		if ctrl[pg.K_f] and not fullscreen:
				screen = pg.display.set_mode((20*Sprites.taille,15*Sprites.taille),pg.FULLSCREEN)
		if ctrl[pg.K_SPACE] and pl.mort:
		
			pl = Entites.Player(3,3)
			
		cl.tick(60)
		
		screen.fill((0,0,0))
		pg.draw.rect(screen,(128,128,128),(15*Sprites.taille,0,5*Sprites.taille,15*Sprites.taille))
		
		pl.niv.salle_active.aff(screen)
		texte_etage(screen,pl)
		barre_de_vie(screen,pl)
		screen.blit(pl.niv.map,((16*Sprites.taille ,Sprites.taille)))
		sac_a_dos(screen,pl)
		score(screen,pl)
		
		pg.draw.rect(screen,(255,255,255),(16*Sprites.taille + pl.niv.salle_active.xi*(Sprites.taille*3//pl.niv.w),Sprites.taille + pl.niv.salle_active.yi*(Sprites.taille*3//pl.niv.w),pl.niv.salle_active.l*(Sprites.taille*3//pl.niv.w)-1,pl.niv.salle_active.h*(Sprites.taille*3//pl.niv.w)-1),2)
		
		
		if not pl.mort:
			pl.tick(screen)
			
			pl.render(screen)
			
			if not pl.tour:
				pl.niv.salle_active.tick(pl,screen)
				pl.tour = True
			
		else:
			screen.fill((0,0,0))
			texte_mort(screen,pl)
		
		
		pg.display.update()
	
	quit()
	

# visualisation()