import random
from random import randint
import sqlite3
import pygame
from pygame.locals import *
from datetime import datetime
pygame.font.init()


class Question(): #Classe question qui crree des objets questions avec intitulé, reponses etc
    def __init__(self,q,r1,r2,r3,r4,r,explication):
        self.q=q
        self.r1=r1
        self.r2=r2
        self.r3=r3
        self.r4=r4
        self.r=r
        self.explication=explication

    def getQuestion(self):
        return self.q

    def getReponses(self):
        return [self.r1,self.r2,self.r3,self.r4]

    def getBonneReponse(self) :
        return self.r

def creer_connexion(fichier) : #Utilisée dans la premiere partie du programme, la connexion  la base de donnée
    '''Créé une connection à partir de 'fichier', un fichier de base de données'''
    connexion = sqlite3.connect(fichier)
    curseur = connexion.cursor()
    return curseur

def listeElements():#renvoie une liste de 16 objects questions (15 + 1 swipe), puis 4 personnes (appel à un ami)
    curseur=creer_connexion("assets/Db/HP.db")
    curseur.execute("SELECT COUNT(*) FROM Questions;")
    nb_questions=curseur.fetchall()
    liste_nombres=random.sample(range(nb_questions[0][0]-1), 16)
    liste_elements=[]
    for i in liste_nombres:
        j=i+1
        curseur.execute("SELECT Question, r1, r2, r3, r4, r, Explication FROM Questions WHERE id="+str(j)+";")
        infos=curseur.fetchall()[0]
        liste_elements.append(Question(infos[0],infos[1],infos[2],infos[3],infos[4],infos[5],infos[6]))

    curseur.execute("SELECT COUNT(*) FROM PersosAmis;")
    nb_persos=curseur.fetchall()
    liste_nombres=random.sample(range(nb_persos[0][0]-1), 4)
    for i in liste_nombres:
        j=i+1
        curseur.execute("SELECT Nom FROM PersosAmis WHERE id_perso="+str(j)+";")
        infos=curseur.fetchall()[0][0]
        liste_elements.append(infos)
    return liste_elements

liste_elements=listeElements() #Une liste renvoyée par listeElements
##for i in liste_elements :
##    if type(i)==Question :
##        print(i.getQuestion())
##    else :
##        print(i)

#On définit la fenetre
etat=0          #0=Accueil // 1=Question a poser // 2=Question posée // 3=Question posée et BONUS utilisé // 4=PERRDU a parametrer // 5= sortie avec gain ou perdu affichée // 6=Sortie a parametrer
niveau=0
gain=['0','0'] # liste des gains : gain actuel, dernier pallier
liste_gains=['100','200','300','500','1.000','2.000','4.000','8.000','12.000','24.000','36.000','72.000','150.000','300.000','1.000.000']
pygame.init()
liste_reponses_dispo=[1,2,3,4] # Contient les reponses dispo, utilisée pour ne pas affichée la ligne en 50/50
icon_32x32 = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon_32x32)
pygame.display.set_caption('Qui Veut Gagner Des Gallions ?')
pygame.mixer.init()
pygame.mixer.music.load("assets/Hedwigs Theme Flute.mp3")
pygame.mixer.music.play(-1)
#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((1380, 920))

#Chargement et collage du fond
fond = pygame.image.load("assets/Fond_VIDE.png").convert()
fenetre.blit(fond, (0,0))

#Chargement et collage du titre, bouton etc
titre = pygame.image.load("assets/Titre.png")
pos_titre=titre.get_rect()
fenetre.blit(titre, pos_titre)
pos_titre = pos_titre.move(198,250)

jouer = pygame.image.load("assets/Bouton Jouer.png")
pos_jouer=jouer.get_rect()
fenetre.blit(jouer, pos_jouer)
pos_jouer=pos_jouer.move(583,450)



#Chargement et collage des bonus
appel = pygame.image.load("assets/Tel_ON.png") #On charge l'image
pos_appel=appel.get_rect() #On enregistre sa position
fenetre.blit(appel, pos_appel) #On affiche
pos_appel = pos_appel.move(2000,2000) #On augmente ses x et y
valeur_appel=1 #1=dispo // 0=Pas dispo
def utilisationAppel(): #Quand il est dispo et on clique dessus
    global appel
    global valeur_appel
    global etat
    etat=3 #On passe a l'état global 3
    appel = pygame.image.load("assets/Tel_OFF.png") #On recréer l'objet avec l'image off
    valeur_appel-=1 #on passe sa valeur à 00
    global texteDemandeAppel, textePerso1, textePerso2, textePerso3, textePerso4, str_demandeAppel, str_demandePerso1, str_demandePerso2, str_demandePerso3, str_demandePerso4, pos_demande_appel, pos_perso1, pos_perso2, pos_perso3, pos_perso4
    str_demandeAppel='Qui voulez vous appeler ?'
    texteDemandeAppel=PoliceQuestion.render(str_demandeAppel,1,(249,235,223)) #On creer nos textes qui contiendront la demande et les noms
    pos_demande_appel=texteDemandeAppel.get_rect()
    pos_demande_appel.centerx=569
    pos_demande_appel.y=625

    str_demandePerso1=liste_elements[16]
    textePerso1=PoliceReponses.render(str_demandePerso1,1,(249,235,223))
    pos_perso1=textePerso1.get_rect()
    pos_perso1.centerx=569
    pos_perso1.y=675

    str_demandePerso2=liste_elements[17]
    textePerso2=PoliceReponses.render(str_demandePerso2,1,(249,235,223))
    pos_perso2=textePerso2.get_rect()
    pos_perso2.centerx=569
    pos_perso2.y=725

    str_demandePerso3=liste_elements[18]
    textePerso3=PoliceReponses.render(str_demandePerso3,1,(249,235,223))
    pos_perso3=textePerso3.get_rect()
    pos_perso3.centerx=569
    pos_perso3.y=775

    str_demandePerso4=liste_elements[19]
    textePerso4=PoliceReponses.render(str_demandePerso4,1,(249,235,223))
    pos_perso4=textePerso4.get_rect()
    pos_perso4.centerx=569
    pos_perso4.y=825

public = pygame.image.load("assets/Public_ON.png") #ANALOGUE A APPEL
pos_public=public.get_rect()
fenetre.blit(public, pos_public)
pos_public = pos_public.move(2000,2000)
valeur_public=1
def utilisationPublic():
    global public
    global valeur_public
    global etat
    etat=3
    public = pygame.image.load("assets/Public_OFF.png")
    valeur_public-=1

moitie = pygame.image.load("assets/50_ON.png")#ANALOGUE A APPEL
pos_moitie=moitie.get_rect()
fenetre.blit(moitie, pos_moitie)
pos_moitie = pos_moitie.move(2000,2000)
valeur_moitie=1
def utilisationMoitie():
    global moitie
    global valeur_moitie
    global etat
    global liste_reponses_dispo
    etat=3
    moitie = pygame.image.load("assets/50_OFF.png")
    valeur_moitie-=1
    global texteReponse1, texteReponse2, texteReponse3, texteReponse4, pos_question, pos_reponse1, pos_reponse2, pos_reponse3, pos_reponse4
    global niveau
    bonne_reponse=liste_elements[niveau-1].getBonneReponse()
    autre_reponse=randint(1,4)
    while autre_reponse==bonne_reponse:
        autre_reponse=randint(1,4)
    liste_reponses_a_garder=[bonne_reponse,autre_reponse]
    liste_reponses_dispo=liste_reponses_a_garder
    for i in range(1,5):
        if not i in liste_reponses_a_garder:
            if i==1:
                texteReponse1=PoliceReponses.render('',1,(249,235,223))
            if i==2:
                texteReponse2=PoliceReponses.render('',1,(249,235,223))
            if i==3:
                texteReponse3=PoliceReponses.render('',1,(249,235,223))
            if i==4:
                texteReponse4=PoliceReponses.render('',1,(249,235,223))



swipe = pygame.image.load("assets/Swipe_ON.png")#ANALOGUE A APPEL
pos_swipe=swipe.get_rect()
fenetre.blit(swipe, pos_swipe)
pos_swipe = pos_swipe.move(2000,2000)
valeur_swipe=1
def utilisationSwipe():
    global swipe
    global valeur_swipe
    global etat
    etat=3
    swipe = pygame.image.load("assets/Swipe_OFF.png")
    valeur_swipe-=1
    global texteQuestion, texteReponse1, texteReponse2, texteReponse3, texteReponse4, pos_question, pos_reponse1, pos_reponse2, pos_reponse3, pos_reponse4
    texteQuestion=PoliceQuestion.render(liste_elements[15].getQuestion(),1,(249,235,223)) #On recréer nos questions, réponses etc
    texteReponse1=PoliceReponses.render(liste_elements[15].getReponses()[0],1,(249,235,223))
    texteReponse2=PoliceReponses.render(liste_elements[15].getReponses()[1],1,(249,235,223))
    texteReponse3=PoliceReponses.render(liste_elements[15].getReponses()[2],1,(249,235,223))
    texteReponse4=PoliceReponses.render(liste_elements[15].getReponses()[3],1,(249,235,223))
    pos_question=texteQuestion.get_rect()
    pos_question.y=250 #On centre notre question
    pos_question.centerx=690
    pos_reponse1=texteReponse1.get_rect()
    pos_reponse1.y=350
    pos_reponse1.centerx=690
    pos_reponse2=texteReponse2.get_rect()
    pos_reponse2.y=400
    pos_reponse2.centerx=690
    pos_reponse3=texteReponse3.get_rect()
    pos_reponse3.y=450
    pos_reponse3.centerx=690
    pos_reponse4=texteReponse4.get_rect()
    pos_reponse4.y=500
    pos_reponse4.centerx=690









sortie = pygame.image.load("assets/Sortie_ON.png")#ANALOGUE A APPEL
pos_sortie=sortie.get_rect()
fenetre.blit(sortie, pos_sortie)
pos_sortie = pos_sortie.move(2000,2000)


carre = pygame.image.load("assets/Carre.png")#ANALOGUE A APPEL
pos_carre=carre.get_rect()
fenetre.blit(carre, pos_carre)
pos_carre = pos_carre.move(2000,2000)


PoliceQuestion=pygame.font.Font("assets/HARRYP__.TTF",50) #On definit une police pour les questions et une pour les reponses
PoliceReponses=pygame.font.Font("assets/HARRYP__.TTF",35)

texteQuestion=PoliceQuestion.render('',1,(249,235,223)) #On creer nos textes qui contiendront les questions et reponses
texteReponse1=PoliceReponses.render('',1,(249,235,223))
texteReponse2=PoliceReponses.render('',1,(249,235,223))
texteReponse3=PoliceReponses.render('',1,(249,235,223))
texteReponse4=PoliceReponses.render('',1,(249,235,223))
pos_question=texteQuestion.get_rect() #On creer une variable qui contiendra les positions des questions et reponses
pos_reponse1=texteReponse1.get_rect()
pos_reponse2=texteReponse2.get_rect()
pos_reponse3=texteReponse3.get_rect()
pos_reponse4=texteReponse4.get_rect()

str_demandeAppel=''
texteDemandeAppel=PoliceQuestion.render(str_demandeAppel,1,(249,235,223)) #On creer nos textes qui contiendront la demande et les noms
str_demandePerso1=''
textePerso1=PoliceReponses.render(str_demandePerso1,1,(249,235,223))
str_demandePerso2=''
textePerso2=PoliceReponses.render(str_demandePerso2,1,(249,235,223))
str_demandePerso3=''
textePerso3=PoliceReponses.render(str_demandePerso3,1,(249,235,223))
str_demandePerso4=''
textePerso4=PoliceReponses.render(str_demandePerso4,1,(249,235,223))
pos_demande_appel=texteDemandeAppel.get_rect() #On creer une variable qui contiendra les positions de la demande et des noms
pos_perso1=textePerso1.get_rect()
pos_perso2=textePerso2.get_rect()
pos_perso3=textePerso3.get_rect()
pos_perso4=textePerso4.get_rect()
pos_demande_appel.centerx=569
pos_demande_appel.y=625
pos_perso1.centerx=569
pos_perso1.y=675
pos_perso2.centerx=569
pos_perso2.y=725
pos_perso3.centerx=569
pos_perso3.y=775
pos_perso4.centerx=569
pos_perso4.y=825


def poserQuestion(): #Quand on doit poser une questions
    global etat
    global niveau
    global liste_reponses_dispo
    global texteQuestion, texteReponse1, texteReponse2, texteReponse3, texteReponse4, pos_question, pos_reponse1, pos_reponse2, pos_reponse3, pos_reponse4
    liste_reponses_dispo=[1,2,3,4]
    niveau=niveau+1 #On augment le niveau de 1
    etat=2 #On change l état global à 'Questtion posée'
    texteQuestion=PoliceQuestion.render(liste_elements[niveau-1].getQuestion(),1,(249,235,223)) #On recréer nos questions, réponses etc
    texteReponse1=PoliceReponses.render(liste_elements[niveau-1].getReponses()[0],1,(249,235,223))
    texteReponse2=PoliceReponses.render(liste_elements[niveau-1].getReponses()[1],1,(249,235,223))
    texteReponse3=PoliceReponses.render(liste_elements[niveau-1].getReponses()[2],1,(249,235,223))
    texteReponse4=PoliceReponses.render(liste_elements[niveau-1].getReponses()[3],1,(249,235,223))
    pos_question=texteQuestion.get_rect()
    pos_question.y=250 #On centre notre question
    pos_question.centerx=690

    pos_reponse1=texteReponse1.get_rect()
    pos_reponse1.y=350
    pos_reponse1.centerx=690
    pos_reponse2=texteReponse2.get_rect()
    pos_reponse2.y=400
    pos_reponse2.centerx=690
    pos_reponse3=texteReponse3.get_rect()
    pos_reponse3.y=450
    pos_reponse3.centerx=690
    pos_reponse4=texteReponse4.get_rect()
    pos_reponse4.y=500
    pos_reponse4.centerx=690

    global texteDemandeAppel, textePerso1, textePerso2, textePerso3, textePerso4, str_demandeAppel, str_demandePerso1, str_demandePerso2, str_demandePerso3, str_demandePerso4
    str_demandeAppel=''
    texteDemandeAppel=PoliceQuestion.render(str_demandeAppel,1,(249,235,223)) #On creer nos textes qui contiendront la demande et les noms
    str_demandePerso1=''
    textePerso1=PoliceReponses.render(str_demandePerso1,1,(249,235,223))
    str_demandePerso2=''
    textePerso2=PoliceReponses.render(str_demandePerso2,1,(249,235,223))
    str_demandePerso3=''
    textePerso3=PoliceReponses.render(str_demandePerso3,1,(249,235,223))
    str_demandePerso4=''
    textePerso4=PoliceReponses.render(str_demandePerso4,1,(249,235,223))

def reponseJuste():
    global niveau
    global gain
    global etat
    gain[0]=liste_gains[niveau-1]
    if niveau%5==0 :
        gain[1]=liste_gains[niveau-1]
    if niveau==15:
        etat=4
    else :
        global pos_rond
        pos_rond = pos_rond.move(+0,-23)
        poserQuestion()


PointsQuestions = pygame.image.load("assets/Points.png")
pos_points_questions=PointsQuestions.get_rect()
pos_points_questions = pos_points_questions.move(2000,2000)
pos_points_questions.centerx=690


Rond = pygame.image.load("assets/Rond.png")
pos_rond=Rond.get_rect()
fenetre.blit(Rond, pos_rond)
pos_rond = pos_rond.move(2000,2000)

RondVert = pygame.image.load("assets/RondVert.png")
pos_rondvert=RondVert.get_rect()
fenetre.blit(RondVert, pos_rondvert)
pos_rondvert = pos_rondvert.move(2000,2000)

RondRouge = pygame.image.load("assets/RondRouge.png")
pos_rondrouge=RondRouge.get_rect()
fenetre.blit(RondRouge, pos_rondrouge)
pos_rondrouge = pos_rondrouge.move(2000,2000)


#Rafraîchissement de l'écran
pygame.display.flip()

#BOUCLE INFINIE
continuer = 1
while continuer==1:
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT :     #Si un de ces événements est de type QUIT
                continuer = 0      #On arrête la boucle
            if etat!=4 and etat!=5 and etat!=6: #Si pas perdu
                fenetre.blit(fond, (0,0))
                if etat!=0 : #Si il faut repondre à une question
                    coordonnées_souris=pygame.mouse.get_pos() #on recup les coordonnées de la souris
                    if pos_reponse1.topleft[0]<=coordonnées_souris[0]<=pos_reponse1.bottomright[0] and pos_reponse1.topleft[1]<=coordonnées_souris[1]<=pos_reponse1.bottomright[1] and 1 in liste_reponses_dispo:
                        pos_points_questions.centerx=690
                        pos_points_questions.y=pos_reponse1.bottom-20
                        if pygame.mouse.get_pressed()[0]==1:
                            if liste_elements[niveau-1].getBonneReponse()==1 :
                                reponseJuste()
                            else :
                                etat=4
                    elif pos_reponse2.topleft[0]<=coordonnées_souris[0]<=pos_reponse2.bottomright[0] and pos_reponse2.topleft[1]<=coordonnées_souris[1]<=pos_reponse2.bottomright[1] and 2 in liste_reponses_dispo:
                        pos_points_questions.centerx=690
                        pos_points_questions.y=pos_reponse2.bottom-20
                        if pygame.mouse.get_pressed()[0]==1:
                            if liste_elements[niveau-1].getBonneReponse()==2 :
                                reponseJuste()
                            else :
                                etat=4
                    elif pos_reponse3.topleft[0]<=coordonnées_souris[0]<=pos_reponse3.bottomright[0] and pos_reponse3.topleft[1]<=coordonnées_souris[1]<=pos_reponse3.bottomright[1] and 3 in liste_reponses_dispo:
                        pos_points_questions.centerx=690
                        pos_points_questions.y=pos_reponse3.bottom-20
                        if pygame.mouse.get_pressed()[0]==1:
                            if liste_elements[niveau-1].getBonneReponse()==3 :
                                reponseJuste()
                            else :
                                etat=4
                    elif pos_reponse4.topleft[0]<=coordonnées_souris[0]<=pos_reponse4.bottomright[0] and pos_reponse4.topleft[1]<=coordonnées_souris[1]<=pos_reponse4.bottomright[1] and 4 in liste_reponses_dispo:
                        pos_points_questions.centerx=690
                        pos_points_questions.y=pos_reponse4.bottom-20
                        if pygame.mouse.get_pressed()[0]==1:
                            if liste_elements[niveau-1].getBonneReponse()==4 :
                                reponseJuste()
                            else :
                                etat=4
                    elif pos_perso1.topleft[0]<=coordonnées_souris[0]<=pos_perso1.bottomright[0] and pos_perso1.topleft[1]<=coordonnées_souris[1]<=pos_perso1.bottomright[1] and str_demandePerso1!='':
                        pos_points_questions.centerx=569
                        pos_points_questions.y=pos_perso1.bottom-20
                        if pygame.mouse.get_pressed()[0]==1:
                            print('5')
                    elif pos_perso2.topleft[0]<=coordonnées_souris[0]<=pos_perso2.bottomright[0] and pos_perso2.topleft[1]<=coordonnées_souris[1]<=pos_perso2.bottomright[1] and str_demandePerso2!='':
                        pos_points_questions.centerx=569
                        pos_points_questions.y=pos_perso2.bottom-20
                        if pygame.mouse.get_pressed()[0]==1:
                            print('6')
                    elif pos_perso3.topleft[0]<=coordonnées_souris[0]<=pos_perso3.bottomright[0] and pos_perso3.topleft[1]<=coordonnées_souris[1]<=pos_perso3.bottomright[1] and str_demandePerso3!='':
                        pos_points_questions.centerx=569
                        pos_points_questions.y=pos_perso3.bottom-20
                        if pygame.mouse.get_pressed()[0]==1:
                            print('7')
                    elif pos_perso4.topleft[0]<=coordonnées_souris[0]<=pos_perso4.bottomright[0] and pos_perso4.topleft[1]<=coordonnées_souris[1]<=pos_perso4.bottomright[1] and str_demandePerso4!='':
                        pos_points_questions.centerx=569
                        pos_points_questions.y=pos_perso4.bottom-20
                        if pygame.mouse.get_pressed()[0]==1:
                            print('8')
                    else :
                        pos_points_questions.y=2000

                if event.type == MOUSEBUTTONDOWN:
##                    print(event.pos[0],event.pos[1])
                    if etat==0 and 600<=event.pos[0]<=779 and 467<=event.pos[1]<=555:
                        pygame.mixer.music.fadeout(1000)
                        pygame.mixer.music.load("assets/Lilys Theme.mp3")
                        pygame.mixer.music.play(-1)
                        pos_titre = pos_titre.move(0,-220)
                        pos_jouer = pos_jouer.move(2000,2000)
                        pos_appel = pos_appel.move(20-2000,20-2000)
                        pos_public = pos_public.move(20-2000,120-2000)
                        pos_moitie = pos_moitie.move(1260-2000,20-2000)
                        pos_swipe = pos_swipe.move(1260-2000,120-2000)
                        pos_sortie = pos_sortie.move(20-2000,800-2000)
                        pos_carre.x=1380-349
                        pos_carre.y=920-345
                        pos_rond = pos_rond.move(-969,-1103)
                        print('jouer')
                        etat=1
                    elif 40<=event.pos[0]<=109 and 40<=event.pos[1]<=100 and valeur_appel==1 and etat==2:
                        utilisationAppel()
                    elif 39<=event.pos[0]<=126 and 139<=event.pos[1]<=189 and valeur_public==1 and etat==2:
                        utilisationPublic()
                    elif 1279<=event.pos[0]<=1341 and 40<=event.pos[1]<=121 and valeur_moitie==1 and etat==2:
                        utilisationMoitie()
                    elif 1278<=event.pos[0]<=1345 and 138<=event.pos[1]<=203 and valeur_swipe==1 and etat==2:
                        utilisationSwipe()
                    elif 37<=event.pos[0]<=101 and 820<=event.pos[1]<=882 and etat==2:
                        etat=6

                if etat==1:
                    poserQuestion()

                fenetre.blit(carre, pos_carre)
                fenetre.blit(Rond, pos_rond)
                fenetre.blit(titre, pos_titre)
                fenetre.blit(jouer, pos_jouer)
                fenetre.blit(appel, pos_appel)
                fenetre.blit(public, pos_public)
                fenetre.blit(moitie, pos_moitie)
                fenetre.blit(swipe, pos_swipe)
                fenetre.blit(sortie, pos_sortie)
                fenetre.blit(texteQuestion,pos_question)
                fenetre.blit(texteReponse1,pos_reponse1)
                fenetre.blit(texteReponse2,pos_reponse2)
                fenetre.blit(texteReponse3,pos_reponse3)
                fenetre.blit(texteReponse4,pos_reponse4)
                fenetre.blit(texteDemandeAppel,pos_demande_appel)
                fenetre.blit(textePerso1,pos_perso1)
                fenetre.blit(textePerso2,pos_perso2)
                fenetre.blit(textePerso3,pos_perso3)
                fenetre.blit(textePerso4,pos_perso4)
                fenetre.blit(PointsQuestions,pos_points_questions)
                fenetre.blit(RondRouge, pos_rondrouge)
                fenetre.blit(RondVert, pos_rondvert)

            if etat==4 : #Si perdu a afficher
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load("assets/Fin.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                pos_titre = pos_titre.move(0,220)
                etat=5
                textePerdu=PoliceQuestion.render('Vous repartez avec '+gain[1]+' Gallions',1,(249,235,223)) #On creer notre texte de defaite
                pos_perdu=textePerdu.get_rect()
                pos_perdu.centerx=690
                pos_perdu.y=500
            if etat==6 : #Si sortie avec gain a afficher
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load("assets/Fin.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                pos_titre = pos_titre.move(0,220)
                etat=5
                textePerdu=PoliceQuestion.render('Vous repartez avec '+gain[0]+' Gallions',1,(249,235,223)) #On creer notre texte de defaite
                pos_perdu=textePerdu.get_rect()
                pos_perdu.centerx=690
                pos_perdu.y=500
            if etat==5:
                fenetre.blit(fond, (0,0))
                fenetre.blit(titre, pos_titre)
                fenetre.blit(textePerdu,pos_perdu)

        #Rafraichissement
        pygame.display.flip()


pygame.quit() #on ferme la fenetre
