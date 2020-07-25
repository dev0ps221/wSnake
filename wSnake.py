#!/usr/bin/python3.7
#coding:utf-8
import pygame
import random
import time
#Un bloc du serpent
r = random.randrange
class MENU(pygame.sprite.Sprite):
    """docstring for MENU."""
    def voirChoix(self):
        self.actuel = self.tabOptions[self.indiceActuel]
        self.genererOptions()
    def genererOptions(self):
        font = pygame.font.SysFont("Arial",50)
        self.options ={
            "play" : {
                "image":font.render("*Jouer" if (self.actuel=="Jouer") else "Jouer",True,self.couleurs["selectionnee"] if (self.actuel=="Jouer") else self.couleurs["normale"]),
                "rect":((self.rect.width)/3,(self.rect.height)/3),
                "valeur":"jouer"
            },
            "options" : {
                "image":font.render("*Options" if (self.actuel=="Options") else "Options",True,self.couleurs["selectionnee"] if (self.actuel=="Options") else self.couleurs["normale"]),
                "rect":((self.rect.width)/3,((self.rect.height)/3)+(60)),
                "valeur":"options"
            },
            "exit" : {
                "image":font.render("*Quitter" if (self.actuel=="Quitter") else "Quitter",True,self.couleurs["selectionnee"] if (self.actuel=="Quitter") else self.couleurs["normale"]),
                "rect":((self.rect.width)/3,((self.rect.height)/3)+(120)),
                "valeur":"quitter"
            }
        }
        for option in self.options:
            self.image.blit(self.options[option]['image'],self.options[option]['rect'])
    def __init__(self, rect):
        super(MENU, self).__init__()
        self.image = pygame.Surface([rect.width,rect.height]);
        self.rect = self.image.get_rect()
        self.image.fill((0,0,0))
        self.couleurs={
            "normale":(250,200,200),
            "selectionnee":(55,250,80)
        }
        self.tabOptions=[
            "Jouer",
            "Options",
            "Quitter"
        ]
        self.choixMenu = "still"
        self.indiceActuel = 0
class Bloc (pygame.sprite.Sprite):
    def __init__(self,position,taille_segment,taille="defaut"):
        super().__init__()
        if(taille!="defaut"):self.image = pygame.Surface([taille,taille])
        else:self.image = pygame.Surface([taille_segment,taille_segment])
#        self.image.fill((255,255,100))
        self.image.fill(((255),(255),(255)))
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = position
    def touche(self, sprite):
        return self.rect.colliderect(sprite.rect)
class Nourriture(Bloc):
    def __init__(self,position,taille="defaut"):
        super().__init__(position,taille)
        self.image.fill((205,255,25))
def jouer(menu):
    #le serpent
    mue = False
    position={"x":0,"y":0}
    taille_segment = 14
    marge = 1
    segments_serpent = []
    serpent = pygame.sprite.Group()
    x,y = position["x"],position["y"] = 60,60
    for n in range(3):
        x = x + (taille_segment )
        bloc = Bloc((x,y),taille_segment)
        segments_serpent.insert(0,bloc)
        serpent.add(bloc)
    #la Nourriture
    tab_nourriture = []
    nourriture = pygame.sprite.Group()
    #Le Jeu

    fini = False
    sens = "droite"
    clock = pygame.time.Clock()
    prises = 0
    fps = 8
    vitesse = 1
    nscore = 0
    while not fini:
        if len(segments_serpent)==32:
            mue = True
            taille_segment=12
        if(len(segments_serpent)==64):
            mue = (True)
            taille_segment=10
        if(len(segments_serpent)==96):
            mue = (True)
            taille_segment=8
        width = ecran.get_rect().width
        height = ecran.get_rect().height
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                fini = True
            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_LEFT:
                    if sens != "droite" : sens = "gauche"
                if evenement.key == pygame.K_RIGHT:
                    if sens != "gauche" : sens = "droite"
                if evenement.key == pygame.K_UP:
                    if sens != "bas" : sens = "haut"
                if evenement.key == pygame.K_DOWN:
                    if sens != "haut" : sens = "bas"
                if evenement.key == pygame.K_RETURN:
                    while True:
                        event = pygame.event.wait()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            break
        if len(nourriture)==0:
            tab_nourriture,nourriture=genererNourriture(taille_segment,tab_nourriture,nourriture)
        plusX = 0
        plusY = 0
        if sens == "gauche":
            if segments_serpent[0].rect.x == 0 :
                fini = True
            else:
                plusX = (taille_segment ) * -1
                plusY = 0
        if sens == "droite":
            if segments_serpent[0].rect.x >= width-(taille_segment) :
                fini = True
            else:
                plusX = (taille_segment )
                plusY = 0
        if sens == "haut":
            if segments_serpent[0].rect.y == 0 :
                fini = True
            else:
                plusX = 0
                plusY = (taille_segment ) * -1
        if sens == "bas":
            if segments_serpent[0].rect.y >= height-(taille_segment) :
                fini = True
                time.sleep(5)
            else:
                plusX = 0
                plusY = (taille_segment )
        ancien = segments_serpent.pop()
        serpent.remove(ancien)
        position['x'] = segments_serpent[0].rect.x + plusX
        position['y'] = segments_serpent[0].rect.y + plusY
        bloc = Bloc((position['x'],position['y']),taille_segment)
        segments_serpent.insert(0,bloc)
        serpent.add(bloc)
        serpent.update()
        ecran.fill((50,0,50))
        # ecran.fill((12,12,24))
        serpent.draw(ecran)
        nourriture.update()
        nourriture.draw(ecran)
        font = pygame.font.Font('freesansbold.ttf', 16)
        score = font.render("score: "+str(nscore),True,(0,255,0),(12,12,24))
        rectScore = score.get_rect()
        rectScore.x = 0
        rectScore.y = 0
        ecran.blit(score,rectScore)
        pygame.display.flip()
        if segments_serpent[0].touche(tab_nourriture[0]):
            prises,fps,nscore,segments_serpent,taille_segment,marge,serpent,nourriture,tab_nourriture,vitesse = manger(sens,prises,fps,nscore,segments_serpent,taille_segment,marge,serpent,nourriture,tab_nourriture,vitesse)
        for segment in segments_serpent:
            if segment != segments_serpent[0]:
                if segments_serpent[0].touche(segment) :
                    fini = True if segments_serpent[0].rect.width == segment.rect.width else False
                    mue = False
        if fini == True :
            menu.choixMenu = "still"
            print(menu.choixMenu)
        clock.tick(fps)
def menu(ecran,jouer):
    menu = MENU(ecran.get_rect())
    quitter = False
    while not quitter:
        ecran.fill((0,0,0))
        menu.image.fill((0,0,0))
        menu.voirChoix()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quitter = True
            if e.type == pygame.KEYDOWN :
                if e.key == pygame.K_DOWN:
                    menu.indiceActuel+=1
                if e.key == pygame.K_UP:
                    menu.indiceActuel+=1 * (-1)
                if e.key == pygame.K_RETURN :
                    menu.choixMenu = menu.tabOptions[menu.indiceActuel]
        if menu.choixMenu is "still" :
            ecran.blit(menu.image,menu.rect)
        elif menu.choixMenu is "Jouer":
            jouer(menu)
        else :
            quitter = True
        pygame.display.flip()
def genererNourriture(taille_segment,tab_nourriture,nourriture):
    x = random.randrange(15,width-taille_segment)
    y = random.randrange(15,height-taille_segment)
    nourr = Nourriture((x,y),int(taille_segment/2))
    tab_nourriture.append(nourr)
    nourriture.add(nourr)
    return tab_nourriture,nourriture
def manger(sens,prises,fps,nscore,segments_serpent,taille_segment,marge,serpent,nourriture,tab_nourriture,vitesse):
    if prises == 8:
        prises = 0
        vitesse+=1
        fps+=1
    else:
        prises+=1
    if sens == "gauche":
        x = segments_serpent[len(segments_serpent)-1].rect.x + (((taille_segment)*vitesse ) * -1)
        y = segments_serpent[len(segments_serpent)-1].rect.y
    if sens == "droite":
        x = segments_serpent[len(segments_serpent)-1].rect.x + (((taille_segment)*vitesse ))
        y = segments_serpent[len(segments_serpent)-1].rect.y
    if sens == "haut":
        y = segments_serpent[len(segments_serpent)-1].rect.y + (((taille_segment)*vitesse ) * -1)
        x = segments_serpent[len(segments_serpent)-1].rect.x
    if sens == "bas":
        y = segments_serpent[len(segments_serpent)-1].rect.y + (((taille_segment)*vitesse ))
        x = segments_serpent[len(segments_serpent)-1].rect.x
    bloc = Bloc((x,y),taille_segment)
    segments_serpent.append(bloc)
    serpent.add(bloc)
    nourr = tab_nourriture.pop()
    nourriture.remove(nourr)
    nscore+=3
    return prises,fps,nscore,segments_serpent,taille_segment,marge,serpent,nourriture,tab_nourriture,vitesse
#on commence :)
pygame.init()
pygame.display.set_caption("xSnake v1.0.1 - Tek-Tech 2020")
#L'ecran
width = 400
height = 400
ecran = pygame.display.set_mode((width,height))#,pygame.FULLSCREEN
menu(ecran,jouer)
pygame.quit()
