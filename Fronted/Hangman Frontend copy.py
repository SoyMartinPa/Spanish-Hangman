import pygame, random, subprocess, os
from sys import exit

os.chdir(os.path.dirname(__file__))
pygame.init()

screen = pygame.display.set_mode((1000, 350))
pygame.display.set_caption("Proyecto Programacion")
clock = pygame.time.Clock()

# ── Assets ──────────────────────────────────────────────────────────────────

def cargar_assets():
    def img(path, size=None):
        s = pygame.image.load(path)
        return pygame.transform.scale(s, size) if size else s

    return {
        "titulo":      img('graficos/TITLE.png'),
        "teclado_1":   img('graficos/FIRST.png'),
        "teclado_2":   img('graficos/SECOND.png'),
        "teclado_3":   img('graficos/THIRD.png'),
        "palo":        img('graficos/gallow.png',       (250, 250)),
        "unodos":      img('graficos/unodos.png',       (250, 250)),
        "trescuatro":  img('graficos/trescuatro.png',   (250, 250)),
        "cincoseis":   img('graficos/cincoseis.png',    (250, 250)),
        "sieteocho":   img('graficos/sietocoho.png',    (250, 250)),
        "nuevediez":   img('graficos/nuevedies.png',    (250, 250)),
        "once":        img('graficos/once.png',         (250, 250)),
    }

# ── Rects ────────────────────────────────────────────────────────────────────

def crear_rects():
    fila1 = "qwertyuiop"
    fila2 = "asdfghjklñ"
    fila3 = "zxcvbnm"
    ancho1 = 55.4
    ancho3 = 386 / 7
    rects = {}
    for i, l in enumerate(fila1):
        rects[l] = pygame.Rect(ancho1 * i, 0, ancho1, 50).move(330, 130)
    for i, l in enumerate(fila2):
        rects[l] = pygame.Rect(ancho1 * i, 0, ancho1, 50).move(330, 200)
    for i, l in enumerate(fila3):
        rects[l] = pygame.Rect(ancho3 * i, 0, ancho3, 50).move(415, 270)
    return rects

# ── Lógica ───────────────────────────────────────────────────────────────────

def clear():
    subprocess.run(['cmd', '/c', 'cls'] if os.name == 'nt' else ['clear'])

def elige_letra_random():
    return random.choice("qwertyuiopasdfghjklñzxcvbnm")

def emoji_segun_contador(assets, contador):
    if contador >= 10:   return assets["unodos"]
    elif contador >= 8:  return assets["trescuatro"]
    elif contador >= 5:  return assets["cincoseis"]
    elif contador >= 3:  return assets["sieteocho"]
    elif contador >= 0:  return assets["nuevediez"]
    else:                return assets["once"]

def texto_segun_contador(contador, letra):
    if contador == 11:  return f'¡Ganaste! Letra: {letra}'
    elif contador > 0:  return f'Intentos: {contador}'
    elif contador == 0: return 'Último intento!'
    else:               return 'GAME OVER!'

# ── Dibujar ──────────────────────────────────────────────────────────────────

def dibujar(screen, assets, contador, letra):
    screen.fill('white')
    font = pygame.font.Font(None, 36)
    texto = texto_segun_contador(contador, letra)
    screen.blit(font.render(texto, True, 'black'), (80, 300))
    screen.blit(assets["titulo"],   (380, 0))
    screen.blit(assets["teclado_1"],(330, 130))
    screen.blit(assets["teclado_2"],(330, 200))
    screen.blit(assets["teclado_3"],(415, 270))
    screen.blit(emoji_segun_contador(assets, contador), (10, 40))
    pygame.display.update()

# ── Revisión ─────────────────────────────────────────────────────────────────

def revisa_letra(player_letra, random_letra, contador):
    if player_letra == random_letra:
        clear()
        print(f"{player_letra} es la letra correcta!")
        return 11  # señal de victoria
    else:
        contador -= 1
        clear()
        print(f"{player_letra} es incorrecta. Intentos restantes: {contador}")
        if contador < 0:
            print("GAME OVER!")
        return contador

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    assets = cargar_assets()
    rects  = crear_rects()
    letra  = elige_letra_random()
    contador = 10
    running  = True

    clear()
    print("¡Adivina la letra!\n")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and running:
                for l, rect in rects.items():
                    if rect.collidepoint(event.pos):
                        contador = revisa_letra(l, letra, contador)
                        if contador == 11 or contador < 0:
                            running = False
                        break

        dibujar(screen, assets, contador, letra)
        clock.tick(60)

if __name__ == "__main__":
    main()