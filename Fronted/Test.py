import pygame, random, subprocess, os, json
from sys import exit

os.chdir(os.path.dirname(__file__))
ABECEDARIO = "qwertyuiopasdfghjklñzxcvbnmáéíóú"
MAX_ERRORES = 10

pygame.init()
screen = pygame.display.set_mode((1000,450))
pygame.display.set_caption("Proyecto Programacion")
clock = pygame.time.Clock()

def cargar_assets():
    def escalar(path):
        return pygame.transform.scale(pygame.image.load(path), (250, 250))

    return {
        "cuadrado":   pygame.image.load('graficos/cuadrado.png'),
        "titulo":     pygame.image.load('graficos/TITLE.png'),
        "teclado_1":  pygame.image.load('graficos/FIRST.png'),
        "teclado_2":  pygame.image.load('graficos/SECOND.png'),
        "teclado_3":  pygame.image.load('graficos/THIRD.png'),
        "palo":       escalar('graficos/gallow.png'),
        "unodos":     escalar('graficos/unodos.png'),
        "trescuatro": escalar('graficos/trescuatro.png'),
        "cincoseis":  escalar('graficos/cincoseis.png'),
        "sieteocho":  escalar('graficos/sietocoho.png'),
        "nuevediez":  escalar('graficos/nuevedies.png'),
        "once":       escalar('graficos/once.png'),
    }

def crear_rects():
    fila1 = "qwertyuiop"
    fila2 = "asdfghjklñ"
    fila3 = "zxcvbnm"
    ancho = 55.4
    rects = {}
    for i, l in enumerate(fila1):
        rects[l] = pygame.Rect(ancho * i, 0, ancho, 50).move(330, 130)
    for i, l in enumerate(fila2):
        rects[l] = pygame.Rect(ancho * i, 0, ancho, 50).move(330, 200)
    for i, l in enumerate(fila3):
        rects[l] = pygame.Rect(ancho * i, 0, ancho, 50).move(415, 270)
    return rects

def clear():
    if os.name == 'nt': subprocess.run(['cmd','/c','cls'])
    else: subprocess.run(['clear'])
        
def normalizar(c):
    return 'a' if c == 'á' else 'e' if c == 'é' else 'i' if c == 'í' else 'o' if c == 'ó' else 'u' if c == 'ú' else c

# Este contador empieza en 10. Por cada intento fallido, ira bajando
# hasta llegar a 0, donde acabara el juego con un 'game over'.
contador = 10
# mientras sea verdadero, el teclado seguira respondiendo a los clicks
running = True

def game_over(random_letra):
    global running
    clear()
    print("GAME OVER!\n")
    print(f"La letra correcta era {random_letra}")
    print("el emoji murio, rip")
    running = False

def intento_correcto(letra):
    global contador
    global running
    contador = 11
    clear()
    print(f"{letra} es la letra correcta!")
    print("el emoji sobrevivio, yippiee")
    running = False

def intento_fallido(letra,random_letra):
    global contador
    clear()
    print("Adivina la letra!\n")
    print(f"{letra} es una letra equivocada")
    print(f"Intentos Restantes: {contador}")
    contador -= 1
    if contador == -1:
        game_over(random_letra)

with open("spanish.json", "r", encoding="utf-8") as diccionario:
    #with open("hangman.json", "r", encoding="utf-8") as hangman:
    data = json.load(diccionario)
        #ascii = json.load(hangman)

usadas = set()
errores = 0
while True:
    real = (random.choice(data)).lower()
    if len(real)>=4: break

palabra = ''.join((normalizar(x) for x in real))

clear()
while True:
    screen.fill('white') ###?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and running:
            for letra, rect in rect.item(): 
                
            

    font_texto = pygame.font.Font(None,40)
    if contador == 11:
        texto = f'Has ganado!! letra: {letra}'
    elif contador > 0 and contador <= 10:
        texto = f"Intentos: {contador}"
    elif contador == 0:
        texto = "Ultimo Intento!"
    else:
        texto = "GAME OVER!"
    text_surface = font_texto.render(texto, True, 'black')
    screen.blit(text_surface,(80,300))
    # ENTRE 4 Y 14 LETRAS
    text_surface = font_texto.render(real[0], True, 'black')
        #screen.blit(text_surface,(500-25*3-3*2,350))
    for i in range(len(real)):
        if len(real) % 2 == 0:
            posicion = (500 + 28*(2*i - len(real) + 1), 350)
        else:
            posicion = (475 + 56*(i - len(real) // 2), 350)
        
        screen.blit(cuadrado_surface, posicion)
        text_surface = font_texto.render(real[i].upper(), True, 'navyblue')
        screen.blit(text_surface,(posicion[0] + 16, posicion[1] + 12))

    screen.blit(titulo_surface, (380,0))

    screen.blit(teclado_1_surface, (330, 130))
    screen.blit(teclado_2_surface, (330, 200))
    screen.blit(teclado_3_surface, (415, 270))

    if contador >= 10:
        screen.blit(unodos_surface, (10,40))
    elif 8<= contador <= 9:
        screen.blit(trescuatro_surface, (10,40))
    elif 5<=contador <= 7:
        screen.blit(cincoseis_surface, (10,40))
    elif 3<= contador <= 4:
        screen.blit(sieteocho_surface, (10,40))
    elif 0<= contador <= 2:
        screen.blit(nuevediez_surface, (10,40))
    else:
        screen.blit(once_surface, (10,40))

    pygame.display.update()
    clock.tick(60)