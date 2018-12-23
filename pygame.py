import pygame
import time
import random

#A játék Sentdex videósorozata segítségével készült

pygame.init()

#Színek
fekete = (0,0,0)
feher = (255,255,255)
kek = (0,0,255)
zold = (0,255,0)
piros = (255,0,0)

display_szelesseg = 840
display_magassag = 650

korlat1 = 136 #Az autópálya bal korlátja
korlat2 = 705 #Az autópálya jobb korlátja

kocsiSzelesseg = 54 #A kocsi szélessége, az ütközésnél fog kelleni

display = pygame.display.set_mode((display_szelesseg,display_magassag))
pygame.display.set_caption('hdani1337-PyGame')
fps = pygame.time.Clock()

kocsiKep = pygame.image.load('img/car.png') #Az autó, amivel vagyunk
kocsiKepUtk = pygame.image.load('img/carCrash.png') #Az autónk, ha ütköztünk
hatterKep = pygame.image.load('img/bg.png') #A háttérkép
masikKocsi = pygame.image.load('img/enemyCar.png') #A szembe jövő autó

def szoveg_obj(szoveg,betu):
    szovegSurface = betu.render(szoveg, True, feher)
    return szovegSurface, szovegSurface.get_rect()


def kiir(szoveg):
    nagySzoveg = pygame.font.Font('pygame/freesansbold.ttf',45)
    SzovegSurf, SzovegDoboz = szoveg_obj(szoveg, nagySzoveg)
    SzovegDoboz.center = ((display_szelesseg/2),(display_magassag*0.2))
    display.blit(SzovegSurf, SzovegDoboz)

    pygame.display.update()

    time.sleep(3)

    game()


def kocsi(x,y):
    display.blit(kocsiKep,(x,y)) #Az ablakunkra (display) ,,rányomjuk" (blit) a kocsit (kocsiKep) arra a pozícióra (x,y), amit majd megadunk

def kocsiUtk(x,y):
    display.blit(kocsiKepUtk,(x,y))
    pygame.display.update()

def utkozesKorlat(x,y):
    kocsiUtk(x,y)
    kiir('Nekimentél a korlátnak')

def hatter():
    display.blit(hatterKep,(0,0)) #Ugyanezt tesszük a háttérképünkkel is

def game():
    kilepve = False

    kx = (display_szelesseg * 0.45)#Kocsi x koordinátája
    ky = (display_magassag * 0.8)#Kocsi y koordinátája
    kx_valt = 0 #A kocsi balra-jobbra mozgatásához fog kelleni

    while not kilepve:
        hatter()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() #Ha a piros X-et megnyomják (bezárják az ablakot), akkor álljon le
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a: #Ha balra nyilat vagy A-t nyom a játékos, akkor menjen balra az autó
                    kx_valt = -7 
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d: #Ha pedig jobbra nyilat vagy D-t nyom, akkor pedig jobbra menjen
                    kx_valt = 7

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    kx_valt = 0 #Ha nem nyomjuk az irányító gombokat, akkor nullázódjon le a mozgatás

        kx += kx_valt #Amennyit mozgott az autó, adja hozzá a pozícióhoz

        kocsi(kx,ky) #Meghívjuk a kocsi metódusunkat

        #Ütközés
        if kx < korlat1 or kx > (korlat2 - kocsiSzelesseg): #Ha nekimegy az autó valamelyik korlátnak
            utkozesKorlat(kx,ky) #Írjuk ki, hogy nekimentél a korlátnak

        pygame.display.update() #Frissítjuk a képet
        fps.tick(60) #Másodpercenkénti képfrissítés száma

game()
pygame.quit()
quit()