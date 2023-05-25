import pygame
import random

# Dimensiones del mapa
ANCHO_MAPA = 800
ALTO_MAPA = 600
TAMANO_CELDA = 20

# Colores
COLOR_FONDO = (0, 0, 0)
COLOR_GUSANITO = (0, 255, 0)
COLOR_COMIDA = (255, 0, 0)

# Direcciones
ARRIBA = 0
ABAJO = 1
IZQUIERDA = 2
DERECHA = 3

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_MAPA, ALTO_MAPA))
    pygame.display.set_caption('Gusanito')

    reloj = pygame.time.Clock()

    gusanito = [(ANCHO_MAPA // 2, ALTO_MAPA // 2)]
    direccion = random.randint(0, 3)
    comida = generar_comida(gusanito)

    puntaje = 0

    pausado = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direccion != ABAJO:
                    direccion = ARRIBA
                elif event.key == pygame.K_DOWN and direccion != ARRIBA:
                    direccion = ABAJO
                elif event.key == pygame.K_LEFT and direccion != DERECHA:
                    direccion = IZQUIERDA
                elif event.key == pygame.K_RIGHT and direccion != IZQUIERDA:
                    direccion = DERECHA
                elif event.key == pygame.K_p:
                    pausado = not pausado

        if not pausado:
            gusanito = mover_gusanito(gusanito, direccion)
            if gusanito[0] == comida:
                gusanito.append((0, 0))
                comida = generar_comida(gusanito)
                puntaje += 1

            if verificar_colision(gusanito):
                pygame.quit()
                return

            pantalla.fill(COLOR_FONDO)
            dibujar_gusanito(pantalla, gusanito)
            dibujar_comida(pantalla, comida)
            mostrar_puntaje(pantalla, puntaje)
            pygame.display.flip()

        reloj.tick(10)

def generar_comida(gusanito):
    while True:
        x = random.randint(0, ANCHO_MAPA // TAMANO_CELDA - 1) * TAMANO_CELDA
        y = random.randint(0, ALTO_MAPA // TAMANO_CELDA - 1) * TAMANO_CELDA
        if (x, y) not in gusanito:
            return x, y

def mover_gusanito(gusanito, direccion):
    x, y = gusanito[0]
    if direccion == ARRIBA:
        y -= TAMANO_CELDA
    elif direccion == ABAJO:
        y += TAMANO_CELDA
    elif direccion == IZQUIERDA:
        x -= TAMANO_CELDA
    elif direccion == DERECHA:
        x += TAMANO_CELDA

    gusanito.insert(0, (x, y))
    gusanito.pop()

    return gusanito

def verificar_colision(gusanito):
    x, y = gusanito[0]
    if x < 0 or x >= ANCHO_MAPA or y < 0 or y >= ALTO_MAPA:
        return True

    if gusanito[0] in gusanito[1:]:
        return True

    return False

def dibujar_gusanito(pantalla, gusanito):
    for segmento in gusanito:
        pygame.draw.rect(pantalla, COLOR_GUSANITO, (segmento[0], segmento[1], TAMANO_CELDA, TAMANO_CELDA))

def dibujar_comida(pantalla, comida):
    pygame.draw.rect(pantalla, COLOR_COMIDA, (comida[0], comida[1], TAMANO_CELDA, TAMANO_CELDA))

def mostrar_puntaje(pantalla, puntaje):
    fuente = pygame.font.SysFont(None, 36)
    texto = fuente.render('Puntaje: {}'.format(puntaje), True, (255, 255, 255))
    pantalla.blit(texto, (10, 10))

if __name__ == '__main__':
    main()
