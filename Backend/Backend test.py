import json, os, random
os.chdir(os.path.dirname(__file__))
ABECEDARIO = "qwertyuiopasdfghjklñzxcvbnmáéíóú"
MAX_ERRORES = 10

def normalizar(c):
    return 'a' if c == 'á' else 'e' if c == 'é' else 'i' if c == 'í' else 'o' if c == 'ó' else 'u' if c == 'ú' else c

def valida(usadas):
    global invalido
    print()
    c= input("  Adivinanza: ").lower().strip()
    while not (len(c) == 1 and c in ABECEDARIO and c not in usadas):
        print("\033[A\033[2K", end="")   # sube 1 línea y la borra
        print("\033[A\033[2K", end="")   # sube otra línea y la borra
        
        if len(c) !=1 : print("  ERROR: Ingresa solo UNA letra a la vez.")
        elif c not in ABECEDARIO: print(f"  ERROR:'{c}' no es una letra válida del abecedario.")
        elif c in invalido or c in tabla: print(f"  ERROR: la letra '{c}' ya fue ingresada antes.")
        c= input("  Adivinanza: ")
    c = normalizar(c)
    return c

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

with open("spanish.json", "r", encoding="utf-8") as diccionario:
    with open("hangman.json", "r", encoding="utf-8") as hangman:
        data = json.load(diccionario)
        ascii = json.load(hangman)


invalido = ''
usadas = ''
errores = 0

while True:
    real = (random.choice(data)).lower()
    if len(real)>=4: break

palabra = ''.join((normalizar(x) for x in real))
tabla = ['_' for i in range(len(real))]
lineas = ''


for i in range(len(real)): lineas+=tabla[i]+ ' '


clear()

while True:
    clear()
    print(ascii["Hangman"][errores])
    print(f"\n  {lineas}\n")
    print(f"  Intentos fallidos  : {errores}/10")
    print(f"  Intentos restantes : {10 - errores}")
    if invalido: print(f"  Letras incorrectas : {', '.join(invalido)}")

    if '_' not in lineas:
        print("\n  Ganaste!")
        break    
    if errores>=10:
        print("\n  Perdiste!")
        print(f"  Palabra correcta: {palabra.capitalize()}")
        break    

    print()
    caracter = valida(usadas)
    if caracter in palabra: 
        for i,x in enumerate(real):
            v = normalizar(x)
            if caracter == v: 
                tabla[i] = x

    else: 
        errores+=1
        invalido += caracter
    usadas += caracter

    lineas = ''
    for i in range(len(real)): lineas+=tabla[i]+ ' '

#Nota, los tildes son una cosa medio rara del juego que hay que tener en cuenta. 