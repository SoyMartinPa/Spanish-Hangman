import pygame, random, subprocess, os, json, time
os.chdir(os.path.dirname(__file__))
#Constantes-------------------------------------------------- START

LETRAS_VALIDAS = "qwertyuiopasdfghjklñzxcvbnmáéíóú"
MAX_ERRORES = 10
INSTRUCCIONES = """
╔══════════════════════════════════════════════════════════╗
║                     CÓMO JUGAR                           ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  1. SET DE PALABRAS                                      ║
║     • Integrado   → palabras incluidas por defecto       ║
║     • Agregadas   → solo las palabras que tú agregaste   ║
║     • Ambos       → combinación de las dos anteriores    ║
║                                                          ║
║  2. MODO DE JUEGO                                        ║
║     • Terminal    → juega directamente en la consola     ║
║     • Gráfico     → abre una ventana visual del juego    ║
║                                                          ║
║  3. EN EL JUEGO                                          ║
║     • Adivina la palabra oculta letra por letra          ║
║     • Tienes un máximo de 10 errores antes de perder     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
AGREGAR_PALABRAS = """
╔══════════════════════════════════════════════════════════╗
║                   AGREGAR PALABRAS                       ║
╠══════════════════════════════════════════════════════════╣
║  • Solo letras del alfabeto (sin números ni símbolos)    ║
║  • Entre 3 y 12 caracteres                               ║
║  • Deja en blanco y presiona Enter para terminar         ║
╚══════════════════════════════════════════════════════════╝
"""
TITULO = r"""
 ██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
 ██║  ██║██╔══██╗████╗  ██║██╔════╝ ████╗ ████║██╔══██╗████╗  ██║
 ███████║███████║██╔██╗ ██║██║  ███╗██╔████╔██║███████║██╔██╗ ██║
 ██╔══██║██╔══██║██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║
 ██║  ██║██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║
 ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
"""
SET = r"""
 ███████╗███████╗████████╗    ██████╗ ███████╗
 ██╔════╝██╔════╝╚══██╔══╝    ██╔══██╗██╔════╝
 ███████╗█████╗     ██║       ██║  ██║█████╗  
 ╚════██║██╔══╝     ██║       ██║  ██║██╔══╝  
 ███████║███████╗   ██║       ██████╔╝███████╗
 ╚══════╝╚══════╝   ╚═╝       ╚═════╝ ╚══════╝

 ██████╗  █████╗ ██╗      █████╗ ██████╗ ██████╗  █████╗ ███████╗
 ██╔══██╗██╔══██╗██║     ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝
 ██████╔╝███████║██║     ███████║██████╔╝██████╔╝███████║███████╗
 ██╔═══╝ ██╔══██║██║     ██╔══██║██╔══██╗██╔══██╗██╔══██║╚════██║
 ██║     ██║  ██║███████╗██║  ██║██████╔╝██║  ██║██║  ██║███████║
 ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
"""
MODO_DE_JUEGO = r"""
 ███╗   ███╗ ██████╗ ██████╗  ██████╗     ██████╗ ███████╗
 ████╗ ████║██╔═══██╗██╔══██╗██╔═══██╗    ██╔══██╗██╔════╝
 ██╔████╔██║██║   ██║██║  ██║██║   ██║    ██║  ██║█████╗  
 ██║╚██╔╝██║██║   ██║██║  ██║██║   ██║    ██║  ██║██╔══╝  
 ██║ ╚═╝ ██║╚██████╔╝██████╔╝╚██████╔╝    ██████╔╝███████╗
 ╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝     ╚═════╝ ╚══════╝

     ██╗██╗   ██╗███████╗ ██████╗  ██████╗ 
     ██║██║   ██║██╔════╝██╔════╝ ██╔═══██╗
     ██║██║   ██║█████╗  ██║  ███╗██║   ██║
██   ██║██║   ██║██╔══╝  ██║   ██║██║   ██║
╚█████╔╝╚██████╔╝███████╗╚██████╔╝╚██████╔╝
 ╚════╝  ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ 

"""
#Constantes-------------------------------------------------- END

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def archivos():
    with open("spanish.json", "r", encoding="utf-8") as f:  
        data = json.load(f) # Abre y carga los datos json (cierra el archivo automaticamente) 
    with open("hangman.json", "r", encoding="utf-8") as f:
        ascii_art = json.load(f) # Abre y carga los datos, pero el resultado queda en el diccionario. 


    # Verificación para que hangman.json tenga las suficientes etapas antes de empezar.
    etapas = ascii_art["Hangman"] # Atajo para no escribir ascii_art["Hangman"] cada vez.
    if len(etapas) < MAX_ERRORES + 1: # Verifica que la lista tenga 11 elementos. 
        raise ValueError( # Si esto se cumple mostrar error. 
            f"hangman.json tiene solo {len(etapas)} etapas en 'Hangman', "
            f"pero se necesitan {MAX_ERRORES + 1} (índices 0 a {MAX_ERRORES})."
        )
    
    return data, etapas

def imprimir(etapas, errores, tabla):
    clear() # Imprime el nuevo estado del juego y elimina el anterior, funciona como loop.
    time.sleep(0.05) #Descubrimos que a veces falla el clear_output si va seguido de un input, por tanto, le daremos un tiempo para evitar el problema
    print(etapas[errores])
    linea = ' '.join(tabla) # Une los elementos de la tabla con separación de un espacio 
    print(f"\n  {linea}\n") 
    print(f"  Intentos fallidos  : {errores}/{MAX_ERRORES}")
    print(f"  Intentos restantes : {MAX_ERRORES - errores}")

    return linea


def normalizar(c): 
    return 'a' if c=='á' else 'e' if c=='é' else 'i' if c=='í' else 'o' if c=='ó' else 'u' if c=='ú' else c # Valida letras normales y sus tildes.

def valida(usadas,etapas,errores,tabla): # Función que valida que la letra del jugador sea correcta antes de ser utilizada en el juego. 
    while True:
        c = input("Adivinanza: ").lower().strip() 

        if len(c) != 1: # ¿Qué ocurre si el jugador ingresó mas de un carácter? 
            imprimir(etapas,errores,tabla)
            print("Error: ingresa solo UNA letra a la vez.") # Mostrar error
            continue
        if c not in LETRAS_VALIDAS: # ¿Qué ocurre si la letra no está en el abecedario?
            imprimir(etapas,errores,tabla)
            print(f"Error: '{c}' no es una letra válida del abecedario.") # Imprimir error
            continue
        cn = normalizar(c) # Primero normaliza la letra (saca la tilde). 
        if cn in usadas: # ¿Qué ocurre si la letra ya fue ingresada anteriormente?
            imprimir(etapas,errores,tabla)
            print(f"Error: la letra '{c}' ya fue ingresada antes.") # luego revisa si fue usada antes, en caso de ser así muestra error.
            continue

        return cn

def palabra_azar(data, flag_set,palabras_agregadas):
    if flag_set == 1 : real = random.choice(data).lower()
    elif flag_set == 2: real = random.choice(list(palabras_agregadas)).lower()
    elif flag_set == 3: real = random.choice(list(data) + list(palabras_agregadas)).lower()
    else: raise SystemExit("Error inesperado.")

    palabra_norm = ''.join(normalizar(x) for x in real) # Lee las palabras sin tilde, las normaliza y las une en un string. 
    return real, palabra_norm


def terminal(flag_set,palabras_agregadas):
    data,etapas = archivos()
    real, palabra_norm = palabra_azar(data,flag_set,palabras_agregadas)
    tabla = ['_'] * len(real) # Se reemplaza el guión por la letra una vez que la letra esté correcta.
    usadas      = set() # En un conjunto vacío se guardan todas las letras ya ingresadas.
    incorrectas = [] # Guarda todos los errores.  
    errores     = 0 
    global running
    while True:
        linea = imprimir(etapas,errores,tabla)

        if '_' not in linea: # Si todas las lineas estan utilizadas por letras reales...
            while True:
                clear()
                time.sleep(0.05)
                print("\n  ¡Ganaste! ¡Adivinaste la palabra!\n")
                res = input(f"\n\n ¿Continuar? (S/N)")
                if res.lower() == 's': break
                elif res.lower() == 'n': running = False; break
            break
        if errores >= MAX_ERRORES: # LLegas a los 10 intentos fallidos.
            while True:
                clear()
                time.sleep(0.05)
                print(f"\n  ¡Perdiste! La palabra correcta era: {real.capitalize()}\n")
                res = input(f"\n\n ¿Continuar? (S/N)")
                if res.lower() == 's': break
                elif res.lower() == 'n': running = False; break
            break
        if incorrectas:
            print(f"  Letras incorrectas : {', '.join(incorrectas)}")

        print()
        caracter = valida(usadas,etapas,errores,tabla)
        usadas.add(caracter)

        if caracter in palabra_norm: # Revela la posicion y la letra a la vez. 
            for i, x in enumerate(real): 
                if caracter == normalizar(x):
                    tabla[i] = x
        else:
            errores += 1
            incorrectas.append(caracter)

# Pygame clases
class Button:
    def __init__(self, text, width, height, pos, elevation, letra, font):
        # core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]
        self.letra = letra

        # top rectangle
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = "#FFFFFF"

        # outline rectangle
        self.outline_top_rect_outer = pygame.Rect(pos,(width, height))
        self.outline_top_rect_inner = pygame.Rect(pos,(width-4, height-4))

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos,(width,elevation))
        self.bottom_color = "gray38"

        # text
        self.text_surf = font.render(text,True,'#000c54')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        
        # shadow text
        self.shadow_text_surf = font.render(text,True,'#7B7B7B')
        self.shadow_text_rect = self.shadow_text_surf.get_rect(center = self.top_rect.center)
        self.shadow_offset = 1

    def draw(self, screen, activo, usadas):
        # color when already used
        if self.letra in usadas:
            self.top_color = "#A8A8A8"
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        self.shadow_text_rect.center = self.top_rect.center
        self.outline_top_rect_inner.center = self.top_rect.center
        self.outline_top_rect_outer.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation


        self.bottom_surf = pygame.Surface(pygame.Rect(self.bottom_rect).size, pygame.SRCALPHA)
        pygame.draw.rect(self.bottom_surf, (0,0,0,140), self.bottom_surf.get_rect(), border_radius = 10)
        screen.blit(self.bottom_surf, self.bottom_rect)

        #pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen,self.top_color,self.top_rect,border_radius=12)
        pygame.draw.rect(screen, '#000c54', self.outline_top_rect_outer, width=1, border_radius=12)
        pygame.draw.rect(screen, '#000c54', self.outline_top_rect_inner, width=1, border_radius=10)
        screen.blit(self.shadow_text_surf,(self.shadow_text_rect.x+self.shadow_offset,self.shadow_text_rect.y+self.shadow_offset))
        screen.blit(self.text_surf,self.text_rect)
        if not activo:
            self.dynamic_elevation = self.elevation
            self.top_color = '#FFFFFF'
        else:
            self.check_click()

    def check_click(self):
        global letra_seleccionada
        mouse_pos = pygame.mouse.get_pos()
        # el mouse esta por encima del boton
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = "#4BA1D7"
            self.shadow_text_surf
            # el boton fue presionado, se esta esperando a que se suelte
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            # el boton no esta siendo presionado
            else:
                self.dynamic_elevation = self.elevation
                # el boton fue presionado, enviar señal 
                if self.pressed == True:
                    letra_seleccionada = self.letra
                    self.pressed = False
        # el mouse no esta por encima del boton
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = "#FFFFFF"

#Pygame funciones ------------------------------------------- START
def cargar_assets():
    def escalar(path):
        return pygame.transform.scale(pygame.image.load(path), (250, 250))
    def translucido(path):
        path.set_alpha(150)
        return path
    
    fondo_texto = pygame.Surface((155,40))
    fondo_texto.fill("black")


    # este es un diccionario
    return {
        "cuadrado":   pygame.image.load('graficos/cuadrado.png'),
        "titulo":     pygame.image.load('graficos/logoB.png'),
        "fondo":      pygame.image.load('graficos/FONDO.png'),
        "unodos":     escalar('graficos/newunodos.png'),
        "trescuatro": escalar('graficos/newtrescuatro.png'),
        "cincoseis":  escalar('graficos/newcincoseis.png'),
        "sieteocho":  escalar('graficos/newsieteocho.png'),
        "nuevediez":  escalar('graficos/newnuevediez.png'),
        "once":       escalar('graficos/newonce.png'),
        "happy":      escalar('graficos/happyhappy.png'),
        "texto":      translucido(fondo_texto)
    }

def cargar_rects(font_botones):
    fila1  = "qwertyuiop"
    fila2  = "asdfghjklñ"
    fila3  = "zxcvbnm"

    rects  = {}
    for i, l in enumerate(fila1): rects[l] = Button(l, 50, 50, (330 + 56*i, 130), 6, l, font_botones)
    for i, l in enumerate(fila2): rects[l] = Button(l, 50, 50, (330 + 56*i, 200), 6, l, font_botones)
    for i, l in enumerate(fila3): rects[l] = Button(l, 50, 50, (415 + 56*i, 270), 6, l, font_botones)
    return rects

def imagen_etapa(assets, errores):
    if   errores < 0:  return assets["happy"]
    elif errores <= 2: return assets["unodos"]
    elif errores <= 4: return assets["trescuatro"]
    elif errores <= 6: return assets["cincoseis"]
    elif errores <= 8: return assets["sieteocho"]
    elif errores <= 9: return assets["nuevediez"]
    else:              return assets["once"]

def hangman_pygame(flag_set, palabras_agregadas):
    global letra_seleccionada
    pygame.init()
    screen = pygame.display.set_mode((1000, 450))
    pygame.display.set_caption("Hangman")
    clock = pygame.time.Clock()
    activo = True


    data,etapas = archivos()

    assets = cargar_assets()

    real, palabra_norm = palabra_azar(data, flag_set , palabras_agregadas)
    tabla = ['_'] * len(real)
    usadas = set()
    font = pygame.font.Font(None, 40)
    texto = "Intentos: 10"
    errores = 0
    rects = cargar_rects(font)
    letra_seleccionada = ""
    continuar = Button("Continuar",150,40,(100,350), 6, "continuar", font)
    salir = Button("Salir",150,40,(100,400), 6, "salir", font)

    # elemento para que el primer click del programa funcione correctamente
    window = pygame.Window.from_display_module()
    window.focus() 

    while True:
        screen.fill('white')
        screen.blit(assets["fondo"], (0, 0))

        if not activo:
            continuar.draw(screen,True,usadas)
            salir.draw(screen,True,usadas)
            if letra_seleccionada == "continuar":
                hangman_pygame(flag_set, palabras_agregadas)
            elif letra_seleccionada == "salir":
                pygame.quit()
                exit()

        for boton in rects.values():
            boton.draw(screen, activo, usadas)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if activo and letra_seleccionada != "":
            if letra_seleccionada not in usadas:
                usadas.add(letra_seleccionada)
                if letra_seleccionada in palabra_norm:
                    for i, x in enumerate(real):
                        if normalizar(x) == letra_seleccionada:
                            tabla[i] = x
                    if '_' not in tabla:
                        texto   = "¡Has ganado!"
                        errores = -1 # permite agregar al emoji feliz tras finalizar el juego con una victoria.
                        activo = False
                else:
                    errores += 1
                    if errores >= MAX_ERRORES:
                        texto   = f"Palabra: {real.capitalize()}"
                        activo = False
                    else:
                        texto = f"Intentos: {MAX_ERRORES - errores}"
            letra_seleccionada = ""

        n = len(palabra_norm)
        for i, c in enumerate(palabra_norm):

            if n % 2 == 0:
                x = 500 + 28 * (2*i - n + 1)
            else:
                x = 475 + 56 * (i - n // 2)
            posicion = (x, 350)


            descubierta = c in usadas
            color        = "#000C54"        if descubierta else "white"
            color_sombra = "cornflowerblue" if descubierta else "white"
            letra        = c.upper()

            screen.blit(assets["cuadrado"], posicion)
            screen.blit(font.render(letra, True, color_sombra), (posicion[0]+14, posicion[1]+14))
            screen.blit(font.render(letra, True, color),        (posicion[0]+16, posicion[1]+12))

        texto_surface = font.render(texto, True, 'black')

        
        texto_rect = texto_surface.get_rect(topleft=(60, 300))
        fondo_rect = texto_rect.inflate(15, 15)
        fondo_surf = pygame.Surface(pygame.Rect(fondo_rect).size, pygame.SRCALPHA)
        pygame.draw.rect(fondo_surf, (0,0,0,140), fondo_surf.get_rect(), border_radius = 10)
        screen.blit(fondo_surf, fondo_rect)


        screen.blit(font.render(texto, True, 'black'), (62,304)) #Esto es la sombra del texto.
        screen.blit(font.render(texto, True, 'white'), (60,302)) #Esto es el texto.
        
        screen.blit(assets["titulo"],    (380, 0))
        screen.blit(imagen_etapa(assets,errores),      (10,  40))

        pygame.display.update()
        clock.tick(60)


#Pygame funciones ------------------------------------------- END


def consola():    
    palabras_agregadas = set()
    pantalla = 0
    flag_set = 0
    while True:
        if pantalla == 0:
            clear()
            time.sleep(0.05)
            print(f"{TITULO}\n\n")
            print("1) Jugar")
            print("2) Agregar palabras")
            print("3) Intrucciones")
            print("4) Salir")
            while not (1<=pantalla<=4):
                pantalla = int(input("Opción: "))


        elif pantalla == 1:
            clear()
            time.sleep(0.05)
            print(SET)
            print("1) Integrado")
            print("2) Agregado") if palabras_agregadas else print("2) NO HAY PALABRAS AGREGADAS")
            print("3) Ambos")
            print("4) Atras")
            while not (10<=pantalla<=40):
                pantalla = (int(input("Opción: ")))*10

            if pantalla == 10: flag_set = 1
            elif pantalla == 20 and palabras_agregadas: flag_set = 2
            elif pantalla == 20 and not palabras_agregadas: pantalla = 0 
            elif pantalla == 30: flag_set = 3
            if pantalla == 40: pantalla = 0


        elif pantalla == 2:
            nueva = 1
            flag = -1
            while nueva:
                clear()
                time.sleep(0.05)
                print(AGREGAR_PALABRAS)
                if palabras_agregadas: print(f"\nSet actual: {palabras_agregadas}")
                if flag == 1: print("Palabra invalida\n\n")
                elif flag == 2: print("La palabra debe estar entre 3 a 14 caracteres\n\n")
                elif flag == 0: print("Palabra agregada con exito!\n\n") 
                else: print()


                nueva = input("Ingrese la nueva palabra: ").strip()
                if not all(c.lower() in LETRAS_VALIDAS for c in nueva): flag = 1
                elif not (3<=len(nueva)<=14): flag = 2
                else:
                    palabras_agregadas.add(nueva.capitalize())
                    flag = 0
            pantalla = 0
        elif pantalla == 3: 
            clear()
            time.sleep(0.05)
            print(INSTRUCCIONES)
            input("\n\nPresione cualquier tecla para salir")
            pantalla = 0
        elif pantalla == 4: return flag_set,palabras_agregadas,0

        elif 10<=pantalla<=30:
            clear()
            time.sleep(0.05)
            print(MODO_DE_JUEGO)
            print("1) Jugar en la terminal")
            print("2) Jugar con interfaz gráfica")
            print("3) Atras")
            while not (1<=pantalla<=3):
                pantalla = int(input("Opción: "))
            
            if pantalla == 1: return flag_set, palabras_agregadas, 1
            if pantalla == 2: return flag_set, palabras_agregadas, 2
            if pantalla == 3: pantalla = 1



flag_set,palabras_agregadas,num = consola()
running = True
if num == 1: 
    while running:
        terminal(flag_set,palabras_agregadas)
elif num == 2: 
    while running:
        hangman_pygame(flag_set,palabras_agregadas)
else: pass 
