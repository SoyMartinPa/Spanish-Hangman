import pygame, random, subprocess, os
from sys import exit

pygame.init()

screen = pygame.display.set_mode((1000,350))
screen.fill('white')
pygame.display.set_caption("Proyecto Programacion")
clock = pygame.time.Clock()

titulo_surface = pygame.image.load('graficos/TITLE.png')
teclado_1_surface = pygame.image.load('graficos/FIRST.png')
teclado_2_surface = pygame.image.load('graficos/SECOND.png')
teclado_3_surface = pygame.image.load('graficos/THIRD.png')

palo_surface = pygame.image.load('graficos/gallow.png')
palo_surface = pygame.transform.scale(palo_surface, (250,250))

unodos_surface = pygame.image.load('graficos/unodos.png')
unodos_surface = pygame.transform.scale(unodos_surface, (250,250))
trescuatro_surface = pygame.image.load('graficos/trescuatro.png')
trescuatro_surface = pygame.transform.scale(trescuatro_surface, (250,250))
cincoseis_surface = pygame.image.load('graficos/cincoseis.png')
cincoseis_surface = pygame.transform.scale(cincoseis_surface, (250,250))
sieteocho_surface = pygame.image.load('graficos/sietocoho.png')
sieteocho_surface = pygame.transform.scale(sieteocho_surface, (250,250))
nuevediez_surface = pygame.image.load('graficos/nuevedies.png')
nuevediez_surface = pygame.transform.scale(nuevediez_surface, (250,250))
once_surface = pygame.image.load('graficos/once.png')
once_surface = pygame.transform.scale(once_surface, (250,250))

# Area de CLicks 1
rect_q = pygame.Rect(0,0,55.4,50)
rect_w = pygame.Rect(55.4,0,55.4,50)
rect_e = pygame.Rect(55.4*2,0,55.4,50)
rect_r = pygame.Rect(55.4*3,0,55.4,50)
rect_t = pygame.Rect(55.4*4,0,55.4,50)

rect_y = pygame.Rect(55.4*5,0,55.4,50)
rect_u = pygame.Rect(55.4*6,0,55.4,50)
rect_i = pygame.Rect(55.4*7,0,55.4,50)
rect_o = pygame.Rect(55.4*8,0,55.4,50)
rect_p = pygame.Rect(55.4*9,0,55.4,50)


# Area de CLicks 2
rect_a = pygame.Rect(0,0,55.4,50)
rect_s = pygame.Rect(55.4,0,55.4,50)
rect_d = pygame.Rect(55.4*2,0,55.4,50)
rect_f = pygame.Rect(55.4*3,0,55.4,50)
rect_g = pygame.Rect(55.4*4,0,55.4,50)

rect_h = pygame.Rect(55.4*5,0,55.4,50)
rect_j = pygame.Rect(55.4*6,0,55.4,50)
rect_k = pygame.Rect(55.4*7,0,55.4,50)
rect_l = pygame.Rect(55.4*8,0,55.4,50)
rect_nh = pygame.Rect(55.4*9,0,55.4,50)


# Area de CLicks 3
rect_z = pygame.Rect(0,0,386/7,50)
rect_x = pygame.Rect(386/7,0,386/7,50)
rect_c = pygame.Rect((386/7)*2,0,386/7,50)

rect_v = pygame.Rect((386/7)*3,0,386/7,50)
rect_b = pygame.Rect((386/7)*4,0,386/7,50)
rect_n = pygame.Rect((386/7)*5,0,386/7,50)
rect_m = pygame.Rect((386/7)*6,0,386/7,50)


# Mueve el Area a su Imagen
# Primera Fila
clickable_rect_q = rect_q.move(330,130)
clickable_rect_w = rect_w.move(330,130)
clickable_rect_e = rect_e.move(330,130)
clickable_rect_r = rect_r.move(330,130)
clickable_rect_t = rect_t.move(330,130)

clickable_rect_y = rect_y.move(330,130)
clickable_rect_u = rect_u.move(330,130)
clickable_rect_i = rect_i.move(330,130)
clickable_rect_o = rect_o.move(330,130)
clickable_rect_p = rect_p.move(330,130)

# Segunda Fila
clickable_rect_a = rect_a.move(330,200)
clickable_rect_s = rect_s.move(330,200)
clickable_rect_d = rect_d.move(330,200)
clickable_rect_f = rect_f.move(330,200)
clickable_rect_g = rect_g.move(330,200)

clickable_rect_h = rect_h.move(330,200)
clickable_rect_j = rect_j.move(330,200)
clickable_rect_k = rect_k.move(330,200)
clickable_rect_l = rect_l.move(330,200)
clickable_rect_nh = rect_nh.move(330,200)

# Tercera Fila
clickable_rect_z = rect_z.move(415,270)
clickable_rect_x = rect_x.move(415,270)
clickable_rect_c = rect_c.move(415,270)

clickable_rect_v = rect_v.move(415,270)
clickable_rect_b = rect_b.move(415,270)
clickable_rect_n = rect_n.move(415,270)
clickable_rect_m = rect_m.move(415,270)

# Logica del Frontend
"""
Hacer un contador con la siguiente logica:
Intentos 10: El emoji no reacciona (unodos.png)
Intentos 9-8: El emoji se da cuenta (trescuatro.png)
Intentos 7-5: El emoji se pone triste (cincoseis.png)
Intentos 4-3: El emoji se cuestiona sus decisiones de vida (sieteocho.png)
Intentos 2-1: El emoji se esta asfixiando :( (nuevediez.png)
Intentos 0: El emoji murio, RIP (once.png)
"""
# Este contador empieza en 10. Por cada intento fallido, ira bajando
# hasta llegar a 0, donde acabara el juego con un 'game over'.
contador = 10
# mientras sea verdadero, el teclado seguira respondiendo a los clicks
running = True

def game_over(random_letra):
    clear()
    print("GAME OVER!\n")
    print(f"La letra correcta era {random_letra}")
    print("el emoji murio, rip")
    global running
    running = False

def intento_correcto(letra):
    global contador
    contador = 11
    clear()
    print(f"{letra} es la letra correcta!")
    print("el emoji sobrevivio, yippiee")
    global running
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

# funcion para testear nomas
def elige_letra_random() -> str:
    letras = "qwertyuiopasdfghjklñzxcvbnm"
    letra_random = random.choice(letras)
    return letra_random

# funcion que limpia la terminal
def clear():
    if os.name == 'nt':
        subprocess.run(['cmd','/c','cls'])
    else:
        subprocess.run(['clear'])

# funcion para revisar si la letra seleccionada es igual a la letra random
def revisa_letra(player_letra:str, random_letra:str):
    if player_letra == random_letra:
        intento_correcto(player_letra)
    else:
        intento_fallido(player_letra,random_letra)

# inicia el juego con el programa eligiendo una letra random
letra = elige_letra_random()
clear()
print("Adivina la letra!\n")
# CHEAT para testear xd
# print(f"la letra correcta es {letra}")

while True:
    screen.fill('white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and running:
            # PRIMERA FILA
            if clickable_rect_q.collidepoint(event.pos):
                print("La q fue oprimida")
                revisa_letra("q",letra)
            elif clickable_rect_w.collidepoint(event.pos):
                print("La w fue oprimida")
                revisa_letra("w",letra)
            elif clickable_rect_e.collidepoint(event.pos):
                print("La e fue oprimida")
                revisa_letra("e",letra)    
            elif clickable_rect_r.collidepoint(event.pos):
                print("La r fue oprimida")
                revisa_letra("r",letra)
            elif clickable_rect_t.collidepoint(event.pos):
                print("La t fue oprimida")
                revisa_letra("t",letra)

            elif clickable_rect_y.collidepoint(event.pos):
                print("La y fue oprimida")
                revisa_letra("y",letra)
            elif clickable_rect_u.collidepoint(event.pos):
                print("La u fue oprimida")
                revisa_letra("u",letra)
            elif clickable_rect_i.collidepoint(event.pos):
                print("La i fue oprimida")
                revisa_letra("i",letra)
            elif clickable_rect_o.collidepoint(event.pos):
                print("La o fue oprimida")
                revisa_letra("o",letra)
            elif clickable_rect_p.collidepoint(event.pos):
                print("La p fue oprimida")
                revisa_letra("p",letra)

            # SEGUNDA FILA
            elif clickable_rect_a.collidepoint(event.pos):
                print("La a fue oprimida")
                revisa_letra("a",letra)
            elif clickable_rect_s.collidepoint(event.pos):
                print("La s fue oprimida")
                revisa_letra("s",letra)
            elif clickable_rect_d.collidepoint(event.pos):
                print("La d fue oprimida")
                revisa_letra("d",letra)
            elif clickable_rect_f.collidepoint(event.pos):
                print("La f fue oprimida")
                revisa_letra("f",letra)
            elif clickable_rect_g.collidepoint(event.pos):
                print("La g fue oprimida")
                revisa_letra("g",letra)

            elif clickable_rect_h.collidepoint(event.pos):
                print("La h fue oprimida")
                revisa_letra("h",letra)
            elif clickable_rect_j.collidepoint(event.pos):
                print("La j fue oprimida")
                revisa_letra("j",letra)
            elif clickable_rect_k.collidepoint(event.pos):
                print("La k fue oprimida")
                revisa_letra("k",letra)
            elif clickable_rect_l.collidepoint(event.pos):
                print("La l fue oprimida")
                revisa_letra("l",letra)
            elif clickable_rect_nh.collidepoint(event.pos):
                print("La ñ fue oprimida")
                revisa_letra("ñ",letra)

            # TERCERA FILA
            elif clickable_rect_z.collidepoint(event.pos):
                print("La z fue oprimida")
                revisa_letra("z",letra)
            elif clickable_rect_x.collidepoint(event.pos):
                print("La x fue oprimida")
                revisa_letra("x",letra)
            elif clickable_rect_c.collidepoint(event.pos):
                print("La c fue oprimida")
                revisa_letra("c",letra)

            elif clickable_rect_v.collidepoint(event.pos):
                print("La v fue oprimida")
                revisa_letra("v",letra)
            elif clickable_rect_b.collidepoint(event.pos):
                print("La b fue oprimida")
                revisa_letra("b",letra)
            elif clickable_rect_n.collidepoint(event.pos):
                print("La n fue oprimida")
                revisa_letra("n",letra)
            elif clickable_rect_m.collidepoint(event.pos):
                print("La m fue oprimida")
                revisa_letra("m",letra)

    font_texto = pygame.font.Font(None,36)
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

    screen.blit(titulo_surface, (380,0))

    screen.blit(teclado_1_surface, (330, 130))
    screen.blit(teclado_2_surface, (330, 200))
    screen.blit(teclado_3_surface, (415, 270))

    if contador >= 10:
        screen.blit(unodos_surface, (10,40))
    elif contador <= 9 and contador >= 8:
        screen.blit(trescuatro_surface, (10,40))
    elif contador <= 7 and contador >= 5:
        screen.blit(cincoseis_surface, (10,40))
    elif contador <= 4 and contador >= 3:
        screen.blit(sieteocho_surface, (10,40))
    elif contador <= 2 and contador >= 0:
        screen.blit(nuevediez_surface, (10,40))
    else:
        screen.blit(once_surface, (10,40))

    pygame.display.update()
    clock.tick(60)