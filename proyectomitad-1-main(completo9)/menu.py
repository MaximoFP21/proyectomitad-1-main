import pygame
from constantes import *
from funciones import *

pygame.init()

fondo_menu = pygame.transform.scale(pygame.image.load("texturas/fondo.jpg"), PANTALLA)

# Crear lista de botones - AHORA CON 7 BOTONES
lista_botones = crear_lista_botones("texturas/textura_respuesta.jpg", 150, 125, 7)

# AGREGAR "AGREGAR PREGUNTA" A LA LISTA
lista_texto_botones = ["JUGAR", "DIFICULTAD", "RANKINGS", "ESTADISTICAS", "AGREGAR PREGUNTA", "AJUSTES", "SALIR"]

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
                    # Convertir "AGREGAR PREGUNTA" a "agregar_pregunta"
                    texto_retorno = lista_texto_botones[i].lower().replace(" ", "_")
                    return texto_retorno
    
    pantalla.blit(fondo_menu, (0, 0))
    
    for i in range(len(lista_botones)):
        # Obtener el ancho del texto
        texto_surface = FUENTE_ARIAL_30_NEGRITA.render(lista_texto_botones[i], True, COLOR_BLANCO)
        texto_ancho = texto_surface.get_width()
        
        # Calcular posición X centrada
        boton_ancho = lista_botones[i]["rectangulo"].width
        pos_x_centrada = (boton_ancho - texto_ancho) // 2
        
        # Mostrar texto centrado
        mostrar_texto(lista_botones[i]["superficie"], lista_texto_botones[i],
                      (pos_x_centrada, 10), FUENTE_ARIAL_30_NEGRITA, COLOR_BLANCO)
        pantalla.blit(lista_botones[i]["superficie"], lista_botones[i]["rectangulo"])
    
    return ventana