import pygame
from constantes import *
from funciones import *

pygame.init()

fondo_dificultad = pygame.transform.scale(pygame.image.load("texturas/fondo.jpg"), PANTALLA)

lista_botones_dificultad = crear_lista_botones("texturas/textura_respuesta.jpg", 150, 125, 3)
lista_texto_dificultad = ["FACIL", "NORMAL", "DIFICIL"]
ESPACIADO_VERTICAL = 15  


altura_total_botones = (len(lista_botones_dificultad) * lista_botones_dificultad[0]["rectangulo"].height + (len(lista_botones_dificultad) - 1) * ESPACIADO_VERTICAL)

y_inicio = (ALTO - altura_total_botones) // 2


for i in range(len(lista_botones_dificultad)):
    boton_rect = lista_botones_dificultad[i]["rectangulo"]
    boton_rect.centerx = ANCHO // 2
    boton_rect.y = y_inicio + i * (boton_rect.height + ESPACIADO_VERTICAL)


def mostrar_dificultad(pantalla: pygame.Surface, cola_eventos) -> str:
    ventana = "dificultad"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(lista_botones_dificultad)):
                if lista_botones_dificultad[i]["rectangulo"].collidepoint(evento.pos):
                    SONIDO_CLICK.play()
                    return lista_texto_dificultad[i].lower()
    
    pantalla.blit(fondo_dificultad, (0, 0))
    
    for i in range(len(lista_botones_dificultad)):
        mostrar_texto(
            lista_botones_dificultad[i]["superficie"],
            lista_texto_dificultad[i],
            (90, 10),
            FUENTE_ARIAL_30_NEGRITA,
            COLOR_BLANCO
        )
        pantalla.blit(lista_botones_dificultad[i]["superficie"], lista_botones_dificultad[i]["rectangulo"])
    
    return ventana