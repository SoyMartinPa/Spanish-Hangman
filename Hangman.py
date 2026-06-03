import json, os, random
os.chdir(os.path.dirname(__file__))

def valida():
    global invalido
    c= input("Adivinanza: ")
    while not (len(c) == 1 and c in "qwertyuiopasdfghjklñzxcvbnmmáéíóú" and c not in invalido):
        print("\033[1A\033[2K\r", end="")
        c= input("Adivinanza: ")
    c = 'a' if c == 'á' else 'e' if c == 'é' else 'i' if c == 'í' else 'o' if c == 'ó' else 'u' if c == 'ú' else c
    return c

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

with open("spanish.json", "r", encoding="utf-8") as diccionario:
    with open("hangman.json", "r", encoding="utf-8") as hangman:
        data = json.load(diccionario)
        ascii = json.load(hangman)


invalido = ''
errores = 0
while True:
    real = (random.choice(data)).lower()
    if len(real)>=7: break
palabra = ''.join(('a' if x == 'á' else 'e' if x == 'é' else 'i' if x == 'í' else 'o' if x == 'ó' else 'u' if x == 'ú' else x) for x in real)
tabla = ['_' for i in range(len(real))]
lineas = ''
for i in range(len(real)): lineas+=tabla[i]+ ' '

clear()
while True:
    clear()
    print(ascii["Hangman"][errores])
    print(lineas)

    if '_' not in lineas:
        print("Ganaste!")
        break    
    if errores>4:
        print("Perdiste!")
        print(f"Palabra correcta: {palabra.capitalize()}")
        break    

    caracter = valida()
    if caracter in palabra: 
        for i,x in enumerate(real):
            v = 'a' if x == 'á' else 'e' if x == 'é' else 'i' if x == 'í' else 'o' if x == 'ó' else 'u' if x == 'ú' else x
            if caracter == v: tabla[i] = x
    else: 
        errores+=1
        invalido += caracter


    lineas = ''
    for i in range(len(real)): lineas+=tabla[i]+ ' '

#Nota, los tildes son una cosa medio rara del juego que hay que tener en cuenta. 