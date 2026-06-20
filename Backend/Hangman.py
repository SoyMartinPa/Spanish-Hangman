import pygame, random, subprocess, os, json, time
#Constantes--------------------------------------------------
os.chdir(os.path.dirname(__file__))



def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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
╚══════════════════════════════════════════════════════════╝"""
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
#Constantes--------------------------------------------------


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
        if cn in usadas: 
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
#Pygame funciones ------------------------------------------- START
def cargar_assets():
    def escalar(path):
        return pygame.transform.scale(pygame.image.load(path), (250, 250))
    return {
        "cuadrado":   pygame.image.load('graficos/cuadrado.png'),
        "titulo":     pygame.image.load('graficos/logoB.png'),
        "fondo":      pygame.image.load('graficos/FONDO.png'),
        "teclado_1":  pygame.image.load('graficos/newFIRST.png'),
        "teclado_2":  pygame.image.load('graficos/newSECOND.png'),
        "teclado_3":  pygame.image.load('graficos/newTHIRD.png'),
        "unodos":     escalar('graficos/newunodos.png'),
        "trescuatro": escalar('graficos/newtrescuatro.png'),
        "cincoseis":  escalar('graficos/newcincoseis.png'),
        "sieteocho":  escalar('graficos/newsieteocho.png'),
        "nuevediez":  escalar('graficos/newnuevediez.png'),
        "once":       escalar('graficos/newonce.png'),
    }

def cargar_rects():
    fila1  = "qwertyuiop"
    fila2  = "asdfghjklñ"
    fila3  = "zxcvbnm"
    ancho1 = 55.4
    ancho3 = 386 / 7
    rects  = {}
    for i, l in enumerate(fila1): rects[l] = pygame.Rect(ancho1*i, 0, ancho1, 50).move(330, 130)
    for i, l in enumerate(fila2): rects[l] = pygame.Rect(ancho1*i, 0, ancho1, 50).move(330, 200)
    for i, l in enumerate(fila3): rects[l] = pygame.Rect(ancho3*i, 0, ancho3, 50).move(415, 270)
    return rects

def imagen_etapa(assets, errores):
    if errores <= 2:   return assets["unodos"]
    elif errores <= 4: return assets["trescuatro"]
    elif errores <= 6: return assets["cincoseis"]
    elif errores <= 8: return assets["sieteocho"]
    elif errores <= 9: return assets["nuevediez"]
    else:              return assets["once"]

def hangman_pygame(flag_set, palabras_agregadas):

    pygame.init()
    screen = pygame.display.set_mode((1000, 450))
    pygame.display.set_caption("Hangman")
    clock = pygame.time.Clock()
    activo = True


    data,etapas = archivos()

    assets = cargar_assets()
    rects = cargar_rects()

    real, palabra_norm = palabra_azar(data, flag_set , palabras_agregadas)
    tabla = ['_'] * len(real)
    usadas = set()
    font = pygame.font.Font(None, 40)
    texto = ""
    errores = 0

    while True:
        screen.fill('white')
        screen.blit(assets["fondo"], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and activo:
                for letra, rect in rects.items():
                    if rect.collidepoint(event.pos) and letra not in usadas:
                        usadas.add(letra)

                        if letra in palabra_norm:
                            for i, x in enumerate(real):
                                if normalizar(x) == letra:
                                    tabla[i] = x
                            if '_' not in tabla:
                                texto   = "¡Has ganado!!"
                                activo = False
                        else:
                            errores += 1
                            if errores >= MAX_ERRORES:
                                texto   = f"Palabra: {real.capitalize()}"
                                activo = False
                            else:
                                texto = f"Intentos: {MAX_ERRORES - errores}"
                        break

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


        screen.blit(font.render(texto, True, 'black'), (63, 303)) #Esto la sombra del texto
        screen.blit(font.render(texto, True, 'white'), (60, 300)) #Esto es el texto
        screen.blit(assets["titulo"],    (380, 0))
        screen.blit(assets["teclado_1"], (330, 130))
        screen.blit(assets["teclado_2"], (330, 200))
        screen.blit(assets["teclado_3"], (415, 270))
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
                elif flag == 2: print("La palabra debe estar entre 3 a 12 caracteres\n\n")
                elif flag == 0: print("Palabra agregada con exito!\n\n") 
                else: print()


                nueva = input("Ingrese la nueva palabra: ").strip()
                if not all(c.lower() in LETRAS_VALIDAS for c in nueva): flag = 1
                elif not (3<=len(nueva)<=12): flag = 2
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
