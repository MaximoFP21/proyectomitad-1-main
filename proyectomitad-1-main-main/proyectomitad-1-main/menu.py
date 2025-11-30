import pygame
from constantes import *
from funciones import *

pygame.init()

fondo_menu = pygame.transform.scale(pygame.image.load("texturas/fondo.jpg"), PANTALLA)

# Crear lista de botones
lista_botones = crear_lista_botones("texturas/textura_respuesta.jpg", 150, 125, 6)

lista_texto_botones = ["JUGAR", "DIFICULTAD", "RANKINGS", "ESTADISTICAS", "AJUSTES", "SALIR"]

ESPACIADO_VERTICAL = 15  

altura_total_botones = (len(lista_botones) * lista_botones[0]["rectangulo"].height + 
                        (len(lista_botones) - 1) * ESPACIADO_VERTICAL)

y_inicio = (ALTO - altura_total_botones) // 2

for i in range(len(lista_botones)):
    boton_rect = lista_botones[i]["rectangulo"]
    boton_rect.centerx = ANCHO // 2
    boton_rect.y = y_inicio + i * (boton_rect.height + ESPACIADO_VERTICAL)

def mostrar_menu(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event]) -> str:
    ventana = "menu"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(lista_botones)):
                if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                    SONIDO_CLICK.play()
                    return lista_texto_botones[i].lower()
    
    pantalla.blit(fondo_menu, (0, 0))
    
    for i in range(len(lista_botones)):
        mostrar_texto(lista_botones[i]["superficie"], lista_texto_botones[i],
                      (90, 10), FUENTE_ARIAL_30_NEGRITA, COLOR_BLANCO)
        pantalla.blit(lista_botones[i]["superficie"], lista_botones[i]["rectangulo"])
    
    return ventana