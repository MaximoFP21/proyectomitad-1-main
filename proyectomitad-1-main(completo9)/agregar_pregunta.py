import pygame
from constantes import *
from funciones import *

pygame.init()

# Estado global para el flujo de agregar pregunta
estado_agregar = {
    "paso": "categoria",  # categoria, pregunta, resp1, resp2, resp3, resp4, correcta
    "pregunta": "",
    "respuesta_1": "",
    "respuesta_2": "",
    "respuesta_3": "",
    "respuesta_4": "",
    "respuesta_correcta": "",
    "categoria": ""
}

# Lista de categorías disponibles
CATEGORIAS = ["CIENCIA", "GEOGRAFIA", "HISTORIA", "ARTE", "DEPORTE", "ENTRETENIMIENTO"]

def resetear_estado():
    """Resetea el estado al inicial"""
    global estado_agregar
    estado_agregar = {
        "paso": "categoria",
        "pregunta": "",
        "respuesta_1": "",
        "respuesta_2": "",
        "respuesta_3": "",
        "respuesta_4": "",
        "respuesta_correcta": "",
        "categoria": ""
    }

def mostrar_pantalla_agregar_pregunta(pantalla: pygame.Surface, cola_eventos):
    global estado_agregar
    ventana = "agregar_pregunta"
    
    # Manejar eventos
    for evento in cola_eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                # Borrar último caracter según el paso actual
                if estado_agregar["paso"] == "pregunta":
                    estado_agregar["pregunta"] = estado_agregar["pregunta"][:-1]
                elif estado_agregar["paso"] == "resp1":
                    estado_agregar["respuesta_1"] = estado_agregar["respuesta_1"][:-1]
                elif estado_agregar["paso"] == "resp2":
                    estado_agregar["respuesta_2"] = estado_agregar["respuesta_2"][:-1]
                elif estado_agregar["paso"] == "resp3":
                    estado_agregar["respuesta_3"] = estado_agregar["respuesta_3"][:-1]
                elif estado_agregar["paso"] == "resp4":
                    estado_agregar["respuesta_4"] = estado_agregar["respuesta_4"][:-1]
                elif estado_agregar["paso"] == "correcta":
                    estado_agregar["respuesta_correcta"] = ""
            
            elif evento.key == pygame.K_RETURN:
                # Pasar al siguiente paso
                if estado_agregar["paso"] == "pregunta" and len(estado_agregar["pregunta"]) > 0:
                    estado_agregar["paso"] = "resp1"
                elif estado_agregar["paso"] == "resp1" and len(estado_agregar["respuesta_1"]) > 0:
                    estado_agregar["paso"] = "resp2"
                elif estado_agregar["paso"] == "resp2" and len(estado_agregar["respuesta_2"]) > 0:
                    estado_agregar["paso"] = "resp3"
                elif estado_agregar["paso"] == "resp3" and len(estado_agregar["respuesta_3"]) > 0:
                    estado_agregar["paso"] = "resp4"
                elif estado_agregar["paso"] == "resp4" and len(estado_agregar["respuesta_4"]) > 0:
                    estado_agregar["paso"] = "correcta"
                elif estado_agregar["paso"] == "correcta" and estado_agregar["respuesta_correcta"] in ["1", "2", "3", "4"]:
                    # Guardar pregunta
                    guardar_nueva_pregunta()
                    resetear_estado()
                    SONIDO_CLICK.play()
                    return "menu"
            
            else:
                # Agregar caracter según el paso actual
                char = evento.unicode
                if char.isprintable():
                    if estado_agregar["paso"] == "pregunta" and len(estado_agregar["pregunta"]) < 120:
                        estado_agregar["pregunta"] += char
                    elif estado_agregar["paso"] in ["resp1", "resp2", "resp3", "resp4"]:
                        campo = f"respuesta_{estado_agregar['paso'][-1]}"
                        if len(estado_agregar[campo]) < 50:
                            estado_agregar[campo] += char
                    elif estado_agregar["paso"] == "correcta" and char in ["1", "2", "3", "4"]:
                        estado_agregar["respuesta_correcta"] = char
        
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            # Verificar click en botón volver
            if 10 <= evento.pos[0] <= 110 and 10 <= evento.pos[1] <= 50:
                SONIDO_CLICK.play()
                resetear_estado()
                return "menu"
            
            # Si estamos en selección de categoría, verificar clicks en botones
            if estado_agregar["paso"] == "categoria":
                resultado = manejar_click_categoria(evento.pos)
                if resultado:
                    return resultado
            
            # Verificar click en botón siguiente/finalizar
            boton_x = (ANCHO - 300) // 2
            boton_y = 480
            if boton_x <= evento.pos[0] <= boton_x + 300 and boton_y <= evento.pos[1] <= boton_y + 60:
                SONIDO_CLICK.play()
                # Simular ENTER
                if estado_agregar["paso"] == "pregunta" and len(estado_agregar["pregunta"]) > 0:
                    estado_agregar["paso"] = "resp1"
                elif estado_agregar["paso"] == "resp1" and len(estado_agregar["respuesta_1"]) > 0:
                    estado_agregar["paso"] = "resp2"
                elif estado_agregar["paso"] == "resp2" and len(estado_agregar["respuesta_2"]) > 0:
                    estado_agregar["paso"] = "resp3"
                elif estado_agregar["paso"] == "resp3" and len(estado_agregar["respuesta_3"]) > 0:
                    estado_agregar["paso"] = "resp4"
                elif estado_agregar["paso"] == "resp4" and len(estado_agregar["respuesta_4"]) > 0:
                    estado_agregar["paso"] = "correcta"
                elif estado_agregar["paso"] == "correcta" and estado_agregar["respuesta_correcta"] in ["1", "2", "3", "4"]:
                    guardar_nueva_pregunta()
                    resetear_estado()
                    return "menu"
    
    # Dibujar pantalla según el paso actual
    pantalla.fill(COLOR_NEGRO)
    
    # Título
    mostrar_texto(pantalla, "Agregar Pregunta", (200, 50), FUENTE_ARIAL_50, COLOR_BLANCO)
    
    if estado_agregar["paso"] == "categoria":
        dibujar_seleccion_categoria(pantalla)
    elif estado_agregar["paso"] == "pregunta":
        dibujar_paso_pregunta(pantalla)
    elif estado_agregar["paso"] in ["resp1", "resp2", "resp3", "resp4"]:
        numero = estado_agregar["paso"][-1]
        dibujar_paso_respuesta(pantalla, int(numero))
    elif estado_agregar["paso"] == "correcta":
        dibujar_paso_correcta(pantalla)
    
    # Botón volver
    pygame.draw.rect(pantalla, COLOR_BLANCO, (10, 10, 100, 40), border_radius=5)
    mostrar_texto(pantalla, "VOLVER", (15, 15), FUENTE_ARIAL_25, COLOR_NEGRO)
    
    return ventana

def dibujar_seleccion_categoria(pantalla):
    """Dibuja la pantalla de selección de categoría"""
    mostrar_texto(pantalla, "Selecciona una categoria:", (180, 120), FUENTE_ARIAL_30, COLOR_BLANCO)
    
    # Crear botones de categorías
    y_inicio = 200
    espaciado = 15
    ancho_boton = 400
    alto_boton = 60
    
    for i, categoria in enumerate(CATEGORIAS):
        x = (ANCHO - ancho_boton) // 2
        y = y_inicio + i * (alto_boton + espaciado)
        
        # Dibujar botón
        pygame.draw.rect(pantalla, COLOR_BLANCO, (x, y, ancho_boton, alto_boton), border_radius=10)
        
        # Dibujar texto centrado
        texto_surface = FUENTE_ARIAL_25.render(categoria, True, COLOR_NEGRO)
        texto_rect = texto_surface.get_rect(center=(x + ancho_boton // 2, y + alto_boton // 2))
        pantalla.blit(texto_surface, texto_rect)

def manejar_click_categoria(pos):
    """Maneja el click en un botón de categoría"""
    y_inicio = 200
    espaciado = 15
    ancho_boton = 400
    alto_boton = 60
    x_boton = (ANCHO - ancho_boton) // 2
    
    for i, categoria in enumerate(CATEGORIAS):
        y = y_inicio + i * (alto_boton + espaciado)
        
        # Verificar si el click está dentro del botón
        if x_boton <= pos[0] <= x_boton + ancho_boton and y <= pos[1] <= y + alto_boton:
            SONIDO_CLICK.play()
            estado_agregar["categoria"] = categoria.lower()
            estado_agregar["paso"] = "pregunta"
            return None
    
    return None

def dibujar_paso_pregunta(pantalla):
    """Dibuja la pantalla para ingresar la pregunta"""
    # Mostrar categoría seleccionada
    mostrar_texto(pantalla, f"Categoria: {estado_agregar['categoria'].upper()}", (250, 100), FUENTE_ARIAL_25, COLOR_VERDE)
    
    mostrar_texto(pantalla, "Pregunta:", (250, 140), FUENTE_ARIAL_30, COLOR_BLANCO)
    
    # Cuadro para pregunta
    cuadro_x = 100
    cuadro_y = 200
    cuadro_ancho = 600
    cuadro_alto = 220
    
    pygame.draw.rect(pantalla, COLOR_BLANCO, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto), border_radius=15)
    
    # Mostrar texto con wrap
    lineas = wrap_text(estado_agregar["pregunta"], FUENTE_ARIAL_25, cuadro_ancho - 30)
    y_texto = cuadro_y + 15
    for linea in lineas:
        mostrar_texto(pantalla, linea, (cuadro_x + 15, y_texto), FUENTE_ARIAL_25, COLOR_NEGRO)
        y_texto += 35
    
    # Botón siguiente
    dibujar_boton_siguiente(pantalla)

def dibujar_paso_respuesta(pantalla, numero):
    """Dibuja la pantalla para ingresar una respuesta"""
    # Mostrar categoría seleccionada
    mostrar_texto(pantalla, f"Categoria: {estado_agregar['categoria'].upper()}", (250, 100), FUENTE_ARIAL_25, COLOR_VERDE)
    
    mostrar_texto(pantalla, f"Respuesta {numero}:", (230, 140), FUENTE_ARIAL_30, COLOR_BLANCO)
    
    # Cuadro para respuesta
    cuadro_x = 100
    cuadro_y = 200
    cuadro_ancho = 600
    cuadro_alto = 100
    
    pygame.draw.rect(pantalla, COLOR_BLANCO, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto), border_radius=15)
    
    # Obtener texto actual
    campo = f"respuesta_{numero}"
    texto = estado_agregar[campo]
    
    # Mostrar texto
    lineas = wrap_text(texto, FUENTE_ARIAL_25, cuadro_ancho - 30)
    y_texto = cuadro_y + 35
    for linea in lineas:
        mostrar_texto(pantalla, linea, (cuadro_x + 15, y_texto), FUENTE_ARIAL_25, COLOR_NEGRO)
        y_texto += 35
    
    # Botón siguiente
    dibujar_boton_siguiente(pantalla)

def dibujar_paso_correcta(pantalla):
    """Dibuja la pantalla para seleccionar la respuesta correcta"""
    # Mostrar categoría seleccionada
    mostrar_texto(pantalla, f"Categoria: {estado_agregar['categoria'].upper()}", (250, 100), FUENTE_ARIAL_25, COLOR_VERDE)
    
    mostrar_texto(pantalla, "Respuesta Correcta (1-4):", (180, 140), FUENTE_ARIAL_30, COLOR_BLANCO)
    
    # Cuadro para número
    cuadro_x = 300
    cuadro_y = 220
    cuadro_ancho = 200
    cuadro_alto = 80
    
    pygame.draw.rect(pantalla, COLOR_BLANCO, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto), border_radius=15)
    
    # Mostrar número
    mostrar_texto(pantalla, estado_agregar["respuesta_correcta"], (cuadro_x + 85, cuadro_y + 20), FUENTE_ARIAL_50, COLOR_NEGRO)
    
    # Botón finalizar
    boton_x = (ANCHO - 300) // 2
    boton_y = 480
    pygame.draw.rect(pantalla, COLOR_BLANCO, (boton_x, boton_y, 300, 60), border_radius=15)
    mostrar_texto(pantalla, "FINALIZAR", (boton_x + 70, boton_y + 15), FUENTE_ARIAL_30, COLOR_NEGRO)

def dibujar_boton_siguiente(pantalla):
    """Dibuja el botón siguiente"""
    boton_x = (ANCHO - 300) // 2
    boton_y = 480
    pygame.draw.rect(pantalla, COLOR_BLANCO, (boton_x, boton_y, 300, 60), border_radius=15)
    mostrar_texto(pantalla, "SIGUIENTE", (boton_x + 70, boton_y + 15), FUENTE_ARIAL_30, COLOR_NEGRO)

def guardar_nueva_pregunta():
    """Guarda la nueva pregunta en el archivo CSV"""
    from preguntas import lista_preguntas, guardar_preguntas
    
    nueva_pregunta = {
        "categoria": estado_agregar["categoria"],
        "descripcion": estado_agregar["pregunta"],
        "respuesta_1": estado_agregar["respuesta_1"],
        "respuesta_2": estado_agregar["respuesta_2"],
        "respuesta_3": estado_agregar["respuesta_3"],
        "respuesta_4": estado_agregar["respuesta_4"],
        "respuesta_correcta": int(estado_agregar["respuesta_correcta"]),
        "porcentaje_aciertos": 0,
        "fallos": 0,
        "aciertos": 0,
        "veces_preguntada": 0
    }
    
    lista_preguntas.append(nueva_pregunta)
    guardar_preguntas(lista_preguntas)
    print(f"✓ Pregunta agregada: {nueva_pregunta['descripcion']}")
    print(f"  Categoría: {nueva_pregunta['categoria']}")