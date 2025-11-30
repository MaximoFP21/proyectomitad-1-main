import pygame
from constantes import *
from funciones import *
from preguntas import top5_preguntas, top5_dificiles, lista_preguntas

pygame.init()

boton_volver = crear_elemento_juego("texturas/textura_respuesta.jpg", 100, 40, 10, 10)

def renderizar_texto_simple(superficie, texto, x, y, fuente, color):
    """Renderiza texto en una posición exacta sin ajuste automático"""
    texto_surface = fuente.render(texto, True, color)
    superficie.blit(texto_surface, (x, y))

def mostrar_estadisticas(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event]) -> str:
    """
    Muestra las estadísticas de las preguntas:
    - Top 5 preguntas más acertadas
    - Top 5 preguntas más difíciles
    """
    ventana = "estadisticas"
    
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_volver and boton_volver["rectangulo"].collidepoint(evento.pos):
                SONIDO_CLICK.play()
                return "menu"
    
    pantalla.fill(COLOR_BLANCO)
    
    
    if boton_volver:
        boton_volver["superficie"].fill(COLOR_NEGRO)
        texto_volver = FUENTE_ARIAL_20.render("VOLVER", True, COLOR_BLANCO)
        boton_volver["superficie"].blit(texto_volver, (5, 5))
        pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    
    
    titulo = FUENTE_ARIAL_30_NEGRITA.render("ESTADISTICAS DE PREGUNTAS", True, COLOR_NEGRO)
    pantalla.blit(titulo, (160, 60))
    
    
    titulo_faciles = FUENTE_ARIAL_25.render("TOP 5 MAS FACILES:", True, COLOR_VERDE)
    pantalla.blit(titulo_faciles, (30, 180))
    
    top_faciles = top5_preguntas(lista_preguntas)
    y = 220
    
    if len(top_faciles) == 0:
        texto_vacio = FUENTE_ARIAL_20.render("No hay datos aun", True, (100, 100, 100))
        pantalla.blit(texto_vacio, (30, y))
    else:
        for i in range(len(top_faciles)):
            pregunta = top_faciles[i]
            
            
            descripcion = pregunta['descripcion']
            if len(descripcion) > 32:
                descripcion = descripcion[:32] + "..."
            
            
            texto1 = f"{i+1}. {descripcion}"
            linea1 = FUENTE_ARIAL_20.render(texto1, True, COLOR_NEGRO)
            pantalla.blit(linea1, (30, y))
            
            
            stats = f"     {pregunta['porcentaje_aciertos']}% ({pregunta['aciertos']}/{pregunta['veces_preguntada']})"
            linea2 = FUENTE_ARIAL_20.render(stats, True, (0, 150, 0))
            pantalla.blit(linea2, (30, y + 25))
            
            y += 60
    
    
    titulo_dificiles = FUENTE_ARIAL_25.render("TOP 5 MAS DIFICILES:", True, COLOR_ROJO)
    pantalla.blit(titulo_dificiles, (420, 180))
    
    top_dif = top5_dificiles(lista_preguntas)
    y2 = 220
    
    if len(top_dif) == 0:
        texto_vacio2 = FUENTE_ARIAL_20.render("No hay datos aun", True, (100, 100, 100))
        pantalla.blit(texto_vacio2, (420, y2))
    else:
        for i in range(len(top_dif)):
            pregunta = top_dif[i]
            
            
            descripcion = pregunta['descripcion']
            if len(descripcion) > 32:
                descripcion = descripcion[:32] + "..."
            
            
            texto1 = f"{i+1}. {descripcion}"
            linea1 = FUENTE_ARIAL_20.render(texto1, True, COLOR_NEGRO)
            pantalla.blit(linea1, (420, y2))
            
            
            stats = f"     {pregunta['porcentaje_aciertos']}% ({pregunta['aciertos']}/{pregunta['veces_preguntada']})"
            linea2 = FUENTE_ARIAL_20.render(stats, True, (150, 0, 0))
            pantalla.blit(linea2, (420, y2 + 25))
            
            y2 += 60
    
    return ventana