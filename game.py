#Importar ilbrerias
import pygame
import random
import math
import sys
import os

#Inicializar pygame
pygame.init()

#Tamaño de ventana
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))

#Función para obtener la ruta de los recursos
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

#Cargar fondo
asset_background = resource_path('assets/images/background.png')
background = pygame.image.load(asset_background)

#Cargar icono
asset_icon = resource_path('assets/images/ufo.png')
icon = pygame.image.load(asset_icon)

#Cargar sonido fondo
asset_sound = resource_path('assets/audios/background_music.mp3')
background_sound = pygame.mixer.music.load(asset_sound)

#Cargar player
asset_playerimg = resource_path('assets/images/space-invaders.png')
playerimg = pygame.image.load(asset_playerimg)

#Cargar bullet
asset_bulletimg = resource_path('assets/images/bullet.png')
bulletimg = pygame.image.load(asset_bulletimg)

#Cargar Fuente game over
asset_over_font= resource_path('assets/fonts/RAVIE.TTF')
over_font = pygame.font.Font(asset_over_font, 60)

#Cargar Fuente score
asset_font= resource_path('assets/fonts/comicbd.TTF')
font = pygame.font.Font(asset_font, 32)

# TITULO DE VENTANA
pygame.display.set_caption("SPACE FIGHTER")

# Icono de la ventana
pygame.display.set_icon(icon)

# Reproducir sonido fondo
pygame.mixer.music.play(-1)

# Crear reloj que controla la velocidad del juego
clock = pygame.time.Clock()

#Posición inicial del jugador
playerX = 370
playerY = 470
playerX_change = 0
playerY_change = 0

# Lista para almacenar posiciones enemigas
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

#se inicializan las variables para guardar posiciones enemigas
for i in range(no_of_enemies):
    #Cargar la imagen del enemigo 1
    enemy1 = resource_path('assets/images/enemy1.png')
    enemyimg.append(pygame.image.load(enemy1))

    #Cargar la imagen del enemigo 2
    enemy2 = resource_path('assets/images/enemy2.png')
    enemyimg.append(pygame.image.load(enemy2))

    #Se asigna una posición aleatoria al anemigo
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,150))

    #Se establece la velocidad del movimiento del enemigo
    enemyX_change.append(5)
    enemyY_change.append(20)

    #se inicialiar las variables para guardar la posicion de la bala
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    #se inicializa la puntuación (SCORE)
    score = 0

    #función para mostrar la puntuación (SCORE) en la pantalla
    def show_score():
        score_value = font.render("SCORE" + str(score), True, (255,255,255))
        screen.blit(score_value,(10,10))

    #función para mostrar al jugador en la pantalla
    def player(x, y):
        screen.blit(playerimg, (x,y))

    #función para dibujar al enemigo en la pantalla
    def enemy(x,y,i):
        screen.blit(enemyimg[i], (x,y))
    
    #función para disparar la bala (BULLET)
    def fire_bullet(x, y):
        global bullet_state

        bullet_state = "fire"
        screen.blit(bulletimg,(x+16,y+10))
    
    #defición para comprobar colisión (bala y enemigo)
    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance =math.sqrt((math.pow(enemyX-bulletX,2)) +
                            (math.pow(enemyY-bulletY,2)))
        if distance < 27:
            return True
        else:
            return False
        
    #Función para mostrar el texto de "GAME OVER"
    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255,255,255))
        text_rect = over_text.get_rect(
            center=(int(screen_width/2), int(screen_height/2)))
        screen.blit(over_text, text_rect)

    
    #Funcion principal del juego
    def gameloop():

        #Declaración de variables globales
        global score
        global playerX
        global playerY
        global playerX_change
        global playerY_change
        global bulletX
        global bulletY
        global Collision
        global bullet_state

        in_game = True
        while in_game:
            #Maneja eventos, actualiza y renderiza el juego
            #Limpia la pantalla
            screen.fill((0, 0, 0))
            screen.blit(background, (0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_game = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    #Movimientos del jugador y disparo
                    if event.key == pygame.K_LEFT:
                        playerX_change = -5

                    if event.key == pygame.K_RIGHT:
                        playerX_change = 5

                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            bulletX = playerX
                            bulletY = playerY
                            fire_bullet(bulletX, bulletY)
                    
                    if event.key == pygame.K_UP:
                        playerY_change = -5
                    
                    if event.key == pygame.K_DOWN:
                        playerY_change = 5

                    

                if event.type == pygame.KEYUP:
                    
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        playerX_change = 0 #resetea el cambio horizontal al soltar la tecla
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        playerY_change = 0  #resetea el cambio vertical al soltar la tecla

            #Actualiza la posición del jugador
            playerX += playerX_change
            playerY += playerY_change
            
            # Limitar la posición superior e inferior del jugador
            if playerY <= 0:  # Limitar la posición superior
                playerY = 0
            elif playerY >= 536:  # Limitar la posición inferior
                playerY = 536

            if playerX <= 0:
                playerX = 0
            elif playerX >=736:
                playerX = 736

            #Bucle que se ejecuta para cada enemigo
            game_over = False # inicializar la variable game over
            for i in range(no_of_enemies):
                if enemyY[i] > 440:
                    for j in range(no_of_enemies):
                        enemyY[j] = 2000

                    game_over = True
                    break


                enemyX[i] += enemyX_change [i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 5
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -5
                    enemyY[i] += enemyY_change[i]
                
                #Para comprobar si hay colisión

                collison = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collison:
                    bulletY = 454
                    bullet_state = "ready"
                    score += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(0, 150)
                enemy(enemyX[i], enemyY[i], i)

            if bulletY < 0:
                bulletY = 454
                bullet_state = "ready"

            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            player(playerX, playerY)
            show_score()

            if game_over:
                game_over_text() #muestra el texto de game over
                pygame.display.update()
                pygame.time.wait(2000)
                in_game = False # Salir del bucle del juego

            pygame.display.update()

            clock.tick(120)

gameloop()


