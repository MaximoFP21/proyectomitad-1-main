import pygame
from constantes import *
from funciones import *

pygame.init()

fondo_categoria = pygame.transform.scale(pygame.image.load("texturas/fondo.jpg"), PANTALLA)

# Crear lista de botones
lista_botones_categoria = crear_lista_botones("texturas/textura_respuesta.jpg", 150, 60, 6)

lista_texto_categoria = ["ENTRETENIMIENTO", "DEPORTE", "CIENCIA", "HISTORIA", "GEOGRAFIA", "ARTE"]

# CENTRAR LOS BOTONES EN LA VENTANA
ESPACIADO_VERTICAL = 15  # Espacio entre botones

# Calcular la altura total de todos los botones
altura_total_botones = (len(lista_botones_categoria) * lista_botones_categoria[0]["rectangulo"].height + 
                        (len(lista_botones_categoria) - 1) * ESPACIADO_VERTICAL)

# Calcular posición inicial Y para centrar verticalmente
y_inicio = (ALTO - altura_total_botones) // 2

# Posicionar cada botón
for i in range(len(lista_botones_categoria)):
    boton_rect = lista_botones_categoria[i]["rectangulo"]
    # Centrar horizontalmente
    boton_rect.centerx = ANCHO // 2
    # Posicionar verticalmente con espaciado
    boton_rect.y = y_inicio + i * (boton_rect.height + ESPACIADO_VERTICAL)


def mostrar_categoria(pantalla: pygame.Surface, cola_eventos) -> str:
    ventana = "categoria"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(lista_botones_categoria)):
                if lista_botones_categoria[i]["rectangulo"].collidepoint(evento.pos):
                    SONIDO_CLICK.play()
                    return lista_texto_categoria[i].lower()
    
    pantalla.blit(fondo_categoria, (0, 0))
    
    for i in range(len(lista_botones_categoria)):
        mostrar_texto(lista_botones_categoria[i]["superficie"], lista_texto_categoria[i], 
                      (90, 10), FUENTE_ARIAL_30_NEGRITA, COLOR_BLANCO)
        pantalla.blit(lista_botones_categoria[i]["superficie"], lista_botones_categoria[i]["rectangulo"])
    
    return ventana