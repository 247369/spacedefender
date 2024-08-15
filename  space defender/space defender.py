import pygame
import random

# Inicializar PyGame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))

# Título de la ventana
pygame.display.set_caption("Space Defender")

# Reloj para controlar la velocidad de refresco
reloj = pygame.time.Clock()

# Definir la clase de la nave


class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 40])
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.velocidad_x = 0

    def update(self):
        self.rect.x += self.velocidad_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

    def disparar(self):
        proyectil = Proyectil(self.rect.centerx, self.rect.top)
        todos_los_sprites.add(proyectil)
        proyectiles.add(proyectil)

# Definir la clase de los enemigos


class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 30])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidad_y = random.randint(1, 8)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO:
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.velocidad_y = random.randint(1, 8)

# Definir la clase de los proyectiles


class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 20])
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad_y = -10

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()

# Función principal para iniciar el juego


def iniciar_juego():
    global todos_los_sprites, enemigos, proyectiles

    # Crear grupos de sprites
    todos_los_sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    proyectiles = pygame.sprite.Group()

    # Crear la nave
    nave = Nave()
    todos_los_sprites.add(nave)

    # Crear enemigos
    for _ in range(10):
        enemigo = Enemigo()
        todos_los_sprites.add(enemigo)
        enemigos.add(enemigo)

    # Puntuación
    puntuacion = 0

    # Vidas del jugador
    vidas = 3

    # Bucle principal del juego
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    nave.velocidad_x = -5
                elif evento.key == pygame.K_RIGHT:
                    nave.velocidad_x = 5
                elif evento.key == pygame.K_SPACE:
                    nave.disparar()
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    nave.velocidad_x = 0

        # Actualizar los sprites
        todos_los_sprites.update()

        # Comprobar colisiones entre proyectiles y enemigos
        colisiones = pygame.sprite.groupcollide(
            proyectiles, enemigos, True, True)
        for colision in colisiones:
            puntuacion += 1
            enemigo = Enemigo()
            todos_los_sprites.add(enemigo)
            enemigos.add(enemigo)

        # Comprobar colisiones entre enemigos y la nave
        colisiones = pygame.sprite.spritecollide(nave, enemigos, False)
        if colisiones:
            vidas -= 1
            if vidas <= 0:
                corriendo = False

        # Dibujar la pantalla
        pantalla.fill(NEGRO)
        todos_los_sprites.draw(pantalla)

        # Dibujar la puntuación y las vidas
        mostrar_texto(f"Puntuación: {puntuacion}", 22, ANCHO // 2, 10)
        mostrar_texto(f"Vidas: {vidas}", 22, ANCHO // 2, 40)

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad del juego
        reloj.tick(60)

    # Mostrar pantalla de Game Over
    mostrar_game_over(puntuacion)

# Función para mostrar texto en la pantalla


def mostrar_texto(texto, tamaño, x, y):
    fuente = pygame.font.Font(None, tamaño)
    superficie_texto = fuente.render(texto, True, BLANCO)
    rect_texto = superficie_texto.get_rect()
    rect_texto.midtop = (x, y)
    pantalla.blit(superficie_texto, rect_texto)

# Función para mostrar la pantalla de Game Over


def mostrar_game_over(puntuacion):
    pantalla.fill(NEGRO)
    mostrar_texto("GAME OVER", 64, ANCHO // 2, ALTO // 4)
    mostrar_texto(f"Puntuación Final: {puntuacion}", 22, ANCHO // 2, ALTO // 2)
    mostrar_texto("Presiona una tecla para continuar",
                  18, ANCHO // 2, ALTO * 3 // 4)
    pygame.display.flip()
    esperar_tecla()

# Función para esperar una tecla


def esperar_tecla():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYUP:
                esperando = False

# Función para mostrar el menú principal


def mostrar_menu():
    pantalla.fill(NEGRO)
    mostrar_texto("SPACE DEFENDER", 64, ANCHO // 2, ALTO // 4)
    mostrar_texto("Presiona una tecla para comenzar",
                  18, ANCHO // 2, ALTO * 3 // 4)
    pygame.display.flip()
    esperar_tecla()


# Iniciar el juego desde el menú
mostrar_menu()
iniciar_juego()

# Finalizar PyGame
pygame.quit()
