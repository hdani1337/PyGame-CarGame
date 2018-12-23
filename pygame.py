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

#Méretek
display_szelesseg = 840 #Azért így adjuk meg, mert később még hivatkozunk rá
display_magassag = 650 #Azért így adjuk meg, mert később még hivatkozunk rá

korlat1 = 136 #Az autópálya bal korlátja
korlat2 = 705 #Az autópálya jobb korlátja

kocsiSzelesseg = 54 #A kocsi szélessége, az ütközésnél fog kelleni
ellensegSzelesseg = 50 #A kocsi szélessége, az ütközésnél fog kelleni
ellensegMagassag = 94 #A kocsi magassága, az ütközésnél fog kelleni

#Ablak tulajdonságai
display = pygame.display.set_mode((display_szelesseg,display_magassag)) #Ablak mérete
pygame.display.set_caption('Ámokfutás v0.1') #Ablak címe
fps = pygame.time.Clock() #Ezt később hívjuk meg, itt adjuk meg a képkockák számát másodpercenként

#Képek
kocsiKep = pygame.image.load('img/car.png') #Az autó, amivel vagyunk
kocsiKepUtk = pygame.image.load('img/carCrash.png') #Az autónk, ha ütköztünk
hatterKep = pygame.image.load('img/bg.png') #A háttérkép
hatterKepLost = pygame.image.load('img/bg_lost.png') #Háttérkép, ha vesztettél
masikKocsi = pygame.image.load('img/enemyCar.png') #A szembe jövő autó
masikKocsiUtk = pygame.image.load('img/enemyCarCrash.png') #A szembe jövő autó, ha ütközik


#Metódusok

def enemy(x,y):
    global enemyX

    if x == 1:
        display.blit(masikKocsi,(195,y)) #Első sáv
        enemyX = 195
        return enemyX

    if x == 2:
        display.blit(masikKocsi,(320,y)) #Második sáv
        enemyX = 320
        return enemyX

    if x == 3:
        display.blit(masikKocsi,(450,y)) #Harmadik sáv
        enemyX = 450
        return enemyX

    if x == 4:
        display.blit(masikKocsi,(585,y)) #Negyedik sáv
        enemyX = 585
        return enemyX

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

def hatter():
    display.blit(hatterKep,(0,0)) #Ugyanezt tesszük a háttérképünkkel is

def hatterLost():
    display.blit(hatterKepLost,(0,0))

def kocsiUtk(x,y):
    display.blit(kocsiKepUtk,(x,y))
    pygame.display.update()

def enemyUtk(x,y):
    display.blit(masikKocsiUtk,(x,y))
    pygame.display.update()

def utkozesKorlat(x,y):
    hatterLost()
    kocsiUtk(x,y)
    time.sleep(3)
    game()

def utkozesKocsi(x,y,x_enemy,y_enemy):
    hatterLost()
    pygame.display.update()
    kocsiUtk(x,y)
    enemyUtk(x_enemy,y_enemy)
    time.sleep(3)
    game()

def game():
    kilepve = False

    kx = (display_szelesseg * 0.465)#Kocsi x koordinátája
    ky = (display_magassag * 0.79)#Kocsi y koordinátája
    kx_valt = 0 #A kocsi balra-jobbra mozgatásához fog kelleni

    enemy_kezdX = random.randrange(1,4) #Random sáv
    enemy_kezdY = -300 #300 pixellel a pálya fölött
    enemy_sebesseg = 5 #Kezdetben 300 pixel/másodperc sebesség (5*60)

    while not kilepve:
        hatter() #Háttér beállítása

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() #Ha a piros X-et megnyomják (bezárják az ablakot), akkor álljon le
                quit() #És záródjon be

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a: #Ha balra nyilat vagy A-t nyom a játékos, akkor menjen balra az autó
                    kx_valt = -9 #9 pixellel
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d: #Ha pedig jobbra nyilat vagy D-t nyom, akkor pedig jobbra menjen
                    kx_valt = 9 #9 pixellel

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    kx_valt = 0 #Ha nem nyomjuk az irányító gombokat, akkor nullázódjon le a mozgatás

        kx += kx_valt #Amennyit mozgott az autó, adja hozzá a pozícióhoz
       
        enemy(enemy_kezdX,enemy_kezdY) #Meghívjuk az ellenfelet
        enemy_kezdY += enemy_sebesseg #Menjen az ellenfél
        kocsi(kx,ky) #Meghívjuk a kocsinkat

        #Ütközés
        if kx < korlat1 or kx > korlat2 - kocsiSzelesseg: #Ha nekimegy az autó valamelyik korlátnak
            utkozesKorlat(kx,ky) #Írjuk ki, hogy nekimentél a korlátnak

        if enemy_kezdY > display_magassag: #Ha az ellenség kilép a képből, akkor
            enemy_kezdY = -100 #Menjen vissza a pálya tetejénél feljebb 100 pixellel, hogy ne egyből jöjjön az autó
            enemy_sebesseg += 0.5 #Növeljük a sebességet
            enemy_kezdX = random.randrange(1,4) #Váltsunk sávot


        if ky < enemy_kezdY + ellensegMagassag:
            if kx < enemyX and kx + kocsiSzelesseg > enemyX:
                utkozesKocsi(kx,ky,enemyX,enemy_kezdY)

            if enemyX + ellensegSzelesseg < kx + kocsiSzelesseg and enemyX + ellensegSzelesseg > kx:
                utkozesKocsi(kx,ky,enemyX,enemy_kezdY)
            
        
        pygame.display.update() #Frissítjuk a képet
        fps.tick(60) #Másodpercenkénti képfrissítés száma

game()
pygame.quit()
quit()
